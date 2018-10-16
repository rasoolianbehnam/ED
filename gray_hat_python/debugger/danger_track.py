from pydbg import *
from pydbg.defines import *

#import utils

dangerous_functions = {
                        "strcpy" : "msvcrt.dll",
                        "strncpy" : "msvcrt.dll",
                        "sprintf" : "msvcrt.dll",
                        "vsprintf" : "msvcrt.dll"
                       }
dangerous_functions_resolved = {}
crash_encountered = False
instruction_count = 0

def danger_handler(dbg):
    esp_offset = 0
    print("[*] Hit %s" % dangerous_functions_resolved[dbg.context.Eip])
    print("===========================================================")

    while esp_offset < 20:
        parameter = dbg.smart_dereference(dbg.context.Esp + esp_offset)
        print("[ESP + %D] => %s" % (esp_offset, parameter))
        esp_offset += 4
    print("===========================================================")
    dbg.suspend_all_threads()
    dbg.process_snapshot()
    dbg.resume_all_thread()

    return DBG_CONTINUE

def access_violation_handler(dbg):
    global crash_encountered

    if dbg.dbg.u.Exception.dbFirstChance:
        return DBG_EXCEPTION_NOT_HANDLED
    crash_bin = utils.crash_binning.crash_binning()
    crash_bin.record_crash(dbg)
    print(crash_bin.crash_synopsis())

    if crash_encountered == False:
        dbg.suspend_all_threads()



dbg = pydbg()
pid = int(raw_input("Enter the PID you wish to monitor: "))

dbg.attach(pid)

for func, dll in dangerous_functions.items():
    func_address = dbg.func_resolve(dll, func)
    print("[*] Resolved breakpoint: %s -> 0x%08x" % (func, func_address))
    dbg.bp_set(func_address, handler=danger_handler)
    dangerous_functions_resolved[func_address] = func

#dbg.set_callback(EXCEPTION_ACCESS_VIOLATION, access_violation_handler)
#dbg.set_callback(EXCEPTION_SINGLE_STEP, single_step_handler)
#dbg.run()
