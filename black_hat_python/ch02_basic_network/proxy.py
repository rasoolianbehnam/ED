import socket
import sys
import threading
import time

def receive_from(connection):
    buffer = ""
    connection.settimeout(5)
    try:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            buffer += data
    except Exception as e:
        print("[!!!] Exception!")
        print(e)
    return buffer

def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, unicode) else 2
    for i in xrange(0, len(src), length):
        s = src[i:i+length]
        hexa = b' '.join(["%0*X" % (digits, ord(x)) for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append( b"%04X    %-*s    %s" % (i, length*(digits + 1),\
                hexa, text))
    print b'\n'.join(result)

def response_handler(response):
    return response

def request_handler(request):
    return request


def proxy_handler(client_socket, remote_host, remote_port, receive_first, run_event):

    now = 0
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    if receive_first:
        print "[*] Receiving from remote"
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)
        remote_buffer = response_handler(remote_buffer)
        
        if len(remote_buffer):
            print "[<==] Sending %d bytes to localhost." % len(remote_buffer)
            client_socket.send(remote_buffer)
    while True:
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            now = 0
            print "[==>] Received %d bytes from localhost." % len(local_buffer)
            hexdump(local_buffer)
            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print "[==>] Sent to remote."

        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            now = 0
            print "[<==] Received %d bytes from remote." % len(remote_buffer)
            hexdump(remote_buffer)
            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print "[<==] Sent to localhost."
        if not len(local_buffer) or not len(remote_buffer) or not run_event.is_set():
            if not now:
                now = time.time()
            else:
                if (time.time() - now) > 30:
                    client_socket.close()
                    remote_socket.close()
                    print "[*] No more data. Closing connections."
                    break


def server_loop(local_host,local_port,remote_host,remote_port,receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except:
        print "[!!] Failed to listen on %s:%d" % (local_host,local_port)
        print "[!!] Check for other listening sockets or correct permissions."
    server.listen(5)
    run_event = threading.Event()
    run_event.set()
    proxy_thread = None
    try:    
        while True:
            client_socket, addr = server.accept()
            # print out the local connection information
            print "[==>] Received incoming connection from %s:%d"%(addr[0],addr[1])
            proxy_thread = threading.Thread(target=proxy_handler, \
                    args=(client_socket, remote_host, remote_port, receive_first,run_event))
            proxy_thread.start()
    except KeyboardInterrupt:
        run_event.clear()
        if proxy_thread:
            proxy_thread.join()

def main():
    # no fancy command-line parsing here
    if len(sys.argv[1:]) != 5:
        print "Usage: ./proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]"
        print "Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True"
        sys.exit(0)
    # setup local listening parameters
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    # setup remote target
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    # this tells our proxy to connect and receive data
    # before sending to the remote host
    receive_first = sys.argv[5]
    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False
    # now spin up our listening socket
    server_loop(local_host,local_port,remote_host,remote_port,receive_first)

if __name__=="__main__":
    main()
