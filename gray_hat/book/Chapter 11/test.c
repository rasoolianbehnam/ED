#include <stdio.h>

int main() {
    strcpy(A, "AAAA");
    strcpy(B, "BBBB");
    strcpy(C, "CCCC");
    printf("%s.%s.%s\n", A, B, C);
    printf("Address of A: %p\n", A);
    printf("Address of B: %p\n", B);
    printf("Address of C: %p\n", C);
}
