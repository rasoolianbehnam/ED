import com.sun.jna.Library;
import com.sun.jna.Native;
import com.sun.jna.Platform;
import com.sun.jna.Structure;
import com.sun.jna.Pointer;
import com.sun.jna.Callback;

public class HelloWorld {
    public interface CLibrary extends Library {
        CLibrary INSTANCE = (CLibrary)Native.loadLibrary("pcap", CLibrary.class);
        interface Cback extends Callback {
            int invoke(Pointer handle, Pcap_pkthdr header, Pointer packet);
        }
        String pcap_lookupdev(char[] device);
        Pointer pcap_open_live(String device, int size, int a, int b, char[] errbuf);
        String pcap_next(Pointer pcap_handle, Pcap_pkthdr header);
        void pcap_loop(Pointer pcap_handle, int num, Cback Mardas, String mardas);
        void pcap_close(Pointer pcap_handle);
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
        //Pcap_pkthdr header = new Pcap_pkthdr();
        //System.out.println(header.getFieldList());
        //char packet[];
        //String packet;
        //for (int i=0 ; i < 3; i++) {
        //    try {
        //        packet = CLibrary.INSTANCE.pcap_next(pcap_handle, header);
        //        if (packet == null) {
        //            System.out.println("mardas");
        //        } else {
        //        System.out.printf("Got a %d char packet\n", header.len);
        //        System.out.println(new String(packet));
        //        //System.out.println(new String(packet));
        //        }
        //    } catch (Exception e) {
        //        System.out.println("error");
        //        e.printStackTrace();
        //    }
        //}

        CLibrary.Cback myCback = new CLibrary.Cback() {
        //    public int invoke(Pointer handle, Pointer header, Pointer pkt) {
        //        Pcap_pkthdr h = new Pcap_pkthdr(header);
        //        int len = h.len;
        //        System.out.printf("Got a %d char packet\n", len);
        //        for (int i=0; i < len; i++) {
        //            System.out.printf("%02x",  pkt.getByte(i));
        //            if (i%16==0) System.out.println();
        //        }
        //        System.out.println("\n****************");
        //        return 0;
        //    }

            public int invoke(Pointer handle, Pcap_pkthdr header, Pointer pkt) {
                int len = header.len;
                StringBuilder sb = new StringBuilder();
                System.out.printf("Got a %d char packet\n", len);
                byte b;
                for (int i=0; i < len; i++) {
                    b = pkt.getByte(i);
                    sb.append((char) (b < 0 ? b + 256 : b));
                    System.out.printf("%02x", b);
                    if (i%16==0) {
                        System.out.println(" | " + sb);
                        sb = new StringBuilder();
                    }
                }
                System.out.println("\n****************");
                return 0;
            }
        };
        CLibrary.INSTANCE.pcap_loop(pcap_handle, 0, myCback, null);
        CLibrary.INSTANCE.pcap_close(pcap_handle);
        System.out.println("Successfully closed!");
    }
}
