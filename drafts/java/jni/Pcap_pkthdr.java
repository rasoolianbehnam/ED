import com.sun.jna.Library;
import com.sun.jna.Native;
import com.sun.jna.Platform;
import com.sun.jna.Structure;
import java.util.Arrays;
import java.util.ArrayList;
import java.util.List;

public class Pcap_pkthdr extends Structure {
    public static class ByReference extends Pcap_pkthdr implements Structure.ByReference {}
    public static class ByValue extends Pcap_pkthdr implements Structure.ByValue {}
    public char[] comment = new char[256];
    public int len;
    public int caplen;
    public byte[] ts = new byte[16];
    //public Pcap_pkthdr() {
    //    ts = new byte[16];
    //    comment = new char[256];
    //}
    public final List getFieldOrder() {
        List fields = new ArrayList(super.getFieldOrder());
        fields.addAll(Arrays.asList(new String[] {"ts", "caplen", "len", "comment"}));
        return fields;
    }
}


