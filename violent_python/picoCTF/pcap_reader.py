from scapy.all import *
import dpkt
pcap_file = 'data.pcap'

#a = rdpcap(pcap_file)
#print a
#sessions = a.sessions()
#
#for session in sessions:
#    for packet in sessions[session]:
#        if 'pass' in packet:
#            print packet
f = open(pcap_file)
pcap = dpkt.pcap.Reader(f)

for (ts, buf) in pcap:
    if 'user-agent' in buf.lower():
        print buf


