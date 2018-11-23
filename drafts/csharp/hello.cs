using System;
using System.Runtime.InteropServices;
public struct pcap_pkthdr {
    [MarshalAsAttribute(UnmanagedType.ByValTStr, SizeConst = 16)]
    public string ts;
    public uint caplen;
    public uint len;
    [MarshalAsAttribute(UnmanagedType.ByValTStr, SizeConst = 32)]
    public string comment;
}

public class mardas {
    [DllImport("/usr/lib/libpcap.dylib")]
    public static extern string pcap_lookupdev(char[] device);
    public static extern long  pcap_open_live(string device, int size, int a, int b, char[] errbuf);
    public static extern char[] pcap_next(long pcap_handle, pcap_pkthdr header);
    //public static extern void printf(string text);

    public static void Main(string[] args) {
        Console.WriteLine("mardas");
        char[] errbuf = new char[32];
        string device = pcap_lookupdev(errbuf);
        if (device == null) {
            Console.WriteLine(new string(errbuf));
            return;
        }
        Console.WriteLine(device);
    }
}
