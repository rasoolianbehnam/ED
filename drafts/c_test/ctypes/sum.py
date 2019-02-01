import ctypes as ct
pointer = ct.POINTER

_sum = ct.CDLL('./libsum.so')
_sum.our_function.argtypes = (ct.c_int, pointer(ct.c_int))

def out_function(numbers):
    global _sum
    num_numbers = len(numbers)
    array_type = ct.c_int * num_numbers
    result = _sum.our_function(ct.c_int(num_numbers), array_type(*numbers))
    return int(result)

print(out_function([1, 2, 3]))
