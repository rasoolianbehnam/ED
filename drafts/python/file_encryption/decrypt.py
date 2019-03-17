from file_encryption import *
import getpass
import sys, os

def printUsage():
    print "USAGE: python %s <filename>" % (sys.argv[0])

def get_pass():
    password = getpass.getpass("Please enter password: ")
    remaining_len = 16 - (len(password) % 16)
    return password + '*'*remaining_len


def decrypt_dir(dir):
    password = get_pass()
    for d, p, f in os.walk(dir):
        for ff in f:
            if ff.endswith(".enc"):
                file = "%s/%s"%(d, ff)
                decrypt(file, password=password)



def decrypt(file, password=None):
    if password is None:
        password = get_pass()
    out = decrypt_file(password, file)
    if (out is not None):
        out_hash = md5(out);
        dirname  = os.path.dirname(out)
        basename = os.path.basename(out)
        with open(dirname+"/."+basename+".hash", 'r') as f:
            current_hash = f.readline()[:-2]
        #print out_hash
        #print current_hash
        if out_hash == current_hash:
            os.remove(file)
            os.remove(dirname+"/."+basename+'.hash')
            print("[*] Finished decryption of %s."%file)
        else:
            os.remove(out)
            print("Hashes don't match!")

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
