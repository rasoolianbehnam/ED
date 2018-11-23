import requests
import urllib
import base64
import hashlib
params = """Host: 192.168.0.1
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36 OPR/56.0.3051.104
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: Authorization=Basic%%20%s"""
username = 'mardas'
password = 'admin'
params = params% urllib.quote(base64.b64encode(username + ":" + hashlib.md5(password).hexdigest()))
myparams = {}
for l in params.split('\n'):
    p, v = l.split(':')
    myparams[p.strip()] = v.strip()
url = 'http://192.168.0.1/userRpm/LoginRpm.htm?Save=Save'
print myparams
res = requests.get(url, headers=myparams)
print res.text
