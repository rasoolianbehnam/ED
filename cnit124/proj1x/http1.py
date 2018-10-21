import socket
socket.setdefaulttimeout(2)

#target = raw_input('Target host (like ww.ccsf.edu): ')
target = 'attackdirect.samsclass.info'
for i in range(1, 65535//1000):
    tport = i * 1000
    try:
        s = socket.socket()
        s.connect((target, tport))
        print tport
        out = s.recv(1024)
        print out
        s.close()
    except:
        pass
