from file_encryption import *
import getpass
import sys, os

if len(sys.argv) < 2:
    print "USAGE: python %s <filename>" % (sys.argv[0])
    sys.exit(0);
password = getpass.getpass("Please enter password: ")
password2 = getpass.getpass("Please verify password: ")
if (password != password2):
    print "[!] Passwords don't match"
    sys.exit(0)
remaining_len = 16 - (len(password) % 16)
password = password + '*'*remaining_len
out = encrypt_file(password, sys.argv[1])
if (out is not None):
    hash = md5(sys.argv[1])
    with open(sys.argv[1] + '.hash', 'w') as f:
        f.write(hash + '\r\n')
    os.remove(sys.argv[1])
print("[*] Finished encryptiion.")
