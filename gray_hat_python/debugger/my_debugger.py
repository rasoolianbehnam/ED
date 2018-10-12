from ctypes import *
from my_debugger_defines import *

kernel32 = windll.kernel32

class debugger():
    def _init_(self):
        self.h_process          = None
        self.pid                = None
        self.debugger_active    = False
        self.thread_id          = None
        self.context            = None

    def load(self, path_to_exe):
        creation_flags = DEBUG_PROCESS
        #creation_flags  = CREATE_NEW_CONSOLE

        startupinfo = STARTUPINFO()
        process_information = PROCESS_INFORMATION()

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
            print("[*] We have successfully launched the process!")
            print("[*] PID: %d" % process_information.dwProcessId)
            self.h_process = self.open_process(process_information.dwProcessId)
        else:
            print("[*] Error: 0x%08x." % kernel32.GetLastError())

    def open_process(self, pid):
        return kernel32.OpenProcess(PROCESS_ALL_ACCESS, pid, False)

    def attach(self, pid):
        self.h_process = self.open_process(pid)

        if kernel32.DebugActiveProcess(pid):
            self.debugger_active    = True
            self.pid                = int(pid)
            self.run()
        else:
            print("[*] Unable to attach to the process")

    def run(self):
        while self.debugger_active:
            self.get_debug_event()

    def get_debug_event(self):
        debug_event     = DEBUG_EVENT()
        continue_status = DBG_CONTINUE

        if kernel32.WaitForDebugEvent(byref(debug_event), INFINITE):
            self.h_thread = self.open_thread(debug_event.dwThreadId)
            self.context  = self.get_thread_context(self.h_thread)
            print("Event Code: %d Thread Id: %d"%(debug_event.dwDebugEventCode, \
                    debug_event.dwThreadId))
            kernel32.ContinueDebugEvent(\
                    debug_event.dwProcessId,\
                    debug_event.dwThreadId,\
                    continue_status)
    def detach(self):
        if kernel32.DebugActiveProcessStop(self.pid):
            print("[*] Finished debugging. Exiting...")
            return True
        else:
            print("There was an error!")
            return False

    def enumerate_threads(self):
        hSnapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, self.pid)
        if hSnapshot is not None:
            thread_list = []
            thread_entry = THREADENTRY32()
            thread_entry.dwSize = sizeof(thread_entry)
            success = kernel32.Thread32First(hSnapshot, byref(thread_entry))
            while success:
                if thread_entry.th32OwnerProcessID == self.pid:
                    thread_list.append(thread_entry.th32ThreadID)
                success = kernel32.Thread32Next(hSnapshot, byref(thread_entry))
            kernel32.CloseHandle(hSnapshot)
            return thread_list
        else:
            return False
    def open_thread(self, thread_id):
        h_thread = kernel32.OpenThread(THREAD_ALL_ACCESS, None, thread_id)
        if h_thread is None:
            print("[*] Could not obtain a valid thread handle.")
            return False
        return h_thread

    def get_thread_context(self, thread_id):
        h_thread = self.open_thread(thread_id)
        context = CONTEXT()
        context.ContextFlags = CONTEXT_FULL |  CONTEXT_DEBUG_REGISTERS
        if kernel32.GetThreadContext(h_thread, byref(context)):
            kernel32.CloseHandle(h_thread)
            return context
        else:
            return False
