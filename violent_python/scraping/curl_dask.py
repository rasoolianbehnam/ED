import re
import os
import subprocess
from dask import delayed, compute

parallel_requests = 16
curl_template = """
curl 'https://s6.openstream.io/hls/qvsbe4jhmdblgwsztru2a6wha442g2tzcmkoawk3rjkv2radnknvcx7gmdva/seg-%d-v1-a1.jpg' -H 'Connection: keep-alive' -H 'Sec-Fetch-Dest: empty' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36' -H 'DNT: 1' -H 'Accept: */*' -H 'Origin: https://embed.streamx.me' -H 'Sec-Fetch-Site: cross-site' -H 'Sec-Fetch-Mode: cors' -H 'Referer: https://embed.streamx.me/?k=0ef002e8f2ffdfbe02e1a0ebbe55ab2f&li=0&tham=1584229621&lt=os&st=5b59af664b9f90b4d00f73cc3916bb6692b1ebd3f8cf22e31b04fb1d6adcf4e089a1d8a35f764484574a5ff3c1750637740a3f9dcbd67dcd6ce37a3be4590731cf2ccb7bea24ca00c3e7bcea8daafe86c2a64227a603205da0f677bb150f6520ba92a6f54af63199dd63bf7b67fd55def64f0b673e2a0b68ba4f080228f86d890f8b550184e927b046275f93ed1c7588&qlt=720p&spq=p&prv=&key=cd611dc6ecb91abf8df84ca6ae889413&ua=802a1200e7ca638d6a6071bfed50e66dd9601ba77a61cd5f11804df3c90df345653cde993e9e048349bc2f40bc30179570ba61df020566c38708e7f2979d6eb92a4a8c1767892b29a014c70b10d1857ed57417ab868b28c76b5a125987b828e3e2cc174cff45417bd6434b46707b4506f5417626325a7afde47fa9f3c4fa3bc8&h=1584229621' -H 'Accept-Language: en-US,en;q=0.9,fa;q=0.8' --compressed
""".strip()
min_num = 1
max_num = 8440
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

counts = {}
max_tries = 5
q = [i for i in range(min_num, max_num+1) if not os.path.isfile(file_name_template%i)]

def test(a):
    curl_command = curl_template%a
    file_name    = file_name_template%a
    try:
        output = subprocess.check_output(\
                "%s > %s"%(curl_command, file_name), 
                stderr=subprocess.STDOUT, shell=True)
        print('%s'%curl_command)
    except subprocess.CalledProcessError as ex:
        pass

compute([delayed(test)(a) for a in q], schedule='threads')
