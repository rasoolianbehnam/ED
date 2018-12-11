ctypedef unsigned char u_char
ctypedef struct pcap_pkthdr:
    char ts[16]
    unsigned int caplen
    unsigned int len

ctypedef struct Ethernet:
    u_char ether_src_addr[6]
    u_char ether_dst_addr[6]
    unsigned short ether_type

ctypedef struct Ip:
    unsigned char ip_version_and_header_length;
    unsigned char ip_tos;
    unsigned short ip_len; 
    unsigned short ip_id;
    unsigned short ip_frag_offset; 
    unsigned char ip_ttl;
    unsigned char ip_type;
    unsigned short ip_checksum;
    unsigned char ip_src_addr[4]
    unsigned char ip_dest_addr[4]

ctypedef void (*pcap_handler) (u_char * args, const pcap_pkthdr *header, const u_char *packet)

cdef extern from "pcap.h":
    ctypedef struct pcap_t:
        pass
    char *pcap_lookupdev(char *err);
    pcap_t *pcap_open_live(const char * device, 
            int length, int a, int b, char *err);
    const u_char* pcap_next(pcap_t *handle, pcap_pkthdr *header)
    int pcap_loop(pcap_t *handle, int num_packets, pcap_handler callback, u_char *args);

