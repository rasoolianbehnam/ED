from file_encryption import *
import getpass
import sys, os

def printUsage():
    print("USAGE: python %s <filename>" % (sys.argv[0]))

def get_pass():
    password = getpass.getpass("Please enter password: ")
    password2 = getpass.getpass("Please verify password: ")
    if (password != password2):
        print("[!] Passwords don't match")
        sys.exit(0)
    remaining_len = 16 - (len(password) % 16)
    return password + '*'*remaining_len

def encrypt_dir(dir):
    password = get_pass()
    for d, p, f in os.walk(dir):
        for ff in f:
            file = "%s/%s"%(d, ff)
            encrypt(file, password=password)

def encrypt(file, password=None):
    if password is None:
        password = get_pass()
    out = encrypt_file(password, file)
    if (out is not None):
        hash = md5(file)
        dirname  = os.path.dirname(file)
        basename = os.path.basename(file)
        with open(dirname + "/." + basename + '.hash', 'w') as f:
            f.write(hash + '\r\n')
        os.remove(file)
    print("[*] Finished encryptiion.")

if __name__=="__main__":
    if len(sys.argv) < 2:
        printUsage()
        sys.exit(0)

    if os.path.isfile(sys.argv[1]):
        encrypt(sys.argv[1])
    elif os.path.isdir(sys.argv[1]):
        encrypt_dir(sys.argv[1])
    else:
        print("File %s doesn't exist. Exitting."%sys.argv[1])
        sys.exit(0)
