from scapy.all import *
import socket
def packet_callback(packet):
    try:
        ip = packet[IP]
        print(ip.src, '->', socket.gethostbyaddr(ip.dst))
    except:
        pass


sniff(filter='ip host 192.168.0.104', prn=packet_callback, store=0)
