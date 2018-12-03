import java.net.*;
import java.util.Date;
import java.util.logging.*;
import java.io.*;

public class UdpClient {
    public static void main(String[] args) {
        try (DatagramSocket socket = new DatagramSocket(0)) {
            socket.setSoTimeout(3000);
            DatagramPacket req = new DatagramPacket(new byte[1], 1, InetAddress.getByName("localhost"), 6656);
            DatagramPacket res = new DatagramPacket(new byte[1024], 1024);
            socket.send(req);
            socket.receive(res);
            System.out.println(new String(res.getData(), 0, res.getLength(), "US-ASCII"));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
