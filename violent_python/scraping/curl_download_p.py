import re
import Queue
import subprocess
import multiprocessing
import os
import time

parallel_requests = 8
curl_template = "curl 'https://stream-2-1.loadshare.org/stream/VideoID-wM5vckU5/IpU-vKkyc7N4-3BVVRqTuXz8nYcmIXFyCXd5CrO01Zv2r3FlqyOoXutp6vbiLakRCojQwMQdcUj3CioSNuzu9ytmRP2EtXy42FSpyy0BZCAUCqJIk1D7EvIuZlLuT3OakVWhc0Wt5RIGNdl8ff_Wfg/seg-%d-f2-v1-a1.ts?token=ip=97.80.236.60~st=1548972835~exp=1548987235~acl=/*~hmac=057e7a6ea11435468e4845c09bab5f57741ca3dbb6729bf01d971d7939844c17' -H 'origin: https://putlocker.digital' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: en-US,en;q=0.9' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 OPR/57.0.3098.116' -H 'accept: */*' -H 'referer: https://putlocker.digital/tv-series/stranger-things-season-1/7JacmszI/mPRjSOQh/3QhHXCKC-watch-online-free.html' -H 'authority: stream-2-1.loadshare.org' --compressed"
min_num = 1
max_num = 550

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
    my_thread = multiprocessing.Process(target=test)
    my_thread.start()
    #test()

