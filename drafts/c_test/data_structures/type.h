#include <stdio.h>

#define NODE(myType, node_name)  \
typedef struct  {       \
    struct mardas* next;      \
    myType value;           \
    char name[20];          \
} node_name;

#define NODEFOREACH(node, head, var)       \
    for (node var=head; var; var=var->next)

NODE(int, Node);

void printNode(Node *n) {
    printf("[%s %d]", n->name, n->value);
}

void printLinkedList(Node *n) {
    NODEFOREACH(Node*, n, i) {
        printf("[%s %d]->", n->name, n->value);
    }
}

Node* searchLinkedList(Node *p, int value) {
    NODEFOREACH(Node*, p, n) {
        if (n->value == value) {
            return n;
        }
    }
    return 0;
}
