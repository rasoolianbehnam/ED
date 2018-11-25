import com.sun.jna.Library;
import com.sun.jna.Native;
import com.sun.jna.Platform;
import com.sun.jna.Structure;
import com.sun.jna.Pointer;
import com.sun.jna.Callback;
import java.util.Arrays;
import java.util.ArrayList;
import java.util.List;


public class DecodeSniff {
    public interface CLibrary extends Library {
        CLibrary INSTANCE = (CLibrary)Native.loadLibrary("pcap", CLibrary.class);
        interface Cback extends Callback {
            int invoke(Pointer handle, Pcap_pkthdr_apple header, Pointer packet);
        }
        String pcap_lookupdev(char[] device);
        Pointer pcap_open_live(String device, int size, int a, int b, char[] errbuf);
        Pointer pcap_next(Pointer pcap_handle, Pcap_pkthdr_apple header);
        void pcap_loop(Pointer pcap_handle, int num, Cback Mardas, String mardas);
        void pcap_close(Pointer pcap_handle);
    }
    public static class Pcap_pkthdr extends Structure {
        public static class ByValue extends Pcap_pkthdr implements Structure.ByValue { }
        public int len;
        public int caplen;
        public byte[] ts = new byte[16];
        public List<String> getFieldOrder() {
            List<String> fields = new ArrayList<String>(super.getFieldOrder());
            fields.addAll(Arrays.asList(new String[] {"ts", "caplen", "len"}));
            return fields;
        }
    }

    public static class Pcap_pkthdr_apple extends Pcap_pkthdr {
        public byte[] comment = new byte[256];
        public final List<String> getFieldOrder() {
          List<String> fields = new ArrayList<String>(super.getFieldOrder());
            fields.addAll(Arrays.asList(new String[] {"comment"}));
            return fields;
        }
    }

    public static class eth_hdr extends Structure {
        private static final int ETH_ALEN = 6;
        public static final int  ETH_HLEN = 14;
        public byte h_dest[] = new byte[ETH_ALEN];
        public byte h_source[] = new byte[ETH_ALEN];
        public short h_proto;

        public eth_hdr() {super();};
        public eth_hdr(Pointer p) {
            super(p);
            h_dest = p.getByteArray(0, ETH_ALEN);
            h_source = p.getByteArray(ETH_ALEN, ETH_ALEN);
            h_proto = p.getShort(2*ETH_ALEN);
        };


        public final List<String> getFieldOrder() {
            List<String> fields = new ArrayList<String>(super.getFieldOrder());
            fields.addAll(Arrays.asList(new String[] {"h_dest", "h_source", "h_proto"}));
            return fields;
        }
    }

    public static class ip_hdr extends Structure {
        public byte ip_version_and_header_length; // Version and header length
        public byte     ip_tos;
        public short    ip_len; 
        public short    ip_id;
        public short    ip_frag_offset; 
        public byte     ip_ttl;
        public byte     ip_type; 
        public short    ip_checksum; 
        public byte     ip_src_addr[] = new byte[4]; 
        public byte     ip_dest_addr[] = new byte[4];
        public ip_hdr(Pointer p, long offset) { 
            super(p); 
            ip_version_and_header_length = p.getByte(offset+0);
            ip_tos = p.getByte(offset+1);
            ip_len = p.getShort(offset+2); 
            ip_id  = p.getShort(offset+4);
            ip_frag_offset = p.getShort(offset+6); 
            ip_ttl = p.getByte(offset+8);
            ip_type = p.getByte(offset+9); 
            ip_checksum = p.getShort(offset+10); 
            ip_src_addr = p.getByteArray(offset+12, 4); 
            ip_dest_addr = p.getByteArray(offset+16, 4); 
        }

        public final    List<String> getFieldOrder() {
            List<String> fields = new ArrayList<String>(super.getFieldOrder());
            fields.addAll(Arrays.asList(new String[] {"ip_version_and_header_length", "ip_tos",
            "ip_len", "ip_id", "ip_frag_offset", "ip_ttl", "ip_type", "ip_checksum", "ip_src_addr", "ip_dest_addr"}));
            return fields;
        }

    };
    public static class tcp_hdr extends Structure {
        public static final int TCP_FIN     = 0x01;
        public static final int TCP_SYN     = 0x02;
        public static final int TCP_RST     = 0x04;
        public static final int TCP_PUSH    = 0x08;
        public static final int TCP_ACK     = 0x10;
        public static final int TCP_URG     = 0x20;
        public byte[]   tcp_src_port  = new byte[2];
        public byte[]   tcp_dest_port = new byte[2];
        public int     tcp_seq;
        public int     tcp_ack;
        public byte    reserved_and_tcp_offset;
        public byte    tcp_flags;
        public short   tcp_window;
        public short   tcp_checksum;
        public short   tcp_urgent;
        public tcp_hdr(Pointer p, long offset) {
            super(p);
            tcp_src_port = p.getByteArray(offset, 2);
            tcp_dest_port = p.getByteArray(offset+2, 2);
            tcp_seq = p.getInt(offset+4);
            tcp_ack = p.getInt(offset+8);
            reserved_and_tcp_offset = p.getByte(offset+12);
            tcp_flags = p.getByte(offset+13);
            tcp_window = p.getShort(offset+14);
            tcp_checksum = p.getShort(offset+16);
            tcp_urgent = p.getShort(offset+18);
        }
        public final List<String> getFieldOrder() {
            List<String> fields = new ArrayList<String>(super.getFieldOrder());
            String additionalFields[] = new String[] { "tcp_src_port", 
                "tcp_dest_port", 
                "tcp_seq", 
                "tcp_ack", 
                "reserved_and_tcp_offset", 
                "tcp_flags", 
                "tcp_window", 
                "tcp_checksum", 
                "tcp_urgent"};
            fields.addAll(Arrays.asList(additionalFields));
            return fields;
        }
    }

    public static void main(String args[]) {
        char buff[] = new char[100];
        String device = CLibrary.INSTANCE.pcap_lookupdev(buff);
        if (device == null) {
            System.out.println("pcap_lookup: " + (new String(buff)));
            System.exit(0);
        }
        System.out.println("Sniffing on device " + device);
        Pointer pcap_handle = CLibrary.INSTANCE.pcap_open_live(device, 4096, 1, 0, buff);
        if (pcap_handle == null) {
            System.out.println("pcap_open_live: " + (new String(buff)));
            System.exit(0);
        }
        System.out.println("Success fully opened pcap with pointer: " + pcap_handle);
        Pcap_pkthdr_apple header = new Pcap_pkthdr_apple();
        //System.out.println(header.getFieldList());
        //char packet[];
        Pointer packet;
        for (int i=0 ; i < 3; i++) {
            try {
                packet = CLibrary.INSTANCE.pcap_next(pcap_handle, header);
                if (packet == null) {
                    System.out.println("mardas");
                } else {
                System.out.printf("Got a %d char packet\n", header.len);
                //System.out.println(new String(packet));
                //System.out.println(new String(packet));
                }
            } catch (Exception e) {
                System.out.println("error");
                e.printStackTrace();
            }
        }

        CLibrary.Cback myCback = new CLibrary.Cback() {
        //    public int invoke(Pointer handle, Pointer header, Pointer pkt) {
        //        Pcap_pkthdr_apple h = new Pcap_pkthdr_apple(header);
        //        int len = h.len;
        //        System.out.printf("Got a %d char packet\n", len);
        //        for (int i=0; i < len; i++) {
        //            System.out.printf("%02x",  pkt.getByte(i));
        //            if (i%16==0) System.out.println();
        //        }
        //        System.out.println("\n****************");
        //        return 0;
        //    }

            public int invoke(Pointer handle, Pcap_pkthdr_apple header, Pointer pkt) {
                int len = header.len;
                StringBuilder sb = new StringBuilder();
                System.out.printf("Got a %d char packet\n", len);
                //Utilities.dump(pkt.getByteArray(0, len));
                Utilities.decode_ether(pkt);
                int ip_header_size = Utilities.decode_ip(pkt);
                int tcp_header_size = Utilities.decode_tcp(pkt);
                int total_header_size = eth_hdr.ETH_HLEN+ip_header_size+tcp_header_size;
                Utilities.dump(pkt, total_header_size, header.len-total_header_size);
                //byte b;
                //for (int i=0; i < len; i++) {
                //    b = pkt.getByte(i);
                //    sb.append((char) (b < 0 ? b + 256 : b));
                //    System.out.printf("%02x ", b);
                //    if (i%16==0) {
                //        System.out.println(" | " + sb);
                //        sb = new StringBuilder();
                //    }
                //}
                //System.out.println("\n****************");
                return 0;
            }
        };
        CLibrary.INSTANCE.pcap_loop(pcap_handle, 0, myCback, null);
        CLibrary.INSTANCE.pcap_close(pcap_handle);
        System.out.println("Successfully closed!");
    }
}
