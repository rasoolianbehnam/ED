import socket

target_ip='127.0.0.1'
target_port=9999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((target_ip, target_port))

message = "GET / HTTP/1.1 \r\nHost: www.google.com\r\n\r\n"
client.send(message)

response = client.recv(4096)
print response
