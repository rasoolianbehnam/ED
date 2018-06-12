import pxssh
def send_command(s, cmd):
    s.sendline(cmd)
    s.prompt()
    print s.before

def connect(host, user, password):
    try:
        s = pxssh.pxssh()
        s.login(host, user, password)
        return s
    except:
        print '[-] Error Connecting'
        exit(0)

s = connect('127.0.0.1', 'mardas', 'fuckthisshit2')
while True:
    command = raw_input("<BHP#> ")
    send_command(s, command)
