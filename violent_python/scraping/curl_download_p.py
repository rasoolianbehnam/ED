import re
import queue
import subprocess
import multiprocessing
import os
import time

parallel_requests = 8
curl_template = r"""
curl 'https://s30.openstream.io/hls/qvsbceqpmdblgwsztruka24jkexcbo5yxq6igk5bv3tvut3drdyg7funmhuq/seg-%d-v1-a1.ts' -H 'Connection: keep-alive' -H 'Origin: https://embed.streamx.me' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36' -H 'DNT: 1' -H 'Accept: */*' -H 'Sec-Fetch-Site: cross-site' -H 'Sec-Fetch-Mode: cors' -H 'Referer: https://embed.streamx.me/?k=ea5952d6a5ca1273a9ff14c34728ea52&li=0&tham=1579571350&lt=os&st=128fa457b4d3b5eb35b0cefb26ee3649&qlt=720p&spq=p&prv=&key=3699a7a6fec781edeaef36649e7b8560&ua=802a1200e7ca638d6a6071bfed50e66dd9601ba77a61cd5f11804df3c90df345653cde993e9e048349bc2f40bc30179570ba61df020566c38708e7f2979d6eb92a4a8c1767892b29a014c70b10d1857ec4531740d96c3c5c4ec008eb0eb5d84f0d0024446f318631c2d037b0eaf470e28940b0320e9b9b8db8f6148ddc57a2d3&h=1579571350' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,fa;q=0.8' --compressed
""".strip()
min_num = 1
max_num = 5209

url_regex = re.compile(r'\'.*?\'')
url = url_regex.search(curl_template).group(0)[1:-1]
print("url = ", url)
indexOfParams = url.find("?")
if indexOfParams > 0:
    url = url[:indexOfParams]

file_name_template = url.split('/')[-1]
print("file name: ", file_name_template)

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

