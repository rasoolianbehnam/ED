import socket
import time
socket.setdefaulttimeout(2)

#target = raw_input('Target host (like ww.ccsf.edu): ')
target = 'attackdirect.samsclass.info'
tport = 3100
for tport in [3100, 3200, 3300, 3400, 3500, 3600, 3700, 3800, 3900]:
    print "Port: %d"%tport
    try:
        s1 = socket.socket()
        s2 = socket.socket()
        s3 = socket.socket()

        s1.connect((target, 3100))
        print('s1 connected')
        s1.close()
        s2.connect((target, tport))
        print('s2 connected')
        s2.close()
        time.sleep(2)
        s3.connect((target, 3003))
        print('s3 connected')
        out = s3.recv(1024)
        s3.close()
        print out
    except Exception, e:
        print e
