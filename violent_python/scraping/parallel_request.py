import requests
import Queue
import threading
import subprocess
import time
import os

last_url = 'https://hawk.streamvid.co/tsfiles/ADEDBFCH/1080K/2018/EFDCEIFD/09/FCFEFCAB/27/DBBBAECG/35964-561.ts'
parallel_requests = 5




file_name = last_url.split('/')[-1]
extension = file_name.split('.')[-1]
base = file_name.split('-')[0]
max_number = int(file_name.split('-')[1].split('.')[0])
base_name = '%s-%s.%s'%(base, '%03d', extension)
print(file_name, base, max_number,  extension, base_name)
print('Last file name: %s'%file_name)
print('Base: %s'%base)
print('Max number: %s'%max_number)
print('Base name: %s'%(base_name)
url_base = 'https://hawk.streamvid.co/tsfiles/ADEDBFCH/1080K/2018/EFDCEIFD/09/FCFEFCAB/27/DBBBAECG/%s'%base_name
print('URL base: %s'%url_base)

q = Queue.Queue()
counts = {}
max_tries = 5
for i in range(max_number+1):
    if not os.path.isfile(base_name%i):
        q.put(i)

def test():
    while not q.empty():
        a = q.get()
        url = url_base%a
        try:
            output = subprocess.check_output('aria2c %s'%url, stderr=subprocess.STDOUT, shell=True)
            print('%s'%url)
        except subprocess.CalledProcessError as ex:
            print('Error for %s'%url)
            count_a = counts.get(a, 0)
            if count_a < max_tries:
                print('scheduling retry')
                q.put(a)
                counts[a] = count_a+1
            else:
                print('max tries exceeded. giving up...')
        time.sleep(.5)
            


for i in range(parallel_requests):
    my_thread = threading.Thread(target=test)
    my_thread.start()

