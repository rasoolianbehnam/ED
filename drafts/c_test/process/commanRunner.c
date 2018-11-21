#include <stdio.h>
#include <dirent.h>
#include <unistd.h>


char* commands[] = {"cd", "ls", "q", "pwd"};
char *cwd[FILENAME_MAX];
char *home;

char* findEnv(char *var, char* envs[]) {
    int i = 0;
    while (envs[i]) {
        if (strncmp(var, envs[i], strlen(var)) == 0)
            return envs[i];
        i++;
    }
    return 0;
}
findCmd(char *command) {
    int i = 0;
    while (commands[i]) {
        if (strcmp(command, commands[i]) == 0) return i;
        i++;
    }
    return -1;
}

int getPipes(char* command, char* head, char* tail) {
    char tmp[strlen(command)];
    strcpy(tmp, command);
    char* token;
    char s[] = "|";
    token = strtok(tmp, s);
    strcpy(head, token);
    strcpy(tail, command+strlen(token)+strlen(s));
}

int getCommandAndArgs(char* line, char* cmd, char* args) {
    *cmd = *args = 0;
    sscanf(line, "%s %s", cmd, args);
    strcpy(args, line+strlen(cmd));
}

int run_command(char*cmd, char*args, char* envs[]) {
   char tmp[strlen(args)]; 
   strcpy(tmp, args);
   char s[] = " ";
   char* token;
   int count = 0;
   token = strtok(tmp, s);
   while (token) {
       count++;
       token = strtok(NULL, s);
   }
   char* args_array[count+2];
   args_array[0] = cmd;
   strcpy(tmp, args);
   count = 1;
   token = strtok(tmp, s);
   while (token) {
       args_array[count] = token;
       count++;
       printf("arg = %s\n", token);
       token = strtok(NULL, s);
   }
   args_array[count] = 0;

   char* path = findEnv("PATH", envs);
   char full_path[64];
   printf("path = %s\n", path);
   char tmp2[strlen(path)];
   strcpy(tmp2, path);
   token = strtok(tmp2, ":");
   for (int i = 0; args_array[i]; i++) {
       printf("args = %s\n", args_array[i]);
   }
   char* myenvs[] = { 0 };
   while (token) {
       strcpy(full_path, token);
       strcat(full_path, "/");
       strcat(full_path, cmd);
       printf("full command: %s\n", full_path);
       if (access(full_path, F_OK) != -1) {
           args_array[0] = full_path;
           printf("executing %s = %s\n", cmd, args_array[0]);
           int pid;
           int wpid;
           int status;
           if ((pid = fork()))  {
               while (wpid = wait(&status) > 0);
               return 0;
           } else {
               int r = execve(args_array[0], args_array, myenvs);
               printf("Execve failed r = %d\n", r);
           }
           break;
       }
       token = strtok(0, ":");
   }
   printf("%s cannot be found!\n", cmd);
}

int handle_single(char* cmd, char *args, char* envs[]) {
    int index = findCmd(cmd);
    switch (index) {
        case 0: 
            if (strlen(args) == 0)  {
                printf("cd %s\n", home);
                int ret = chdir(home);
                if (ret != 0) {
                    printf("Cannot change directory to %s\n", home);
                }
            } else if (*args == '~') {
                printf("~ is replaces with %s\n", home);
                char path[strlen(home) + strlen(args) + 10];
                strcpy(path, home);
                strcat(path, args+1);
                int ret = chdir(path);
                if (ret != 0) {
                    printf("Cannot change directory to %s\n", path);
                }
            }
            else {
                int ret = chdir(args);
                if (ret != 0) {
                    printf("Cannot change directory to %s\n", args);
                }
            }
            break;
        case 1:
            if (strlen(args) == 0)  {
                ls("./");
            } else {
                ls(args);
            }
            break;
        case 2:
            exit(0);
            break; 
        case 3:
            if (getcwd(cwd, sizeof(cwd)) != NULL) {
                printf("%s\n", cwd);
            } else printf("Cannot find current directory\n");
            break;
        case -1:
            //getPipes(line, &head, &tail);
            //printf("head = %s and tail = %s\n", head, tail);
            run_command(cmd, args, envs);
            break;
    }
        printf("***********************************\n");
}

int handle_multi(char *line, char* envs[]) {
        char head[32], tail[64], cmd[32], args[64];
        getPipes(line, head, tail); 
        printf("head = %s and tail = %s\n", head, tail);
        getCommandAndArgs(head, cmd, args);
        printf("command = %s, args = %s\n", cmd, args);
        if (strlen(tail) == 0) {
           handle_single(cmd, args, envs); 
        } else {
            printf("piped\n");
            int fd[2];
            pipe(fd);
            if (fork()) {
                close(fd[0]);
                close(1);
                dup(fd[1]);
                close(fd[1]);
                //handle_single(cmd, args, envs);
                printf("cmd = %s\n", cmd);
                //handle_multi(tail);
                int status;
                int wpid;
                //while (wpid = wait(&status) > 0);
                //sleep(1);
            } else {
                close(fd[1]);
                close(0);
                dup(fd[0]);
                close(fd[0]);
                //handle_multi(tail, envs);
                printf("again, tail = %s\n", tail);
                char mardas[128];
                int n;
                while (1) {
                    printf("pertas\n");
                    if (n = read(0, mardas, 128)) {
                        mardas[n] = 0;
                        printf("mardas: %s\n", mardas);
                    }
                    else {
                        printf("exitting\n");
                        exit(0);
                    }
                }
            }
        }
}


//tokenize(char* 
//handle(char* head, char* tail) {
//
//}
//
ls(char* path) {
    printf("path is %s\n", path);
    DIR *dir;
    struct dirent *ent;
    printf("%s\n", path);
    if ((dir = opendir(path)) != NULL) {
        while ((ent = readdir(dir)) != NULL) {
            printf("%s\n", ent->d_name);
        }
      closedir (dir);
    } else {
          /* could not open directory */
        perror ("");
    }
}

int main(int argc, char* argv[], char* envs[]) {
    char line[128];
    home = findEnv("HOME", envs)+5;
    while (1) {
        printf("My bash> ");
        fgets(line, 128, stdin);
        line[strlen(line)-1] = 0;
        //printf("%s\n", line);
        //printf("index = %d\n", index);
        //printf("line = %s\n", line);
        //printf("line = %s\n", cmd);
        //int ret = chdir("/");
        //printf("ret = %d\n", ret);
        //if (getcwd(cwd, FILENAME_MAX) != NULL) {
        //    printf("current dir: %s\n", cwd);
        //} else printf("error\n");
        //printf("env %s = %s\n", "PWD", findEnv("PWD", envs));
        //continueLoop = 0;

        handle_multi(line, envs);
    }
    ////execve(argv[1], argv+1, envs);
}
