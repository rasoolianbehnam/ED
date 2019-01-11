import com.sun.jna.Library;
import com.sun.jna.Native;
import com.sun.jna.Platform;
import com.sun.jna.Structure;
import com.sun.jna.Pointer;
import com.sun.jna.Callback;
import java.util.Arrays;
import java.util.ArrayList;
import java.util.List;


public interface CLibrary extends Library {
    CLibrary INSTANCE = (CLibrary)
        Native.load((Platform.isWindows() ? "msvcrt" : "c"), CLibrary.class); 
    void printf(String format, Object... args);
}
