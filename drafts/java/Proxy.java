import java.net.*;
import java.io.IOException;
import java.io.OutputStream;
import java.io.InputStream;

public class Proxy {
    public static void main(String[] args) {
        String usage = "java Proxy local_port remote_host remote_port listen_first";
        if (args.length != 4)
            System.out.println(usage);
        int local_port = Integer.parseInt(args[0]);
        String remote_host = args[1];
        int remote_port = Integer.parseInt(args[2]);
        String listen_first = args[3];

        boolean receive_first = false;
        if (listen_first.toLowerCase().trim().contains("true"))
            receive_first = true;
        System.out.printf("%s:%d <-> %s:%d\n(%b)", "localhost", local_port,
                remote_host, remote_port, receive_first);
       Proxy p = new Proxy();
       p.server_loop(local_port, remote_host, remote_port, receive_first);
    }

    public void server_loop(int local_port, String remote_host, int remote_port, boolean receive_first) {
        try {
            ServerSocket server = new ServerSocket(local_port);
            while (true) {
                Socket client_socket = server.accept();
                System.out.printf("[==>] Received incoming connection from %s:%d\n", client_socket.getInetAddress(), client_socket.getPort());
                ProxyThread proxyThread = new ProxyThread(client_socket, remote_host, remote_port, receive_first); 
                proxyThread.start();
                //server.close();
            }
        }
        catch (UnknownHostException e) {
            System.out.printf("[!!] Failed to listen on %s:%d\n", "localhost",local_port);
            System.out.println("[!!] Check for other listening sockets or correct permissions.");
        }
        catch (IOException e) {
            e.printStackTrace();
        }

    }
    private static class ProxyThread extends Thread {
        private Socket socket, remoteSocket;
        private boolean receive_first;
        private OutputStream out, remoteOut;
        private InputStream in, remoteIn;
        public ProxyThread(Socket socketIn, String remote_hostIn, int remote_portIn, boolean receive_firstIn) {
            socket = socketIn;
            receive_first = receive_firstIn;
            try {
                remoteSocket = new Socket(remote_hostIn, remote_portIn);
                log("[*] Remote socket " + remote_hostIn + ":" + remote_portIn + " created");
            }
            catch (IOException e) {
                e.printStackTrace();
            }
        }
        public void run() {
            try {
                in = socket.getInputStream();
                out = socket.getOutputStream();
                remoteIn = remoteSocket.getInputStream();
                remoteOut = socket.getOutputStream();
                if (receive_first) {
                    receiveAndSend(remoteIn, out);
                }
                while (true) {
                    int a = receiveAndSend(in, remoteOut);
                    System.out.printf("%03d bytes read from local buffer\n", a);
                    int b = receiveAndSend(remoteIn, out);
                    System.out.printf("%03d bytes read from remote buffer\n", b);
                    //if (a == 0 && b == 0) break;
                }
            }
            catch (IOException e) {
                e.printStackTrace();
            }
            finally {
                try {
                    log("Closing connections!!");
                    socket.close();
                    remoteSocket.close();
                }
                catch (IOException e) {
                    e.printStackTrace();
                }
            }

            
        return;
        }
    }
    private static void log(String message) {
        System.out.println(message);
    }
    private static int receiveAndSend(InputStream in, OutputStream out) {
        byte[] request = new byte[1024];
        int bytesRead;
        int totalBytesRead = 0;
        try {
            while ((bytesRead = in.read(request)) != -1) {
                out.write(request, 0, bytesRead);
                out.flush();
                totalBytesRead += bytesRead;
            }
        }
        catch (IOException e) {
            log("[!!] Failed to read from socket");
        }
        return totalBytesRead;
    }
}
