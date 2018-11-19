#include <stdio.h>

#define N 10

int main() {
    int i, a[N];
    for (i=0; i<N+2; i++) {
        a[i] = i+1;
    }
    a[i] = 123456789;
    printf("i = %d\n", i);
    printf("%d\n", a[i]);
}
