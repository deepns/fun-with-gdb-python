#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <strings.h>
#include <sys/time.h>

typedef struct node {
    int id;
    char name[64];
    time_t creation_time;
    struct node *left;
    struct node *right;
} node_t;

typedef short bool;
#define true 1
#define false 0

node_t *create_node(char *name) {
    static int id = 0;
    node_t *node = malloc(sizeof(node_t));
    node->id = id++;
    snprintf(node->name, 64, "%s", name);

    node->creation_time = time(NULL);
    node->left = NULL;
    node->right = NULL;
    return node;
}

void free_node(node_t *node) {
    if (!node) {
        return;
    }

    node->left = NULL;
    node->right = NULL;
    free(node);
}

void print_node(node_t *node, int recurse) {
    if (!node) {
        return;
    }

    printf("id=%d, name=%s, creation_time(secs)=%lu, creation_time=%s",
        node->id, node->name, node->creation_time, ctime(&node->creation_time));

    if (recurse) {
        print_node(node->left, true);
        print_node(node->right, true);
    }
}

node_t *insert_left(node_t *node, char *name)
{
    if (!node) {
        return NULL;
    }

    if (!node->left) {
        node->left = create_node(name);
    }
    return node->left;
}

node_t *insert_right(node_t *node, char *name)
{
    if (!node) {
        return NULL;
    }

    if (!node->right) {
        node->right = create_node(name);
    }
    return node->right;
}

int main() {
    node_t *root = create_node("root");
    insert_left(root, "X");
    insert_right(root, "Y");
  
    print_node(root, true);
    
    free_node(root->left);
    free_node(root->right);
    free_node(root);

    return 0;
}
