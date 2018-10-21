import requests
import Queue
import threading
import subprocess
import time
import os

last_url = 'https://cdn.mcloud.to/stream/sf:i0:q2:h0:p27:l2/2for9uzzxrA3EyYKMiTCww/1539622800/h/7/4/dk5yp6/hls/480/480-3440.ts'
parallel_requests = 5




file_name       = last_url.split('/')[-1]
base_url        = last_url[:-len(file_name)]
extension       = file_name.split('.')[-1]
name_base       = file_name.split('-')[0]
max_number      = file_name.split('-')[1].split('.')[0]
len_max_number  = len(max_number)
max_number      = int(max_number)
name_template   = '%s-%s.%s'%(name_base, '%%0%dd'%len_max_number, extension)
url_template    = '%s%s'%(base_url, name_template)
print(file_name, name_base, max_number,  extension, name_template)
print('Last file name: %s'%file_name)
print('Base name: %s'%name_base)
print('Max number: %s'%max_number)
print('Name template: %s'%(name_template))
print('URL base: %s'%url_template)

#q = Queue.Queue()
#counts = {}
#max_tries = 5
#for i in range(max_number+1):
#    if not os.path.isfile(name_template%i):
#        q.put(i)
#
#def test():
#    while not q.empty():
#        a = q.get()
#        url = url_template%a
#        try:
#            output = subprocess.check_output('aria2c %s'%url, stderr=subprocess.STDOUT, shell=True)
#            print('%s'%url)
#        except subprocess.CalledProcessError as ex:
#            print('Error for %s'%url)
#            count_a = counts.get(a, 0)
#            if count_a < max_tries:
#                print('scheduling retry')
#                q.put(a)
#                counts[a] = count_a+1
#            else:
#                print('max tries exceeded. giving up...')
#        time.sleep(.5)
#            
#
#
#for i in range(parallel_requests):
#    my_thread = threading.Thread(target=test)
#    my_thread.start()
#
