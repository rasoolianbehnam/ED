import com.sun.jna.Library;
import com.sun.jna.Native;
import com.sun.jna.Platform;
import com.sun.jna.Structure;
import com.sun.jna.Pointer;
import com.sun.jna.Callback;
import java.util.Arrays;
import java.util.ArrayList;
import java.util.List;

object  Mardas extends App{
    //CLibrary.INSTANCE.printf("Hello, World\n");
    val buff: Array[Char] = new Array[Char](100);
    val device = CLibrary.INSTANCE.pcap_lookupdev(buff);
    println(device)
}


