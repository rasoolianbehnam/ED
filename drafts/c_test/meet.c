#include <stdio.h>
//#include <stdlib.h>
#include <string.h>

int main(int argc, char* argv[]) {
    char name[400];
    strcpy(name, argv[1]);
    printf("%s\n", name);
    return 0;
}
