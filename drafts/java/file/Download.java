import java.net.*;
import java.io.*;
public class Download {
    public static void main(String[] args) {
        try {
            File output = new File("google.html");
            BufferedOutputStream fos= new BufferedOutputStream(
                    new FileOutputStream(output));
            URL url = new URL("https://www.google.com");
            //URLConnection connection = url.openConnection();
            InputStream result = new BufferedInputStream(
                    url.openStream());
            StringBuilder sb = new StringBuilder();
            int input;
            while ((input = result.read()) != -1) {
                sb.append((char) input);
                fos.write(input);
            }
            System.out.println(sb);

        }
        catch(MalformedURLException e) {
           System.out.println("[!] Malformed URL"); 
        }
        catch(IOException e) {
           System.out.println("[!] Cannot open connection!"); 
           e.printStackTrace();
        }
    }
}
