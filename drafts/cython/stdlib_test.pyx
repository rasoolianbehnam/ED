from libc.stdlib cimport atoi
from libc.math cimport sin

cdef parse_charptr_to_py_int(char* s):
    assert s is not NULL, "byte string value is NULL"
    return atoi(s)

cdef double f(double x):
    return sin(x * x)

def mardas(x):
    return sin(x*x)
