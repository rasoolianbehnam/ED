public class HelloJni {
    static {
        System.loadLibrary("libSystem.B.dylib");
    }
    private native void printf(String mardas);
    public static void main(String[] args) {
        (new HelloJni()).printf("mardas\n");
    }
}
