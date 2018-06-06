import dpkt
import sys
import socket

def printPcap(pcap):
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            print '[+] Src: %s --> Dst: %s' % (src, dst)
        except:
            pass

def main():
    try:
        f = open(sys.argv[1])
        pcap = dptk.pcab.Reader(f)
    except Exception, e:
        print '[!] Error opening pcap file.'
        print e
        return
    
    printPcap(pcap)

if __name__=='__main__':
    main()
