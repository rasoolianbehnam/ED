import socket
socket.setdefaulttimeout(2)
s = socket.socket()

target = raw_input('Target host (like ww.ccsf.edu): ')
tport = 80

s.connect((target, tport))
s.send('HEAD / HTTP/1.1\nHost: ' + target + '\n\n')
print s.recv(1024)
s.close()
