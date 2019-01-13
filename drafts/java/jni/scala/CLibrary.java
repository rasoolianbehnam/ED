import com.sun.jna.Library;
import com.sun.jna.Native;
import com.sun.jna.Platform;
import com.sun.jna.Structure;
import com.sun.jna.Pointer;
import com.sun.jna.Callback;
import java.util.Arrays;
import java.util.ArrayList;
import java.util.List;


//public interface CLibrary extends Library {
//    CLibrary INSTANCE = (CLibrary)
//        Native.load((Platform.isWindows() ? "msvcrt" : "c"), CLibrary.class); 
//    void printf(String format, Object... args);
//}

public interface CLibrary extends Library {
    CLibrary INSTANCE = (CLibrary)Native.loadLibrary("pcap", CLibrary.class);
    //interface Cback extends Callback {
    //    int invoke(Pointer handle, Pcap_pkthdr header, Pointer packet);
    //}
    String pcap_lookupdev(char[] device);
    Pointer pcap_open_live(String device, int size, int a, int b, char[] errbuf);
    //Pointer pcap_next(Pointer pcap_handle, Pcap_pkthdr header);
    //void pcap_loop(Pointer pcap_handle, int num, Cback Mardas, String mardas);
    //void pcap_close(Pointer pcap_handle);
}
