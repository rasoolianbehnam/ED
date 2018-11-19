#include "type.h"

Node* list, *p;
int main() {
    list = (Node*) malloc(sizeof(Node)); 
    p = list;
    for (int i=1;i<10;i++) {
        p->value = i;
        sprintf(p->name, "Node%d", i);
        p->next = (Node*) malloc(sizeof(Node)); 
        p = p->next;
    }
   printNode(searchLinkedList(list, 5));
   printf("\n");
   printLinkedList(list); 
}
