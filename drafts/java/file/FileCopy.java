import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.ObjectInputStream;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;

public class FileCopy {
    public static void main(String[] args) {
        try {
            //File file = new File("untitled_0_1.odg");
            //File file2 = new File("untitled_0_2.odg");
            FileInputStream fis = new FileInputStream("untitled_0_1.odg");

            FileOutputStream fot = new FileOutputStream("untitled_0_2.odg");
            byte[] buffer = new byte[1024];
            int bytesRead;

            while ((bytesRead = fis.read(buffer)) >= 0) {
                fot.write(buffer, 0, bytesRead);
                fot.flush();
            }
        }
        catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        catch (IOException e) {
            e.printStackTrace();
        }
    }
}
