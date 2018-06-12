import os
import signal
import time
import sys
import threading
import Queue
PID = os.getpid()
goon = Queue.Queue()
goon.put(1)

def print_test():
    while not goon.empty():
        print "pid:", os.getpid()
        time.sleep(1)

pill2kill = threading.Event()
test_thread = threading.Thread(target=print_test)
test_thread.start()
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        goon.get()
        break

    #sys.exit(0)
#while True:
#    try:
#        print os.getpid()
#        time.sleep(1)
#    except KeyboardInterrupt:
#        print "Exitting main...."
#        os.kill(os.getpid(), signal.SIGINT)
