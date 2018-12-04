cdef extern from "pcap.h":
    ctypedef unsigned char u_char
    ctypedef struct pcap_t:
        pass
    ctypedef struct pcap_pkthdr:
        char ts[16]
        unsigned int caplen
        unsigned int len
    ctypedef pcap_pkthdr* mardas
    char *pcap_lookupdev(char *err);
    pcap_t *pcap_open_live(const char * device, 
            int length, int a, int b, char *err);
    const u_char* pcap_next(pcap_t *handle, pcap_pkthdr *header)
    #int pcap_activate(void* mardas)
    #int pcap_loop(pcap_t* pcap_handle, 
    #        int num_loops, pcap_handler handler, unsigned char *err);
