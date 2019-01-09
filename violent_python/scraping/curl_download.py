import re
import Queue
import subprocess
import threading
import os
import time

parallel_requests = 8
curl = "curl 'https://s20.7fuc.xyz/hls/qvsbcngfn7blgwsztrtka66tjmpr76uxm242ukcoqcyzewtljstdxp6tjuga/seg-6290-v1-a1.jpg' -H 'origin: https://putlocker9.nl' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: en-US,en;q=0.9' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36 OPR/56.0.3051.99' -H 'accept: */*' -H 'referer: https://putlocker9.nl/film/the-predator-2018-1080p.64463/watching.html' -H 'authority: s20.7fuc.xyz' --compressed"
max_style = False

curl = curl.replace('%', '%%')
url_regex = re.compile(r'\'.*?\'')
url = url_regex.search(curl).group(0)[1:-1]
#print url
file_name = url.split('/')[-1]
#print file_name
max_num = file_name.split('-')[1].split('.')[0]
len_max_num = len(max_num)
print max_num, len_max_num

if max_style:
    file_name_template = file_name.replace(max_num, '%%0%dd'%len_max_num)
    print file_name_template

    curl_template = curl.replace(max_num, '%%0%dd'%len_max_num)
    print curl_template
else:
    file_name_template = file_name.replace(max_num, '%d')
    print file_name_template
    curl_template = curl.replace(max_num, '%d')
    print curl_template


q = Queue.Queue()
counts = {}
max_tries = 5
for i in range(int(max_num)+1):
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

