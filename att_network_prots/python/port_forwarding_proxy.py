import socket
import threading
import sys
import time

sem = threading.Semaphore()

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

def send_and_receive(conn1, conn2):
    buffer = ""
    try:
        while True:
            data = conn1.recv(4096)
            if not data or len(data) < 1:
                break
            conn2.send(data)
            hexdump(data)
            #buffer += data
    except:
        pass
    return buffer


def request_handler(buffer):
    return buffer

def response_handler(buffer):
    return buffer

def proxy_handler(client_socket,remote_socket,receive_first,run_event):
    now = 0
    try:
        while True:
            local_buffer = send_and_receive(client_socket, remote_socket)
            sem.acquire()
            print "[==>] Received %d bytes from local_host." % len(local_buffer)
            #hexdump(local_buffer)
            sem.release()
            if run_event.is_set():
                break
    except Exception as ex:
        sem.acquire()
        print "Exception occured"
        print ex
        sem.release()
        return


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
    client_socket = None
    remote_socket = None
    try:
        while True:
            client_socket, addr = server.accept()

            print "[<==>] Received incoming connection from %s:%d" %\
                    (addr[0], addr[1])
            remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote_socket.connect((remote_host, remote_port))

            proxy_thread = threading.Thread(
                    target=proxy_handler,
                    args=(client_socket,remote_socket,receive_first,run_event)
                    )
            proxy_thread.start()
            remote_buffer = send_and_receive(remote_socket, client_socket)
            sem.acquire()
            print "[<==] Received %d bytes from remote_host." % len(remote_buffer)
            #hexdump(remote_buffer)
            sem.release()

    except KeyboardInterrupt:
        print("[*] Shutting down all connections...")
        run_event.clear()
        if proxy_thread:
            proxy_thread.join()
        if remote_socket:
            remote_socket.close()
            client_socket.close()
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

    server_loop(local_host, local_port, remote_host, remote_port, receive_first)

if __name__=='__main__':
    main(sys.argv)
