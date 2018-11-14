import java.io.File;
public class ProcessorTest{
    public static void main(String[] args) {
        Runtime run = Runtime.getRuntime();
        System.out.println(run.availableProcessors());
        System.out.println(run.freeMemory() / 1024 / 1024 + "Mb");
        System.out.println(run.totalMemory() / 1024 / 1024 + "Mb");
        File[] roots = File.listRoots();

            /* For each filesystem root, print some info */
        for (File root : roots) {
            System.out.println("File system root: " + root.getAbsolutePath());
            System.out.println("Total space (bytes): " + root.getTotalSpace() / 1024 / 1024 + "Mb");
            System.out.println("Free space (bytes): " + root.getFreeSpace() / 1024 / 1024 + "Mb");
            System.out.println("Usable space (bytes): " + root.getUsableSpace() / 1024 / 1024 + "Mb");
        }
    }

}
