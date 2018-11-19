#include <stdio.h>

typedef struct entry{ struct entry *next;
    char name[64];
    int priority;
}ENTRY;

void printQ(ENTRY *queue)
{
    while(queue){
        // print queue contents
        printf("[%s %d]-> ", queue->name, queue->priority);
        queue = queue->next;
    }
    printf("\n");
}

int main() {
    return(0);
}
