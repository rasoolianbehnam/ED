import java.net.*;
import java.io.*;
import java.util.regex.*;
import java.util.*;
import java.util.concurrent.*;
public class Download {
    private static class DownloadThread implements Callable<Void> {
        Queue<String> q;
        HashMap<String,String> headers;
        public DownloadThread(Queue<String> qIn, HashMap<String,String> headersIn) {
            this.q = qIn;
            this.headers = headersIn;
        }
        public Void call() {
            URL url = null;
            while (true) {
                try {
                    String urlText;
                    synchronized (q) {
                        urlText = q.poll();
                    }
                    if (urlText == null) {
                        break;
                    }
                    url = new URL(urlText);
                    URLConnection uc = url.openConnection();
                    String fileName = getFileName(url);
                    File output = new File(fileName);
                    if (output.exists()) {
                        synchronized (System.out) {
                            log("File " + fileName + " already exists.");
                        }
                        continue;
                    }
                    BufferedOutputStream fos= new BufferedOutputStream(
                            new FileOutputStream(output));
                    for (String key : headers.keySet()) {
                        //log(key + " : " + headers.get(key));
                        uc.setRequestProperty(key, headers.get(key));
                    }

                    log("[*] Downloading file " + fileName + ".");
                    InputStream result = new BufferedInputStream(
                            uc.getInputStream());
                    //StringBuilder sb = new StringBuilder();
                    int input;
                    while ((input = result.read()) != -1) {
                        //sb.append((char) input);
                        fos.write(input);
                    }
                    synchronized (System.out) {
                        log("[*] Finished Downloading from " + url + ".");
                    }
                } catch (IOException e) {
                    if (url != null)
                        synchronized (System.out) {
                            log("[!] Problem downloading from " + url + ".");
                        }
                }
            }
            return null;
        }
    };
    private static HashMap<String, String> processNextHeader(String curlText, int indexOfHeader, String[] header) {
        HashMap<String,String> output = new HashMap<String,String>();
        Pattern p = Pattern.compile("-H '(.*?):(.*?)'");
        Matcher m = p.matcher(curlText);
        while (m.find()) {
            output.put(m.group(1).trim(), m.group(2).trim());
        }
        return output;

    }
    private static String getFileName(URL url) {
        String[] parts = url.getPath().split("/");
        return parts[parts.length-1];
    }
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        try {
            String curlText = args[0];
            String maxNum;
            int numThreads = 1;
            //log(curlText);
            int indexOfHeader = curlText.indexOf("-H");
            String urlString = curlText.substring(curlText.indexOf("'")+1, indexOfHeader-2);
            log(urlString);
            String[] header_title = new String[2];
            URL url = new URL(urlString);
            //URLConnection uc = url.openConnection();
            HashMap<String,String> headers = processNextHeader(curlText, indexOfHeader, header_title);
            String fileName = getFileName(url);
            if (args.length > 1) 
                maxNum = args[1];
            if (args.length > 2)
                numThreads = Integer.parseInt(args[2]);
            Pattern p = Pattern.compile("\\((0{0,4})(\\d{1,4})\\)");
            Matcher m = p.matcher(fileName);
            m.find();
            String zero_part = m.group(1);
            String number_part = m.group(2);
            String replaceString;
            replaceString = "%d";
            if (zero_part.length() > 0) 
                replaceString = String.format("%%0%dd", zero_part.length()+number_part.length());
            //log("Replace String: " + replaceString);
            String fileNameTemplate = m.replaceFirst(replaceString);
            String urlTemplate = p.matcher(urlString).replaceFirst(replaceString);
            log(urlTemplate);
            //log(fileNameTemplate);
            Queue<String> q = new LinkedList<String>();
            for (int i=1; i < Integer.parseInt(number_part)+1; i++) {
                q.add(String.format(urlTemplate, i));
            }
            ExecutorService executor = Executors.newFixedThreadPool(numThreads);
            ArrayList<Future<Void>> tasks = new ArrayList<Future<Void>>();
            for (int i=0; i<numThreads; i++) {
                Callable<Void> task = new DownloadThread(q, headers);
                tasks.add(executor.submit(task));
            }
            for (Future<Void> task : tasks) {
                task.get();
            }
            executor.shutdown();
        }
        catch(IOException e) {
           System.out.println("[!] Cannot open connection!"); 
           e.printStackTrace();
        }
    }
    public static void log(String text) {
        System.out.println(text);
    }
}
