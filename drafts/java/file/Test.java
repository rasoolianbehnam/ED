import java.net.*;
import java.io.*;
public class Test {
    public static void main(String[] args) throws UnknownHostException {
        try {
            URL u = new URL("https://www.google.com");
            System.out.println(u.getProtocol());
            System.out.println(u.getDefaultPort());
            System.out.println(u.getFile());
            System.out.println(u.getAuthority());
            URLConnection uc = u.openConnection();
            uc.setRequestProperty("User-Agent", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0");
            System.out.println(uc);
            //try (InputStreamReader fis = 
            //        new InputStreamReader(u.openStream())) {
            //    int buffer;
            //    while ((buffer = fis.read()) != -1) 
            //        System.out.print((char) buffer);
            //        } catch (IOException e) {
            //            e.printStackTrace();
            //        }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
