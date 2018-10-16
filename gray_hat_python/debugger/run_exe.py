from ctypes import *
from my_debugger_defines import *
import sys

PAGE_READWRITE      = 0x04
PROCESS_ALL_ACCESS  = (0x000F0000 | 0x00100000 | 0xFFF )
VIRTUAL_MEM         = (0x1000 | 0x2000)

kernel32 = windll.kernel32

#pid      = sys.argv[1]
pid      = 'C:\\Windows\\system32\\calc.exe'
#dll_path = sys.argv[2]

#len_dll = len(dll_path)

#h_process = kernel32.OpenProcess( PROCESS_ALL_ACCESS, False, int(pid))

creation_flags          = DEBUG_PROCESS

process_information     = PROCESS_INFORMATION()
startupinfo             = STARTUPINFO()
startupinfo.cb          = sizeof(startupinfo)
startupinfo.dwFlags     = 0x1
startupinfo.wShowWindow = 0x0

if kernel32.CreateProcessA(pid,
                           None,
                           None,
                           None,
                           None,
                           creation_flags,
                           None,
                           None,
                           byref(startupinfo),
                           byref(process_information)):
    print("[*] We have successfully launched the process!")
    pid = process_information.dwProcessId
    print("[*] PID: %d" % process_information.dwProcessId)
    h_handle = kernel32.OpenProcess(PROCESS_ALL_ACCESS, pid, False)
    #kernel32.DebugActiveProcess(pid)
    #debug_event = DEBUG_EVENT()
    #continue_status = DBG_CONTINUE
    #kernel32.WaitForDebugEvent(byref(debug_event), INFINITE)
    #kernel32.ContinueDebugEvent(debug_event.dwProcessId,
    #                            debug_event.dwThreadId,
    #                            continue_status)
    kernel32.DebugActiveProcessStop(pid)
else:
    print("[*] Error: 0x%08x." % kernel32.GetLastError())

