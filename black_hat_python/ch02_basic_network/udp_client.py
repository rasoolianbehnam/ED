import socket

target_ip = '127.0.0.1'
target_port = 8080

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client.sendto("AAABBBCCC", (target_ip, target_port))

data, addr = client.recvfrom(4096)

print data

