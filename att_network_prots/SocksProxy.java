import java.io.*;
import java.net.*;
public class SocksProxy {
    public static void main(String args[]) throws IOException{
        int port = Integer.parseInt(args[0]);
        try (ServerSocket server = new ServerSocket(port)) {
            System.out.println("Successfully bound to port " + port + ".");
            Socket request = server.accept();
            System.out.println(request.getRemoteSocketAddress());
            InputStream in = request.getInputStream();
            byte[] buffer = new byte[1024];
            int bytesRead;
            while ((bytesRead = in.read(buffer)) > 0) {
                System.out.println(buffer);
            }
        } catch (IOException e) {
            System.out.println("Server cannot bind");
            e.printStackTrace();
        }
    }
}
