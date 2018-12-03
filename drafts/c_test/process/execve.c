/* execve.c */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char *argv[])
{
    int p[2];
    pipe(p);
    if (fork()) {
        close(p[1]);
        close(0);
        dup(p[0]);
        close(p[0]);
        char mardas[128];
        int n;
        while (1) {
            if((n=read(0, mardas, 128)) > 0) {
                mardas[n-1] = 0;
                printf("[Main] %s | %d\n", mardas, n);
            }
            else {
                printf("[Main] No more to read\n");
                exit(0);
            }
        }
        //char *newargv[] = { "/usr/bin/wc", NULL };
        //char *newenviron[] = { NULL };
        //newargv[0] = argv[1];
        //execve(newargv[0], newargv, newenviron);
    } else {
        close(p[0]);
        close(1);
        dup(p[1]);
        close(p[1]);
        char* mardas[] = {"1", "2", "3", "4", "5", "6"};
        for (int i=0;i < 3; i++) {
            printf("hello process %d\n", i);
            //char *newargv[] = { "/bin/echo", "hello", "process", mardas[i], NULL };
            //char *newenviron[] = { NULL };
            //execve(newargv[0], newargv, newenviron);
        }
    }
}
