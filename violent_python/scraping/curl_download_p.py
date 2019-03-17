import re
import Queue
import subprocess
import multiprocessing
import os
import time

parallel_requests = 8
curl_template = r"""curl 'https://cdn.mcloud.to/stream/sf:i0:q2:h0:p27:l2/_h0HZ5BuXOaXOOquDAB7Wg/1551718800/i/c/a/6vnpj7/hls/480/480-%04d.ts' -H 'origin: https://mcloud.to' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: en-US,en;q=0.9' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.79' -H 'accept: */*' -H 'referer: https://mcloud.to/embed/@6@37OW3CPA7IP65?sub.file=https%%253A%%252F%%252Fwww6.putlockertv.to%%252Fsubtitle%%252F41652.vtt&ui=rQxi7arr6OYCmI2Gb9QCsJJcqoaXNIvKxzKsUtk%%3D&autostart=true' -H 'authority: cdn.mcloud.to' -H 'cookie: __cfduid=d472dd19f8ae9d2eea7f199c48694c88b1548558742; _ga=GA1.2.1666346265.1548558744; _gid=GA1.2.907929214.1551645496' --compressed"""
min_num = 1
max_num = 4240

url_regex = re.compile(r'\'.*?\'')
url = url_regex.search(curl_template).group(0)[1:-1]
print "url = ", url
indexOfParams = url.find("?")
if indexOfParams > 0:
    url = url[:indexOfParams]

file_name_template = url.split('/')[-1]
print "file name: ", file_name_template

print("url template: %s"%(url))
print("file name: %s"%(file_name_template))

q = multiprocessing.Queue()
counts = {}
max_tries = 5
for i in range(min_num, max_num+1):
    if not os.path.isfile(file_name_template%i):
        q.put(i)

def test():
    while not q.empty():
        a = q.get()
        curl_command = curl_template%a
        file_name    = file_name_template%a
        try:
            print('%s'%curl_command)
            output = subprocess.check_output(\
                    "%s > %s"%(curl_command, file_name), 
                    stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as ex:
            pass
            #print('Error for %s'%url)
            #count_a = counts.get(a, 0)
            #if count_a < max_tries:
            #    print('scheduling retry')
            #    q.put(a)
            #    counts[a] = count_a+1
            #else:
            #    print('max tries exceeded. giving up...')
        time.sleep(.5)
            


for i in range(parallel_requests):
    my_thread = multiprocessing.Process(target=test)
    my_thread.start()
    #test()

