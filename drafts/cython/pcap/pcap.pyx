from __future__ import print_function
from libpcap cimport *
import ipaddress

#from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free
#from libc.stdlib cimport malloc, free
cdef char* inet_ntoa(unsigned char address[4]):
    cdef int i
    out = ""
    for i in address[:4]:
        if i < 0:
            i += 256
        out += "%d."%i
    return out[:-1]

cdef char* eth_to_str(unsigned char address[6]):
    cdef int i
    out = ""
    for i in address[:6]:
        if i < 0:
            i += 256
        out += "%02x:"%i
    return out[:-1]

cdef void pcap_handler_cb (u_char * args, const pcap_pkthdr *header, const u_char *packet):
    print("Received packet of size %d"%header.len)
    if header is not NULL:
        print("Got a packet of length %d"%header.len)
    else:
        print("This is odd! header is null")
        return
    if packet is not NULL:
        eth = <Ethernet *> packet;
        print("Ethernet src: %s"%(eth_to_str(eth.ether_src_addr)), end='\t')
        print("Ethernet dst: %s"%(eth_to_str(eth.ether_dst_addr)))
        
        ip = <Ip *>(packet + 14)
        print("IP src: %s"%inet_ntoa(ip.ip_src_addr), end='')
        print("\t", end='')
        print("IP dst: %s"%inet_ntoa(ip.ip_dest_addr), end='')
        print()
    else:
        print("This is odd! Packet is null.")

cdef class Pcap:
    def __cint__(self):
        pass
    cpdef main(self):
        cdef pcap_pkthdr header
        cdef const u_char *packet
        cdef char errbuff[100]
        cdef char *device
        cdef pcap_t *pcap_handle
        cdef Ethernet *eth;
        cdef Ip *ip;
        cdef int i, j
        device = pcap_lookupdev(errbuff)
        if device is NULL:
            print("Problem at pcap_lookupdev: %s"%errbuff)
        print("Sniffing on device %s\n"%device)
        pcap_handle = pcap_open_live(device, 4096, 1, 0, errbuff)
        if pcap_handle is NULL:
            print("pcap_open_live %s"%errbuff)

        #for i in range(15):
        #    print(i)
        #    packet = pcap_next(pcap_handle, &header)
        #    print("Got a packet of length %d"%header.len)
        #    if packet is not NULL:
        #        eth = <Ethernet *> packet;
        #        print("Ethernet src: %s"%(eth_to_str(eth.ether_src_addr)), end='\t')
        #        print("Ethernet dst: %s"%(eth_to_str(eth.ether_dst_addr)))
        #        
        #        ip = <Ip *>(packet + 14)
        #        print("IP src: %s"%inet_ntoa(ip.ip_src_addr), end='')
        #        print("\t", end='')
        #        print("IP dst: %s"%inet_ntoa(ip.ip_dest_addr), end='')
        #        print()
        #    else:
        #        print("This is odd! Packet is null.")

        pcap_loop(pcap_handle, 15, pcap_handler_cb, NULL)
