import bottle
from beaker.middleware import SessionMiddleware

session_opts = {
	'session.type': 'file',			# The name of the backend to use for storing the sessions or cache objects (file,dbm,memory,ext:memcached,ext:database,ext:google,cookie[max datasize:4096bytes])
	'session.cookie_expires': 300,	# Determines when the cookie used to track the client-side of the session will expire. (True = never expire, False = expire at end of browser session)
	'session.data_dir': "./data",	# Stores data to given path
	'session.auto': True			# True = session will save itself anytime it is accessed during a request
}
app = SessionMiddleware(bottle.app(), session_opts)

@bottle.route('/test')
def test():
	s = bottle.request.environ.get('beaker.session')
	s['test'] = s.get('tests',0) + 1
	s.save()
	return 'Test counter: %d' % s['test']
	
bottle.run(app=app)