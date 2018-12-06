import java.util.concurrent.*;
import java.net.*;
import java.io.*;
public class PortForwardingProxy {
    public final static int THREAD_COUNT = 4;
    public static int sendAndReceive(InputStream clientIn, OutputStream remoteOut, String message) {
        byte[] request = new byte[1024];
        int bytesRead;
        int totalBytesRead = 0;
        System.out.println(message);
        try {
            while ((bytesRead = clientIn.read(request)) > 0) {
                remoteOut.write(request, 0, bytesRead);
                remoteOut.flush();
                totalBytesRead += bytesRead;
                System.out.println(new String(request));
            }
        } catch (IOException e) {
            System.out.println("Cannot read or write");
            e.printStackTrace();
        }
        System.out.println("finished");
        return totalBytesRead;
    }
    private static class ReadWrite extends Thread{
        InputStream clientIn;
        OutputStream remoteOut;
        public ReadWrite(InputStream clientIn, OutputStream remoteOut) {
            this.clientIn = clientIn;
            this.remoteOut = remoteOut;
        }
        public void run() {
            sendAndReceive(clientIn, remoteOut, "nothing");
        }
    }
    private static class MyThread implements Runnable {
        Socket client;
        String remoteAddress;
        int remotePort;
        public MyThread(Socket client, String remoteAddress, int remotePort) {
            this.client = client;
            this.remoteAddress = remoteAddress;
            this.remotePort = remotePort;
        }
        public void run() {
        }
    }
    public static void main(String args[]) {
        //String bind_address = args[0];
        int bind_port = Integer.parseInt(args[0]);
        String remoteAddress = args[1];
        int remotePort = Integer.parseInt(args[2]);
        ExecutorService pool = Executors.newFixedThreadPool(THREAD_COUNT);
        try (ServerSocket server = new ServerSocket(bind_port)) {
            System.out.println("Successfully connected to " + bind_port + ".");
            while (true) {
                try (Socket client = server.accept()) {
                    System.out.printf(
                            "Received a connection from %s\n",
                            client.getRemoteSocketAddress());
                    //pool.submit(new MyThread(client, remoteAddress, remotePort));
            try (Socket remote = new Socket(remoteAddress, remotePort)) {
                InputStream clientIn, remoteIn;
                OutputStream clientOut, remoteOut;
                try {
                    clientIn = new BufferedInputStream(client.getInputStream());
                } catch (IOException e) {
                    System.out.println("Cannot get input stream from client");
                    e.printStackTrace();
                    return;
                }
                try {
                    remoteIn = new BufferedInputStream(remote.getInputStream());
                } catch (IOException e) {
                    System.out.println("Cannot get input stream from client");
                    e.printStackTrace();
                    return;
                }
                try {
                    clientOut = new BufferedOutputStream(client.getOutputStream());
                } catch (IOException e) {
                    System.out.println("Cannot get input stream from client");
                    e.printStackTrace();
                    return;
                }
                try {
                    remoteOut = new BufferedOutputStream(remote.getOutputStream());
                } catch (IOException e) {
                    System.out.println("Cannot get input stream from client");
                    e.printStackTrace();
                    return;
                }
                System.out.println("mardas");
                ReadWrite t = new ReadWrite(remoteIn, clientOut);
                t.start();
                sendAndReceive(clientIn, remoteOut, "nothing");

            } catch (IOException e) {
                System.out.println("Problem connecting to remote.");
            }
                } catch (IOException e) {
                    System.out.println("problem Accepting");
                }
            }
        } catch (IOException e) {
                e.printStackTrace();
        }
        pool.shutdown();
    }
}
