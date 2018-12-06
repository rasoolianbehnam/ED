import socket
import threading
import sys
import time

def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, unicode) else 2
    for i in xrange(0, len(src), length):
        s = src[i:i+length]
        hexa = b' '.join(["%0*X" % (digits, ord(x)) for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append( b"%04X   %-*s  %s" % (i, length*(digits + 1), hexa, text) )
    print b'\n'.join(result)

def receive_from(conn):
    buffer = ""
    conn.settimeout(2)
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            buffer += data
    except:
        pass
    return buffer


def request_handler(buffer):
    return buffer

def response_handler(buffer):
    return buffer

def proxy_handler(client_socket,remote_host,remote_port,receive_first,run_event):
    now = 0
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)
        remote_buffer = response_handler(remote_buffer)
        if len(remote_buffer):
            print "[<==] Sending %d bytes to local_host." %  len(remote_buffer)
            client_socket.send(remote_buffer)
    while True:
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            now = 0
            print "[==>] Received %d bytes from local_host." % len(local_buffer)
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
            print "[<==] Sent to local_host."
        if not len(local_buffer) or not len(remote_buffer) or run_event.is_set():
            if not now:
                now = time.time()
            else:
                if (time.time() - now) > 3:
                    print "[*] No more data. Closing connections."
                    client_socket.close()
                    remote_socket.close()
                    break


def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except:
        print "[!!] Failed to listen on %s:%d" % (local_host,local_port)
        print "[!!] Check for other listening sockets or correct" \
            + "permissions."
        sys.exit(0)
    print "[*] Listening on %s:%d" % (local_host,local_port)
    
    server.listen(5)

    run_event = threading.Event()
    run_event.set()

    proxy_thread = None
    try:
        while True:
            try:
                client_socket, addr = server.accept()
            except Exception as ex:
                if str(ex) == "timed out":
                    continue
                else:
                    sys.exit(0)

            print "[==>] Received incoming connection from %s:%d" %\
                    (addr[0], addr[1])
            proxy_thread = threading.Thread(target=proxy_handler,args=(client_socket,remote_host,remote_port,receive_first,run_event))
            proxy_thread.start()
    except KeyboardInterrupt:
        print("[*] Shutting down all connections...")
        run_event.clear()
        if proxy_thread:
            proxy_thread.join()
        sys.exit()


def main(argv):
    if len(argv) != 6:
        print "Usage: ./proxy.py [local_host] [local_port] [remote_host]" \
              + "[remote_port] [receive_first]"
        print "Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True"
        exit(0)
    local_host     = argv[1]
    local_port     = int(argv[2])
    remote_host    = argv[3]
    remote_port    = int(argv[4])
    receive_first  = argv[5]

    if 'true' in receive_first.lower():
        receive_first = True
    else:
        receive_first = False

    try:
        server_loop(local_host, local_port, remote_host, remote_port, receive_first)
    except KeyboardInterrupt:
        print("[*] Shutting down the proxy...")
        run_event.clear()

if __name__=='__main__':
    main(sys.argv)
