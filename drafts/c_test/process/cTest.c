#include <stdio.h>

int main() {
    char s[128];
    //printf("s = %s\n", s);
    int pd[2];
    pipe(pd);
    if (fork()) {
        close(pd[0]);
        close(1);
        dup(pd[1]);
        close(pd[1]);
        //for (int i=0; i<3; i++) {
        while (1) {
        fgets(s, 128, stdin);
        write(1, s, strlen(s));
        //printf("%s\n", s);
        }
    } else {
        close(pd[1]);
        int n;
        char buff[128];
        for (int i=0; i<4; i++) {
        while (n = read(pd[0], buff, 128)) {
            buff[n] = 0;
            printf("read: %s\n", buff);
        }
        }
    }
}
