import hashlib
##1
#import getpass
#passwd = getpass.getpass('Enter password: ')
#print(hashlib.new('md4', passwd.encode('utf-16le'))).hexdigest()

##2
#hashes = ['52c4859c0617e4a8fec24ba890c5fc57',
#        '39057ef3a9fe57d98e7a9bab7cd2f4f9',
#        '19a641d2520b983abb7c931ceff933fa']
#for username in ['ming', 'mohammed', 'sam']:
#    for i in range(100):
#        passwd = "CCSF-%s-%02d"%(username, i)
#        hash = hashlib.new('md4', passwd.encode('utf-16le')).hexdigest()
#        if hash in hashes:
#            print username, passwd, hash

##3
#hashes = {'ming': '7621eca98fe6a1885d4f5f56a0525915',
#        'mohammed': 'b2173861e8787a326fb4476aa9585e1c',
#        'sam': '42e646b706acfab0cf8079351d176121'}
#for username, hash in hashes.items():
#    for i in range(100):
#        passwd = "CCSF-%s-%02d"%(username, i)
#        my_hash = passwd
#        for j in range(100):
#            my_hash = hashlib.new('md5', my_hash).hexdigest()
#            #print my_hash
#            if my_hash == hash:
#                print username, passwd, hash
#                break
