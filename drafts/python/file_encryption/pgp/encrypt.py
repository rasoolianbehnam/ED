import getpass
import sys, os
import shutil
import base64

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
    dirname  = os.path.dirname(file)
    basename = os.path.basename(file)
    command = 'gpg --batch --passphrase "%s" -o "%s/%s.gpg" -c "%s"'%(password, dirname, basename[::-1], file)
    code = os.system(command)
    if  code == 0:
        os.remove(file)
        #shutil.move("%s.gpg"%file, "%s/%s.gpg"%(dirname, basename[::-1]))
    else:
        print(code)
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
