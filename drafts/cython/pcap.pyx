#from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free
#from libc.stdlib cimport malloc, free
cdef extern from "pcap.h":
    ctypedef unsigned char u_char
    ctypedef struct pcap_t:
        pass
    ctypedef struct pcap_pkthdr:
        char ts[16]
        unsigned int caplen
        unsigned int len
    char *pcap_lookupdev(char *err);
    pcap_t *pcap_open_live(const char * device, 
            int length, int a, int b, char *err);
    const u_char* pcap_next(pcap_t *handle, pcap_pkthdr *header)
    #int pcap_loop(pcap_t* pcap_handle, 
    #        int num_loops, pcap_handler handler, unsigned char *err);

cdef class Pcap:
    def __cint__(self):
        pass
    cdef main(self):
        cdef pcap_pkthdr *header
        #header = <mardas> malloc(sizeof(pcap_pkthdr))
        #sizeof(pcap_pkthdr)
        cdef const unsigned char *packet
        cdef char errbuff[100]
        cdef char *device
        cdef pcap_t *pcap_handle
        device = pcap_lookupdev(errbuff)
        if device is NULL:
            print("pcap_lookupdev")
        print("Sniffing on device %s\n"%device)
        pcap_handle = pcap_open_live(device, 4096, 1, 0, errbuff)
        if pcap_handle is NULL:
            print("pcap_open_live %s", errbuff)

        for i in range(3):
            print i
            packet = pcap_next(pcap_handle, header)
