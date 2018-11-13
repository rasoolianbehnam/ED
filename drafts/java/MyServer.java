import java.io.*;  
import java.net.*;  
public class MyServer {  
    public static void main(String[] args){  
        try{  
            ServerSocket ss = new ServerSocket(6666);  
            Socket s = ss.accept();//establishes connection   
            DataInputStream dis = new DataInputStream(s.getInputStream());  
            String  str = (String)dis.readLine();  
            System.out.println("message= "+str);  
            ss.close();  
        } catch(Exception e){e.printStackTrace();}  
    }  
}  
