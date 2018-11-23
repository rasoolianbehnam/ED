[StructLayout(LayoutKind.Sequential)]
public struct pcap_pkthdr {
    int ts; /* time stamp */
    uint caplen; /* length of portion present */
    uint len; /* length this packet (off wire) */
    [MarshalAs(UnmanagedType.LPStr, SizeConst = 256)]
    string comment;
};


