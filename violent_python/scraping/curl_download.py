import re
import Queue
import subprocess
import threading
import os
import time

parallel_requests = 1
curl = "curl 'https://cdn.mcloud.to/stream/sf:i0:q2:h0:p27:l0/0iSpmvTzO8dH9a71-o_zeg/1539882000/j/a/5/jv0py4/hls/480/480-0018.ts' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: https://mcloud.to/embed/@P@841LOC70PIOW5?sub.file=https%253A%252F%252Fwww6.putlockertv.to%252Fsubtitle%252F17167.vtt&ui=rQxi7arr6OYBmIqDdrl0s%40FT3P39JpizwCe5Jqax&autostart=true' -H 'Origin: https://mcloud.to' -H 'Cookie: __cfduid=df4a85557369278cd99a08f037a4249401528946827; _ga=GA1.2.175193271.1539734230; _gid=GA1.2.2120581852.1539734230; _gat=1' -H 'Connection: keep-alive' -H 'DNT: 1' -H 'TE: Trailers'"

curl = curl.replace('%', '%%')
url_regex = re.compile(r'\'.*?\'')
url = url_regex.search(curl).group(0)[1:-1]
#print url
file_name = url.split('/')[-1]
#print file_name
max_num = file_name.split('-')[1].split('.')[0]
len_max_num = len(max_num)
print max_num, len_max_num

file_name_template = file_name.replace(max_num, '%%0%dd'%len_max_num)
print file_name_template

curl_template = curl.replace(max_num, '%%0%dd'%len_max_num)
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
    #my_thread = threading.Thread(target=test)
    #my_thread.start()
    test()

