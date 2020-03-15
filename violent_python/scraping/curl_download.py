import re
import queue
import subprocess
import threading
import os
import time

parallel_requests = 8
curl_template = "curl 'https://s9.openstream.io/hls/qvsbent5mdblgwsztrx2ay6gjdk7ldfoyvydxvtlborlxxx5ulbih6unaoaq/seg-%d-v1-a1.jpg' -H 'Connection: keep-alive' -H 'Origin: https://embed.streamx.me' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36' -H 'DNT: 1' -H 'Accept: */*' -H 'Sec-Fetch-Site: cross-site' -H 'Sec-Fetch-Mode: cors' -H 'Referer: https://embed.streamx.me/?k=21da0244dcd66c6d9b16fcb9e3590a4f&li=0&tham=1576541748&lt=os&st=5b59af664b9f90b4d00f73cc3916bb6692b1ebd3f8cf22e31b04fb1d6adcf4e09695625524ac7c7f6a3bb9dceda96ec8c281d92a14fd0abe90dddd8e2f4f74d7e3b2c3b9d0c88f2f7e082f4cab5ef4e5a5a9a67ed9b8f2e8c655d9d9488fa6d01ef8fa08ab1db893ed21939466d4a6058a651d818f3e737e459324060eee8e55&qlt=720p&spq=p&prv=&key=56601b06bce5ad7ba3b208a923ffa2d6&ua=802a1200e7ca638d6a6071bfed50e66dd9601ba77a61cd5f11804df3c90df345653cde993e9e048349bc2f40bc30179570ba61df020566c38708e7f2979d6eb92a4a8c1767892b29a014c70b10d1857ef1c3f69c276842b328ac6f92d9a3606c1ee1e2252ea076b07476bac956d10402a9c3685356435bfc651853bf1996a942&h=1576541748' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,fa;q=0.8' --compressed"
min_num = 1
max_num = 7731

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

q = queue.Queue()
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

