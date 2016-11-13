from gevent import monkey
from collections import Counter
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import OAuth2WebServerFlow
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from beaker.middleware import SessionMiddleware

import json
import bottle
# from bottle import bottle.route, run, template, static_file, request,
# redirect

import httplib2
import redis

monkey.patch_all()

# TEMPLATE_PATH.insert(0, 'views')

session_opts = {
    # Name of backend storing session objects (file, dbm, memory,
    # ext:memcached ,ext:database, ext:google, cookie[max datasize:4096bytes])
    'session.type': 'file',
    # Cookie tracking client-side expiration. (True = never expire, False =
    # expire at end of browser session)
    'session.cookie_expires': False,
    'session.data_dir': "./data",  # Stores data to given path
    'session.auto': True  # True = session will save anytime accessed during a request
}
app = SessionMiddleware(bottle.app(), session_opts)

word_dict = {}
oauth_cred = {}
r = redis.StrictRedis(host="localhost", port=6379, db=0)
r_rank = redis.StrictRedis(host="localhost", port=6379, db=1)

with open('client_secrets.json') as f:
    oauth_cred = json.loads(f.read())['web']


@bottle.route('/<filename:path>', 'GET')
def serve_pictures(filename):
    return bottle.static_file(filename, root='./static/')


@bottle.route('/')
def hello():
    """Initialization route: checks if session user logged into Moo, else
    anon-mode."""

    sess = bottle.request.environ.get('beaker.session')

    if (sess.get('code', 0)):
        bottle.redirect("/signin")
    else:
        return bottle.template("search", user="")


@bottle.route('/signin', 'GET')
def home():
    """If the sign-in selected, passes user through Google sign-in protocol.
    """
    flow = flow_from_clientsecrets("client_secrets.json",
                                   scope='https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email',
                                   redirect_uri="http://moogle.ml/redirect")

    uri = flow.step1_get_authorize_url()
    bottle.redirect(str(uri))


@bottle.route('/redirect')
def redirect_page():
    """Redirect route: If user signed in, will reauthenticate token information.
    """
    global oauth_cred
    flow = OAuth2WebServerFlow(client_id=oauth_cred['client_id'],
                               client_secret=oauth_cred['client_secret'],
                               scope='https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email',
                               redirect_uri="http://moogle.ml/redirect")

    code = bottle.request.query.get('code', '')
    print code
    credentials = flow.step2_exchange(code)
    # if token has expired without signout, re-authorize
    if (credentials is None or credentials.invalid):
        bottle.redirect('/signin')

    sess = bottle.request.environ.get('beaker.session')
    # Get sessional user code (as sign-in flag)
    sess['code'] = code

    token = credentials.id_token['sub']

    http = httplib2.Http()
    http = credentials.authorize(http)

    users_service = build('oauth2', 'v2', http=http)
    user_document = users_service.userinfo().get().execute()
    user_email = user_document['email']
    # Get sessional user email
    sess['user_email'] = user_email
    sess.save()

    if (sess.get('user_email', 0) not in word_dict):
        word_dict[sess.get('user_email', 0)] = Counter()

    return bottle.template("search", user=user_email,
                           top_words=word_dict[sess.get('user_email', 0)].most_common(20))


@bottle.route('/signout', 'GET')
def goodbye():
    """Changes sign-in status of user. """
    """Logs the user out, returns to anonymous-mode. """
    sess = bottle.request.environ.get('beaker.session')
    sess.delete()

    bottle.redirect("/")


@bottle.route('/test/1/<filename:path>')
def test_1(filename):
    # Apparently need to be careful with ./* working directory
    return bottle.static_file(filename, root='./htmlcase1/')


@bottle.route('/test/2/<filename:path>')
def test_2(filename):
    # Apparently need to be careful with ./* working directory
    return bottle.static_file(filename, root='./htmlcase2/')


@bottle.route('/static/<filename:path>')
def send_static(filename):
    # Apparently need to be careful with ./* working directory
    return bottle.static_file(filename, root='./')


def get_resolved_urls(word, cursor=0, count=5):
    """Returns a list of urls where the document contains the word."""
    w_id = r.hget("word_to_id", word)

    doc_id_set = r.smembers("word_id_to_doc_ids:%s" % w_id)
    doc_rank = []
    for doc_id in doc_id_set:
        url = r.hget("id_to_doc", doc_id)
        pg_rank = float(r_rank.hget("doc_id_ranks", doc_id))
        doc_rank.append((pg_rank, url))

    return sorted(doc_rank, key=lambda tup: tup[0], reverse=True)


def query_results():
    query = bottle.request.query.q
    # exclude = '!"#$%&()*+,./:;<=>?@[\]^_`{|}~'
    exclude = ""
    clean_query = ''.join(ch for ch in query if ch not in exclude)
    words = clean_query.lower().split()

    query_counter = Counter()
    # Log query word counts
    for word in words:
        query_counter[word] += 1

    # Get search results
    if not words:
        return ""

    # pulls data from the redis db to build the sorted list of urls
    page = int(bottle.request.query.page)

    hits_by_rank = get_resolved_urls(words[0])
    print "#hits", len(hits_by_rank)

    # Paging
    num_pages = len(hits_by_rank) // 5
    if len(hits_by_rank) % 5:
        num_pages += 1
    print "num_pages", num_pages, "page", page

    if page > num_pages:
        page = num_pages

    start = (page - 1) * 5
    page_results = hits_by_rank[start: min(start + 5, len(hits_by_rank))]
    print "page_results", page_results

    return {"words": query_counter, "num_words": len(words), "query": query,
            "rslt_lst": page_results}


@bottle.route('/results')
def ajax_query():
    d = query_results()
    if not d:
        return ""

    d["words"] = d["words"].most_common()
    return bottle.template("res", d)


@bottle.route('/top20')
def top20_results():
    d = query_results()

    sess = bottle.request.environ.get('beaker.session')
    if (sess.get('code', 0)):
        word_dict[sess.get('user_email', 0)] += d["words"]

        sess.save()
        top_words = word_dict[sess.get('user_email', 0)].most_common(20)

        return bottle.template("top20", user=sess['user_email'],
                               top_words=top_words)

    return ""


@bottle.error(400)
@bottle.error(404)
def error_handle(error):
    sess = bottle.request.environ.get('beaker.session')
    return bottle.template("error", user="")


bottle.run(app=app, host='0.0.0.0', port=80, debug=True)
