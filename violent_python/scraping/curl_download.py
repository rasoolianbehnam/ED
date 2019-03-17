import re
import Queue
import subprocess
import threading
import os
import time

parallel_requests = 8
curl_template = "curl 'https://s6.openstream.io/hls/qvsbdbfjndblgwsztqeka2ujbdwodk42bcrmlhwss4sgownzyku3s3aidliq/seg-%d-v1-a1.jpg' -H 'Origin: https://embed.streamx.me' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 OPR/57.0.3098.116' -H 'Accept: */*' -H 'Referer: https://embed.streamx.me/?k=9c8c90d64dcdaef65fb5f8ea04cd3e8e&li=0&tham=1549248810&lt=os&st=128fa457b4d3b5eb35b0cefb26ee3649&qlt=720p&spq=p&prv=&key=67d48e8127b9d819a580c347c034274e&h=1549248810&w=100%&h=675' -H 'Connection: keep-alive' --compressed"
min_num = 1
max_num = 5000

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

q = Queue.Queue()
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
            output = subprocess.check_output(\
                    "%s > %s"%(curl_command, file_name), 
                    stderr=subprocess.STDOUT, shell=True)
            print('%s'%curl_command)
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
    my_thread = threading.Thread(target=test)
    my_thread.start()
    #test()

