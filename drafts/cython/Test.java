public class Test {
    public static long doReallyLongThing(int n) {
        if ( n <= 1) return 1;
        return n * doReallyLongThing(n-1);
    }
    public static void main(String[] args) {
        long total_time = 0;
        long startTime, endTime;
        for (int i=0; i < 100000; i++) {
            startTime = System.nanoTime();
            doReallyLongThing(30);
            endTime = System.nanoTime();
            total_time += (endTime  - startTime);
        }
        System.out.println("That took " + (total_time / 100000.) + " nanoseconds");
    }
}
