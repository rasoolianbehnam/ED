import string, sys
from random import *
if len(sys.argv) > 1:
    seed(sys.argv[1])
punctuation = '~!@#$%^&*_'
characters = string.ascii_letters + punctuation  + string.digits
password =  "".join(choice(characters) for x in range(randint(8, 16)))
print(password)
