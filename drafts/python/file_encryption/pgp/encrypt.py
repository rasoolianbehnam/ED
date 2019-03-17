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
    return password

def encrypt_dir(dir):
    password = get_pass()
    for d, p, f in os.walk(dir):
        for ff in f:
            if ff.endswith(".gpg"):
                continue
            file = "%s/%s"%(d, ff)
            encrypt(file, password=password)

def encrypt(file, password=None):
    if password is None:
        password = get_pass()
    command = 'gpg --batch --passphrase "%s" -c "%s"'%(password, file)
    if os.system(command) == 0:
        os.remove(file)
    else:
        sys.exit(0)
    print("Finished encrypting file %s"%file)

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
