import com.sun.jna.Library;
import com.sun.jna.Native;
import com.sun.jna.Platform;
import com.sun.jna.Structure;
import java.util.Arrays;
import java.util.ArrayList;
import java.util.List;
import com.sun.jna.Pointer;

public class Pcap_pkthdr extends Structure {
    public static class ByReference extends Pcap_pkthdr implements Structure.ByReference {}
    public static class ByValue extends Pcap_pkthdr implements Structure.ByValue {}
    public int len;
    public int caplen;
    public byte[] ts = new byte[16];
    //public Pcap_pkthdr() {
    //    ts = new byte[16];
    //    comment = new char[256];
    //}
    public Pcap_pkthdr() {
        super();
    }
    public Pcap_pkthdr(Pointer p) {
        super(p);
        ts      = p.getByteArray(0, 16);
        caplen  = p.getInt(16);
        len     = p.getInt(20);
    }
    public final List<String> getFieldOrder() {
        List<String> fields = new ArrayList<String>(super.getFieldOrder());
        fields.addAll(Arrays.asList(new String[] {"ts", "caplen", "len"}));
        return fields;
    }
}


