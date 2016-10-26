# searchEngine
Python 2.7  

##Frontend
###Dependencies
bottle  
beaker  
gevent  
httplib2  
uritemplate  
google-api-python-client  
oauth2client* #not sure if included in prev..

###To start server at port 80:  
python server.py

Test cases are also served here at  
*http://localhost:80/test/1/testcode1.html*  
and  
*http://localhost:80/test/2/testcode1.html*

can run crawler.py at these locations. 

##Backend
###Dependencies
BeautifulSoup 3.2.1 
###To test  
*Server must be running at port 80*  
python tester.py
