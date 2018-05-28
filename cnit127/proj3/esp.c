#include <stdio.h>

int main() {
    register int esp asm("esp");
    printf("$esp = %#010x\n", esp);
}
