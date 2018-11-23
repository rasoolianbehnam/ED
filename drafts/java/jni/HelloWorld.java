import com.sun.jna.Library;
import com.sun.jna.Native;
import com.sun.jna.Platform;
import com.sun.jna.Structure;
import com.sun.jna.Pointer;

public class HelloWorld {
    public interface CLibrary extends Library {
        CLibrary INSTANCE = (CLibrary)Native.loadLibrary("pcap", CLibrary.class);
        String pcap_lookupdev(char[] device);
        Pointer pcap_open_live(String device, int size, int a, int b, char[] errbuf);
        char[] pcap_next(Pointer pcap_handle, Pcap_pkthdr header);
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
            System.out.println("pcap_open_live: " + buff);
            System.exit(0);
        }
        System.out.println("Success fully opened pcap with pointer: " + pcap_handle);
        Pcap_pkthdr header = new Pcap_pkthdr();
        //System.out.println(header.getFieldList());
        char packet[];
        for (int i=0 ; i < 3; i++) {
            try {
                //packet = CLibrary.INSTANCE.pcap_next(pcap_handle, header);
                //System.out.printf("Got a %d byte packet\n", header.len);
                //System.out.println(new String(packet));
            } catch (Exception e) {
                System.out.println("error");
            }
        }
    }
}
