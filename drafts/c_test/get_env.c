#include <stdio.h>
#include <stdlib.h>

char* main(int argc, char* argv[]) {
    if (argc < 3) {
        printf("Usage: %s <environment var> <target program name>\n", argv[0]);
        exit(0);
    }
    printf("argv1 = %s and argv2 = %s\n", argv[1], argv[2]);
    char path[] = "PATH";
    char* ptr0 = getenv(path);
    printf("content of %p: %s\n", ptr0, ptr0);

    char* ptr = getenv(argv[1]);
    printf("content of %p: %s\n", ptr, ptr);
    printf("diff = %d\n", (int) ptr - (int) ptr0);
    printf("%d\n", (int) ptr0);
    printf("%d\n", (int) ptr - (int) ptr0);

    exit(0);
}

