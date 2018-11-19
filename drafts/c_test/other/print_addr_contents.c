#include <stdio.h>
#include <stdlib.h>
#include <string.h>

main(int argc, char* argv[]) {
    //if (argc < 2) {
    //    printf("%s env", argv[0]);
    //    exit(-1);
    //}
    //long int ret = atoi(argv[1]);
    int ret = 0xffd6d7e5;
    printf("address of shellcode is 0x%08x \n", ret);
    printf("contents of 0x%08x: %s \n", ret, (char*) ret);
}
