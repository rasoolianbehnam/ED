import getpass
import sys, os
import shutil
import base64

def printUsage():
    print("USAGE: python %s <filename>" % (sys.argv[0]))

def get_pass():
    return getpass.getpass("Please enter password: ")


def decrypt_dir(dir):
    password = get_pass()
    for d, p, f in os.walk(dir):
        for ff in f:
            if ff.endswith(".gpg"):
                file = "%s/%s"%(d, ff)
                decrypt(file, password=password)



def decrypt(file, password=None):
    if password is None:
        password = get_pass()
    out_file = file[:-4]
    dirname  = os.path.dirname(out_file)
    basename = os.path.basename(out_file)
    command = 'gpg --batch --passphrase "%s" -o "%s/%s" -d "%s"'%(password, dirname, basename[::-1], file)
    #print(command)
    #command = "gpg --batch --passphrase %s -c %s"%(password, file)
    if os.system(command) == 0:
        os.remove(file)
        #shutil.move(out_file, "%s/%s"%(dirname, basename[::-1]))
    else:
        sys.exit(0)

if __name__=="__main__":
    if len(sys.argv) < 2:
        pintUsage()
        sys.exit(0)
    if os.path.isfile(sys.argv[1]):
        decrypt(sys.argv[1])
    elif os.path.isdir(sys.argv[1]):
        decrypt_dir(sys.argv[1])
    else:
        print("File %s doesn't exist. Exitting."%sys.argv[1])
        sys.exit(0)
