from bottle import route, run, template, static_file, request
from collections import Counter
# TEMPLATE_PATH.insert(0, 'views')

wordlist = Counter()


@route('/static/<filename:path>')
def send_static(filename):
    # Apparently need to be careful with ./* working directory
    return static_file(filename, root='./static/')


@route('/')
def hello():
    global wordlist
    return template("search", top_words=wordlist.most_common(20))


@route('/results')
def query_results():
    global wordlist
    query = request.query.q
    # exclude = '!"#$%&()*+,./:;<=>?@[\]^_`{|}~'
    exclude = ""
    clean_query = ''.join(ch for ch in query if ch not in exclude)
    words = clean_query.lower().split()

    query_counter = Counter()
    # Log query word counts
    for word in words:
        query_counter[word] += 1

    wordlist += query_counter

    return template("results", words=query_counter.most_common(),
                    num_words=len(words), query=query)


run(host='localhost', port=8080, debug=True)
