import socket
import threading

bind_ip = '127.0.0.1'
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)
print("[*] listening on %s:%d"%(bind_ip, bind_port))
def handle_client(client_socket):
    try:
        request = client_socket.recv(1024)
        print "[*] received %s"%request
        client_socket.send("ACK!")
    except Exception as e:
        print e
        print "[*] Exception! exiting"
    client_socket.close()

while True:
    client, addr = server.accept()
    handle_client(client)
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
