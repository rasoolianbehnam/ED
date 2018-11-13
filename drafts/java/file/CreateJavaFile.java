import java.io.*;
public class CreateJavaFile{
    public static void main(String[] args) {
        if (args.length <= 0) {
            System.out.println("Usage java CreateJavaFile filename");
            return;
        }
        String fileName = args[0];
        String[] split_path = fileName.split("/");
        String name_extension = split_path[split_path.length-1];
        String dir = 
            fileName.substring(0, fileName.length()-name_extension.length());
        if (dir.length() == 0) 
            dir = "./";
        int indexOfJava = name_extension.indexOf(".java");
        String baseName;
        if (indexOfJava < 0) baseName = name_extension;
        else baseName = name_extension.substring(0, indexOfJava);
        baseName = baseName.substring(0, 1).toUpperCase() 
            + baseName.substring(1, baseName.length());
        System.out.println(name_extension);
        System.out.println(dir);
        System.out.println(baseName);
        try {
            File file = new File(baseName + ".java");
            if (file.exists())  {
                System.out.println("File " + name_extension + " already exists");
                return;
            }
            BufferedWriter bf = new BufferedWriter(new PrintWriter(file));
            bf.write("public class " + baseName + " {\n");
            bf.write("    public static void main(String[] args) {\n");
            bf.write("    }\n}");

            bf.close();
        } catch(FileNotFoundException e) {
            e.printStackTrace();
        }catch(IOException e) {
            e.printStackTrace();
        }

    }
}
