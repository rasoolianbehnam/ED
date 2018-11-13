import java.net.*;
public class Test {
    public static void main(String[] args) throws UnknownHostException {
        InetAddress address = InetAddress.getByName("8.8.8.8");
        System.out.println(address.getHostName());
        System.out.println(InetAddress.getLocalHost());
    }
}
