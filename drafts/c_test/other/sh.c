#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

char* shellcode = "mardas";

int main() {
    char* env[2] = {shellcode, 0};
    //execle("./test.out", "test.out", shellcode, 0, env); 
    execle("/bin/sh", "sh", 0, env); 
}
