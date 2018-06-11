from scapy.all import *

def find_syn(p):
    flags = p.sprintf("%TCP.flags%")
    if flags == 'S':
        p_ip = p[IP]
        p_tcp = p[TCP]
        i = IP()
        t = TCP()
        i.dst = p_ip.src
        i.src = p_ip.dst
        t.sport = p_tcp.dport
        t.dport = p_tcp.sport
        t.flags = "SA"
        t.seq = p_tcp.ack
        t.ack = p_tcp.seq + 1
        print "SYS/ACK sent to %s:%s"%(i.dst, t.dport)
        send(i/t)
sniff(prn=find_syn)
        
