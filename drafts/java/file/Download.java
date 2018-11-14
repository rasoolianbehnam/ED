import java.net.*;
import java.io.*;
import java.util.regex.*;
import java.util.*;
import java.util.concurrent.*;
public class Download {
    private static class DownloadThread implements Callable<Void> {
        private static final int MAX_TRIES = 15;
        private Queue<String> q;
        private HashMap<String,String> headers;
        private static HashMap<String, Integer> tryCounts;
        public void cleanup(String urlText) {
            int count;
            synchronized (tryCounts) {
                count = hashGet(tryCounts, urlText, 0) ;
                tryCounts.put(urlText, count+1);
            }
            if (count < MAX_TRIES) {
                synchronized (q) {
                    q.add(urlText);
                }
            } else logErr("[!] Giving up on " + urlText + ".");
        }

        public void cleanup(File f) {
            f.delete();
        }
        public void cleanup(InputStream in) {
            try {
                in.close();
            } catch (IOException e) {
                logErr("[!] Couldn't close input Stream");
            }
        }
        public void cleanup(OutputStream out) {
            try {
                out.close();
            } catch (IOException e) {
                logErr("[!] Couldn't close Output Stream");
            }
        }

        public DownloadThread(Queue<String> qIn, HashMap<String,String> headersIn) {
            this.q = qIn;
            this.headers = headersIn;
            tryCounts = new HashMap<String, Integer>();
        }
        public Void call() {
            String urlText = null;
            String fileName = null;
            BufferedOutputStream fos = null;
            InputStream result = null;
            URL url = null;
            URLConnection uc = null;
            File output = null;
            while (true) {
                synchronized (q) {
                    urlText = q.poll();
                }
                if (urlText == null) {
                    break;
                }
                try {
                    url = new URL(urlText);
                } catch (MalformedURLException e) {
                    logErr("[!] Malformed URL: " + urlText);
                    cleanup(urlText);
                    continue;
                }
                try {
                    uc = url.openConnection();
                } catch (IOException e) {
                    logErr("[!] Cannot create connection");
                    cleanup(urlText);
                    continue;
                }
                fileName = getFileName(url);
                for (String key : headers.keySet()) {
                    //log(key + " : " + headers.get(key));
                    uc.setRequestProperty(key, headers.get(key));
                }
                try {
                    result = new BufferedInputStream( uc.getInputStream());
                    //StringBuilder sb = new StringBuilder();
                } catch (IOException e) {
                    logErr("[!] Cannot get stream.");
                    cleanup(urlText);
                    continue;
                }
                output = new File(fileName);
                if (output.exists()) {
                    synchronized (System.out) {
                        log("File " + fileName + " already exists.");
                    }
                    continue;
                }
                log("[*] Downloading file " + fileName + ".");
                try {
                    fos = new BufferedOutputStream(
                            new FileOutputStream(output));
                } catch (FileNotFoundException e) {
                    logErr("[!] File not Found!");
                    cleanup(urlText);
                    continue;
                }

                int input;
                try {
                    while ((input = result.read()) != -1) {
                        //sb.append((char) input);
                        fos.write(input);
                    }
                } catch (IOException e) {
                    logErr("[!] Problem with writing to file.");
                    cleanup(urlText);
                    cleanup(fos);
                    cleanup(result);
                    cleanup(output);
                    continue;
                }
                synchronized (System.out) {
                    log("[*] Finished Downloading from " + fileName + ".");
                }
                try {
                    fos.close();
                    result.close();
                } catch (IOException e) {
                    logErr("[!] Problem closing streams!");
                }
            }
            Thread.currentThread().interrupt();
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
            String maxNum = "0";
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
            for (int i=0; i < Integer.parseInt(maxNum)+1; i++) {
                if(!(new File(String.format(fileNameTemplate, i)).exists()))
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
    public static void logErr(String text) {
        System.err.println(text);
    }

    public static <T, S> S hashGet(HashMap<T,S> hash, T key, S defaultValue) {
       S value = hash.get(key);
       if (value == null)
           return defaultValue;
       return value;
    }
}
