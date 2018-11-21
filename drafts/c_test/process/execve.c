/* execve.c */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int
main(int argc, char *argv[])
{
    char *newargv[] = { "/bin/echo", "hello", "world", NULL };
    char *newenviron[] = { NULL };
    //newargv[0] = argv[1];
    execve(newargv[0], newargv, newenviron);
}
