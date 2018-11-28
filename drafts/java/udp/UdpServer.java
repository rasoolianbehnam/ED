import java.net.*;
import java.util.Date;
import java.util.logging.*;
import java.io.*;

public class UdpServer {
    private final static Logger audit = Logger.getLogger("request");
    private final static Logger errors = Logger.getLogger("errors");
    public static void main(String[] args) {
        try (DatagramSocket socket = new DatagramSocket(6656)) {
            while (true) {
                try {
                DatagramPacket req = new DatagramPacket(new byte[1024], 1024);
                socket.receive(req);
                byte[] data = (new Date()).toString().getBytes("US-ASCII");
                DatagramPacket res = new DatagramPacket(data, data.length, req.getAddress(), req.getPort());
                socket.send(res);
                } catch (IOException e) {
                    errors.log(Level.SEVERE, e.getMessage(), e);
                }
            } 
        } catch (IOException e) {
                errors.log(Level.SEVERE, e.getMessage(), e);
        }
    }
}
