from file_encryption import *
import getpass
import sys, os

def printUsage():
    print "USAGE: python %s <filename>" % (sys.argv[0])

if __name__=="__main__":
    if len(sys.argv) < 2:
        pintUsage()
        sys.exit(0)

    if not os.path.isfile(sys.argv[1]):
        print("File %s doesn't exist. Exitting."%sys.argv[1])
        sys.exit(0)

    password = getpass.getpass("Please enter password: ")
    remaining_len = 16 - (len(password) % 16)
    password = password + '*'*remaining_len
    out = decrypt_file(password, sys.argv[1])
    if (out is not None):
        out_hash = md5(out);
        with open("."+out+".hash", 'r') as f:
            current_hash = f.readline()[:-2]
        #print out_hash
        #print current_hash
        if out_hash == current_hash:
            os.remove(sys.argv[1])
            os.remove("."+out+'.hash')
            print("[*] Finished decryption.")
        else:
            os.remove(out)
            print("Hashes don't match!")
