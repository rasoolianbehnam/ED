#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <sys/types.h>



struct internet {
 int priority;
 char *name;
};

void winner()
{
 printf("and we have a winner @ %d\n", time(NULL));
}

int main(int argc, char **argv)
{
 struct internet *i1, *i2, *i3;

 i1 = malloc(sizeof(struct internet));
 i1->priority = 1;
 i1->name = malloc(8);

 i2 = malloc(sizeof(struct internet));
 i2->priority = 2;
 i2->name = malloc(8);
 
 printf("i1->name is at %p and i2->name is at %p\n", i1->name, i2->name);
 strcpy(i1->name, argv[1]);
 printf("i1->name is at %p and i2->name is at %p\n", i1->name, i2->name);
 strcpy(i2->name, argv[2]);

 printf("and that's a wrap folks!\n");
}
