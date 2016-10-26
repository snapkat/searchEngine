from gevent import monkey; monkey.patch_all()

import json
import bottle
# from bottle import bottle.route, run, template, static_file, request, redirect
from collections import Counter
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import OAuth2WebServerFlow
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from beaker.middleware import SessionMiddleware
import httplib2

# TEMPLATE_PATH.insert(0, 'views')

session_opts = {
    'session.type': 'file',# Name of backend storing session objects (file, dbm, memory, ext:memcached ,ext:database, ext:google, cookie[max datasize:4096bytes])
    'session.cookie_expires': False,# Cookie tracking client-side expiration. (True = never expire, False = expire at end of browser session)
    'session.data_dir': "./data",# Stores data to given path
    'session.auto': True # True = session will save anytime accessed during a request
}
app = SessionMiddleware(bottle.app(), session_opts)

word_dict = {}
oauth_cred = {}
with open('client_secrets.json') as f:

    oauth_cred = json.loads(f.read())['web']

@bottle.route('/<filename:path>', 'GET')
def serve_pictures(filename):
    return bottle.static_file(filename, root='./static/')


""" Initialization route: checks if session user logged into Moo, else anon-mode """
@bottle.route('/') 
def hello():

    sess = bottle.request.environ.get('beaker.session')

    if (sess.get('code',0)):
        bottle.redirect("/signin")
    else:
        return bottle.template("search")

""" if the sign-in selected, passes user through Google sign-in protocol """
@bottle.route('/signin', 'GET') 
def home():
    flow = flow_from_clientsecrets("client_secrets.json",
        scope='https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email',
        redirect_uri="http://moogle.ml/redirect")

    uri = flow.step1_get_authorize_url()
    bottle.redirect(str(uri))

""" redirect route: If user signed in, will reauthenticate token information """
@bottle.route ('/redirect') 
def redirect_page():
    global oauth_cred
    flow = OAuth2WebServerFlow(client_id=oauth_cred['client_id'],
        client_secret=oauth_cred['client_secret'],
        scope='https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email',
        redirect_uri="http://moogle.ml/redirect")

    code = bottle.request.query.get('code', '')
    print code
    credentials = flow.step2_exchange(code)
    # if token has expired without signout, re-authorize
    if (credentials == None or credentials.invalid):
        bottle.redirect('/signin')

    sess = bottle.request.environ.get('beaker.session')
    #Get sessional user code (as sign-in flag)
    sess['code'] = code

    token = credentials.id_token['sub']	

    http = httplib2.Http()
    http = credentials.authorize(http)


    users_service = build('oauth2','v2',http=http)
    user_document = users_service.userinfo().get().execute()
    user_email = user_document['email']
    #Get sessional user email
    sess['user_email'] = user_email
    sess.save()

    if (sess.get('user_email',0) not in word_dict):
        word_dict[sess.get('user_email',0)] = Counter()

    return bottle.template("login_search", user=user_email,
                top_words=word_dict[sess.get('user_email',0)].most_common(20))

""" changes sign-in status of user """
@bottle.route('/signout', 'GET') 
def goodbye():
    """ logs the user out, returns to anonymous-mode """
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

""" processes search results for user """
@bottle.route('/results') 
def query_results():
    #    global wordlist
    sess = bottle.request.environ.get('beaker.session')

    query = bottle.request.query.q
    # exclude = '!"#$%&()*+,./:;<=>?@[\]^_`{|}~'
    exclude = ""
    clean_query = ''.join(ch for ch in query if ch not in exclude)
    words = clean_query.lower().split()
    
    query_counter = Counter()
    # Log query word counts
    for word in words:
        query_counter[word] += 1

    if (sess.get('code',0)):			
        word_dict[sess.get('user_email',0)] += query_counter

        sess.save()
        return bottle.template("login_results",
                user=sess['user_email'], 
                words=query_counter.most_common(),
                num_words=len(words),
                query=query)

    return bottle.template("results",
                words=query_counter.most_common(),
                num_words=len(words), query=query)


bottle.run(app=app, host='0.0.0.0', port=80, debug=True)
