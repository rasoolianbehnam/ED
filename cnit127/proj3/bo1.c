#include <stdio.h>
#include <string.h>

int main(int argc, char* argv[]) {
    copier(argv[1]);
    printf("Done!\n");
}

int copier(char* str) {
    char buffer[100];
    strcpy(buffer, str);
    printf("%s\n", buffer);
}
