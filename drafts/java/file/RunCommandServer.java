import java.io.*;
import java.util.*;
import java.io.BufferedWriter;
import java.net.*;

public class RunCommandServer {
    public static class ProcessOutputThread extends Thread {
        BufferedReader processInput;
        PrintStream output;
        public ProcessOutputThread(BufferedReader processInputIn, PrintStream outputIn) {
            this.processInput = processInputIn;
            this.output = outputIn;
        }
        public void run() {
            String s;
            try {
                while ((s = processInput.readLine()) != null) {
                    synchronized (output) {
                        output.println(s);
                        //System.out.notify();
                    }
                }
            }
            catch (IOException e) {
                synchronized (output) {
                    output.println("Conection Closed;");
                }
                    //e.printStackTrace();
            }
            finally {
                try {
                    processInput.close();
                }
                catch (IOException e) {
                    output.println("Output stream Could not be Closed;");
                    //e.printStackTrace();
                }
            }
            Thread.currentThread().interrupt();
            return;
        }
    }
    public static class ProcessInputThread extends Thread {
        BufferedWriter processOutput;
        Scanner input;
        PrintStream output;
        public ProcessInputThread(BufferedWriter processOutputIn,
                InputStream inputIn,
                PrintStream outputIn) {
            this.processOutput = processOutputIn;
            this.input = new Scanner(inputIn);
            this.output = outputIn;
        }
        public void run() {
            try {
                while (true) {
                    synchronized (output) {
                        //System.out.wait();
                        output.print("bash$ ");
                    }
                    String text = input.nextLine();
                    text += '\n';
                    processOutput.write(text);
                    processOutput.flush();
                    Thread.sleep(10);
                }
            }
            catch (IOException | InterruptedException e) {
                synchronized (output) {
                    output.println("Connection Closed.");//e.toString());
                }
                //e.printStackTrace();
            }
            finally {
                try {
                    processOutput.close();
                }
                catch (IOException e) {
                    output.println("Output stream Could not be Closed;");
                    //e.printStackTrace();
                }
            }
            Thread.currentThread().interrupt();
            return;
        }
    }



    public static void main(String[] args) {
        try{
            ServerSocket server = new ServerSocket(9232);
            while (true) {
                Socket connection = server.accept();
                System.out.println("A new connection has been made from " + connection.getInetAddress() + ".\n");
                PrintStream output = new PrintStream(connection.getOutputStream());
                InputStream input = connection.getInputStream();
                List<String> commands = new ArrayList<String>();
                for (String command : args) {
                    commands.add(command);
                }
                ProcessBuilder processbuilder = new ProcessBuilder(commands);
                Process process = processbuilder.start();
                BufferedReader processInput = new BufferedReader(new InputStreamReader(process.getInputStream()));
                BufferedWriter processOutput = new BufferedWriter(new OutputStreamWriter(process.getOutputStream()));
                System.out.println("Here is the standard output of the command:\n");
                Thread t1 = new ProcessOutputThread(processInput, output);
                t1.start();
                Thread t2 = new ProcessInputThread(processOutput, input, output);
                t2.start();
            }
        }
        catch (Exception e) {
            System.out.println("This is sad ");
        }
    }
}
