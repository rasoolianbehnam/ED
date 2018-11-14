import java.io.*;
import java.util.*;
import java.io.BufferedWriter;

public class RunCommand {
    public static class ProcessOutputThread extends Thread {
        BufferedReader stdInput;
        public ProcessOutputThread(BufferedReader stdInputIn) {
            this.stdInput = stdInputIn;
        }
        public void run() {
            String s;
            try {
                while ((s = stdInput.readLine()) != null) {
                    synchronized (System.out) {
                        System.out.println(s);
                        //System.out.notify();
                    }
                }
            }
            catch (Exception e) {
                e.printStackTrace();
            }
            finally {
                try {
                    stdInput.close();
                }
                catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }
    public static class ProcessInputThread extends Thread {
        BufferedWriter stdOutput;
        public ProcessInputThread(BufferedWriter stdOutputIn) {
            this.stdOutput = stdOutputIn;
        }
        public void run() {
            Scanner scan = new Scanner(System.in);
            try {
                while (true) {
                    synchronized (System.out) {
                        //System.out.wait();
                        System.out.print("bash$ ");
                    }
                    String input = scan.nextLine();
                    input += '\n';
                    stdOutput.write(input);
                    stdOutput.flush();
                    Thread.sleep(10);
                }
            }
            catch (Exception e) {
                e.printStackTrace();
            }
            finally {
                try {
                    stdOutput.close();
                }
                catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }



    public static void main(String[] args) {
        try{
            List<String> commands = new ArrayList<String>();
            for (String command : args) {
                commands.add(command);
            }
            ProcessBuilder processbuilder = new ProcessBuilder(commands);
            Process process = processbuilder.start();
            BufferedReader stdInput = new BufferedReader(new InputStreamReader(process.getInputStream()));
            BufferedWriter stdOutput = new BufferedWriter(new OutputStreamWriter(process.getOutputStream()));
            System.out.println("Here is the standard output of the command:\n");
            Thread t1 = new ProcessOutputThread(stdInput);
            t1.start();
            Thread t2 = new ProcessInputThread(stdOutput);
            t2.start();
        }
        catch (Exception e) {
            System.out.println("This is sad ");
        }
    }
}
