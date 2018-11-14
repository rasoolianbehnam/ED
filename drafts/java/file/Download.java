import java.net.*;
import java.io.*;
import java.util.regex.*;
import java.util.HashMap;
public class Download {
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
    public static void main(String[] args) {
        try {
            String curlText = args[0];
            String maxNum;
            //log(curlText);
            int indexOfHeader = curlText.indexOf("-H");
            String urlString = curlText.substring(curlText.indexOf("'")+1, indexOfHeader-2);
            log(urlString);
            String[] header_title = new String[2];
            URL url = new URL(urlString);
            URLConnection uc = url.openConnection();
            HashMap<String,String> headers = processNextHeader(curlText, indexOfHeader, header_title);
            for (String key : headers.keySet()) {
                log(key + " : " + headers.get(key));
                uc.setRequestProperty(key, headers.get(key));
            }
            String fileName = getFileName(url);
            if (args.length > 1) 
                maxNum = args[1];
            Matcher m = Pattern.compile("\\((0{0,4})(\\d{1,4})\\)").matcher(fileName);
            m.find();
            String zero_part = m.group(1);
            String number_part = m.group(2);
            String replaceString;
            replaceString = "%d";
            if (zero_part.length() > 0) 
                replaceString = String.format("%%0%dd", zero_part.length()+number_part.length());
            log("Replace String: " + replaceString);
            log(zero_part);
            log(number_part);
            String fileNameTemplate = m.replaceFirst(replaceString);
            log(fileNameTemplate);
            //if (maxNum.startsWith("0")
            //File output = new File(fileName);
            //BufferedOutputStream fos= new BufferedOutputStream(
            //        new FileOutputStream(output));
            ////URLConnection connection = url.openConnection();
            //InputStream result = new BufferedInputStream(
            //        uc.getInputStream());
            ////StringBuilder sb = new StringBuilder();
            //int input;
            //while ((input = result.read()) != -1) {
            //    //sb.append((char) input);
            //    fos.write(input);
            //}
            ////System.out.println(sb);

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
