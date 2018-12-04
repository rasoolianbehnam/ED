import ssl
import socket
import os, sys, re

def main():
    print(ssl.OPENSSL_VERSION)
    curl_text = sys.argv[1]
    replacement_string = sys.argv[2]
    num_last_part = int(sys.argv[3])
    num_threads = int(sys.argv[4])
    num_first_part = 1
    if len(sys.argv) > 5:
        num_first_part = int(sys.argv[5])
    overwrite = False
    if len(sys.argv) > 6:
        if sys.argv[6].lower().find("true") > -1:
            overwrite = True
            print "Overwrite activated"

    c = re.compile("-H '(.*?)'")
    headers = {}
    for line in c.findall(curl_text):
    #    print line
        key = line.split(":")[0]
        value = line[len(key)+2:]
        headers[key] = value

    #print headers

    c = re.compile("curl '(.*?)'")
    url_grand_template = c.search(curl_text).group(1)
    print url_grand_template

    file_name_grand_template = url_grand_template.split("/")[-1]

    c = re.compile("\(.*?\)")
    url_template = c.sub(replacement_string, url_grand_template)
    file_name_template = c.sub(replacement_string, file_name_grand_template)

    c = re.compile("http.*?//(.*?)(/.*)")
    found = c.search(url_template)
    server = found.group(1)
    file_path = found.group(2)
    print server
    print file_path
    if url_template.startswith("https"):
        https = True
        port = 443
    else:
        https = False
        port = 80
    print port

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if https:
        wrappedSocket = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_TLSv1)
    else:
        wrappedSocket = s

    #s.connect((server, port))
    print headers

    packet = "GET %s\r\n"
    for key, value in headers.items():
        packet +=  "%s: %s\r\n"%(key, value)
    packet += "\r\n"
    packet += "\r\n"
    
    wrappedSocket.connect((server, port))
    #wrappedSocket.send(packet)
    #data = ""
    #while True:
    #    buff = wrappedSocket.recv(1024)
    #    if buff is not None:
    #        data += buff
    #    else:
    #        break
    #print data
if __name__=="__main__":
    main()

