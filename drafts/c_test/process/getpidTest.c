#include <stdio.h>

int main() {
    int pid, status;
    printf("This is %d and my parent is %d\n", getpid(), getppid());
    pid = fork();
    prctl(PR_SET_CHILD_SUBREAPER);
    if (pid) {
        printf("This is process %d and my child is %d\n", getpid(), pid);
        //sleep(2);
        pid=wait(&status);
        //printf("PARENT %d EXIT\n", getpid());
        printf("DEAD CHILD=%d, status=0x%04x\n", pid, status);
    }
    else {
        printf("This is process %d and my parent is %d\n", getpid(), getppid());
        sleep(1);
        //printf("CHILD %d EXIT\n", getpid());
        printf("CHILD %d DIES with exit (VALUE)\n", getpid());
        exit(100);
    }
}