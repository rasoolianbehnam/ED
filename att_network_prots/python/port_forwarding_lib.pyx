from libc.string cimport strcpy, strncpy
from libc.stdlib cimport malloc, free

def hexdump2(char* src, length=16):
    cdef char *s, *hexa, *text;
    cdef char **result
    cdef int digits;
    s = <char*> malloc(length * sizeof(s))
    for i in xrange(0, len, length):
        strcpy(s, src[i:i+length])
        hexa = b' '.join(["%0*X" % (digits, ord(x)) for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append( b"%04X   %-*s  %s" % (i, length*(digits + 1), hexa, text) )
    #print b'\n'.join(result)
