#include <stdio.h>
#include <stdlib.h>
char mardas[] = "mardas=raghas";
//void main(int argc, char* argv[]) {
//    if (argc < 3) {
//        printf("Usage: %s <environment var> <target program name>\n", argv[0]);
//        exit(0);
//    }
//    //putenv(mardas);
//    printf("argv1 = %s and argv2 = %s\n", argv[1], argv[2]);
//    char* ptr = getenv(argv[1]);
//    printf("content of %p: %s\n", ptr, ptr);
//    ptr += (strlen(argv[0]) - strlen(argv[2]))*2;
//    printf("%s is at %p\n", argv[1], ptr);
//
//    char* env[2] = {mardas, 0};
//    //execle("./test.out", "test.out", mardas, 0, env); 
//    execle("./get_env.out", "get_env.out", argv[1], "get_env.out", 0, env);
//    exit(127);
//    printf("****************************\n");
//    execle("./get_env.out", "get_env.out", argv[1], "get_env.out", 0, env);
//    exit(127);
//    //execle("./get_env.out", "get_env.out", argv[1], "get_env.out", 0, env);
//    //execl("./get_env.out", "get_env.out", argv[1], "get_env.out", 0);
//}


void main(int argc, char* argv[]) {
    int diff = atoi(argv[1]);
    char path[] = "PATH";
    char* ptr = (char*)((int) getenv(path) + diff);
    printf("content of %p is %s\n", ptr, ptr);
    exit(0);
}
