import com.sun.jna.*;
import java.util.*;
import java.net.*;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.lang.*;

public class Utilities {
    public static ByteBuffer ntohs(byte pkt[]) {
        ByteBuffer buff = ByteBuffer.wrap(pkt);
        buff.order(ByteOrder.BIG_ENDIAN);
        return buff;
    }
    public static int getUnsigned(int a, int numBytes) {
        return a < 0 ? a + (1 << numBytes*8) : a;
    }
    public static void dump(byte[] pkt) {
        byte b;
        StringBuilder sb = new StringBuilder();
        int i;
        for (i=0; i < pkt.length; i++) {
            b = pkt[i];
            if ((b > 31) && (b < 127))
                sb.append((char) b);
            else sb.append(".");
            //sb.append((char) (b < 0 ? b + 256 : b));
            System.out.printf("%02x ", b);
            if (i%16==15) {
                System.out.println("| " + sb);
                sb = new StringBuilder();
            }
        }
        while (i % 16 != 15) {
            System.out.print("   ");
            i++;
        }
        System.out.println("   | " + sb);
        System.out.println();
    }
    public static void dump(Pointer p, int offset, int len) {
        byte pkt[] = p.getByteArray(offset, len);
        dump(pkt);
    }
    public static void decode_ether(Pointer p) {
        DecodeSniff.eth_hdr handle = new DecodeSniff.eth_hdr(p);
        System.out.println("[[ Layer 2 :: Ethernet Header ]]");
        System.out.print("[ Source: ");
        int i;
        for (i=0; i < handle.h_source.length-1; i++) 
            System.out.printf("%02x:", handle.h_source[i]);
        System.out.printf("%02x", handle.h_source[i]);
        System.out.print("    Destination: ");
        for (i=0; i < handle.h_dest.length-1; i++) 
            System.out.printf("%02x:", handle.h_dest[i]);
        System.out.printf("%02x", handle.h_dest[i]);
        System.out.print("    Type: ");
        System.out.println(handle.h_proto + " ]");
    }
    public static int decode_ip(Pointer p) {
        DecodeSniff.ip_hdr handle = new DecodeSniff.ip_hdr(p, DecodeSniff.eth_hdr.ETH_HLEN);
        try {
            InetAddress src_address = InetAddress.getByAddress(handle.ip_src_addr);
            InetAddress dst_address = InetAddress.getByAddress(handle.ip_dest_addr);
            System.out.printf("\t(( Layer 3 ::: IP Header ))\n");
            System.out.printf("\t( Source: %s\t", src_address.getHostAddress());
            System.out.printf("Dest: %s )\n", dst_address.getHostAddress());
            System.out.printf("\t( Type: %d\t", (int) handle.ip_type < 0 ? handle.ip_type + 256 : handle.ip_type);
            System.out.printf("ID: %d\tLength: %d )\n", handle.ip_id < 0 ? handle.ip_id + 65536 : handle.ip_id, 
                    handle.ip_len < 0 ? handle.ip_len + 65536 : handle.ip_len);
        } catch (UnknownHostException e) {
            System.out.println("Host not valid");
        }
        return handle.size();
    }
    public static int decode_tcp(Pointer p) {
        DecodeSniff.ip_hdr ip_header = new DecodeSniff.ip_hdr(p, DecodeSniff.eth_hdr.ETH_HLEN);
        DecodeSniff.tcp_hdr tcp_header = new DecodeSniff.tcp_hdr(p, DecodeSniff.eth_hdr.ETH_HLEN+ip_header.size());
        short srcPort = ntohs(tcp_header.tcp_src_port).getShort();
        short dstPort = ntohs(tcp_header.tcp_dest_port).getShort();
        int  header_size = 4 * getUnsigned(tcp_header.reserved_and_tcp_offset & 0x0F, 1);
        System.out.printf("\t\t{{ Layer 4 :::: TCP Header }}\n");
        System.out.printf("\t\t{ Src Port: %d\t", getUnsigned(srcPort, 2)); 
        System.out.printf("Dest Port: %d }\n", getUnsigned(dstPort, 2));
        System.out.printf("\t\t{ Seq #: %d\t", Integer.toUnsignedLong(tcp_header.tcp_seq));
        System.out.printf("Ack #: %d }\n", Integer.toUnsignedLong(tcp_header.tcp_ack)); 
        System.out.printf("\t\t{ Header Size: %d\tFlags: ", header_size);
        if((tcp_header.tcp_flags & DecodeSniff.tcp_hdr.TCP_FIN) != 0)  System.out.printf("FIN ");
        if((tcp_header.tcp_flags & DecodeSniff.tcp_hdr.TCP_SYN) != 0)  System.out.printf("SYN ");
        if((tcp_header.tcp_flags & DecodeSniff.tcp_hdr.TCP_RST) != 0)  System.out.printf("RST ");
        if((tcp_header.tcp_flags & DecodeSniff.tcp_hdr.TCP_PUSH) != 0) System.out.printf("PUSH ");
        if((tcp_header.tcp_flags & DecodeSniff.tcp_hdr.TCP_ACK) != 0)  System.out.printf("ACK ");
        if((tcp_header.tcp_flags & DecodeSniff.tcp_hdr.TCP_URG) != 0)  System.out.printf("URG ");
        System.out.println();
        return header_size;
    }

}
