#include <stdio.h>

int main(int argc, char* argv[], char* envs[]) {
    int i = 0;
    //printf("%s\n",*(char**)getenv("SHELL"));
    while (strncmp(envs[i], "PATH", 4) != 0) {
        i++;
    }
    printf("paths = %s\n", envs[i]+5);
    char paths[strlen(envs[i])];
    strcpy(paths, envs[i]+5);
    char s[2] = ":";
    char* token = strtok(paths+4, s);
    token = strtok(NULL, s);
    do {
        printf("%s\n", token);
        token = strtok(NULL, s);
    }
    while (token);
    printf("paths = %s\n", envs[i]+5);
}
