#include <iostream>

struct Node {
    int value;
    Node *left;
    Node *right;
    Node(int val) : value(val), left(nullptr), right(nullptr) {}
};

/**
 * Computes the Internal Path Length (IPL) of a Binary Search Tree (BST).
 *
 * Definition:
 * The Internal Path Length (IPL) of a BST is the sum of the depths of all nodes in the tree.
 * The depth of a node is the number of edges from the root to that node.
 *
 * Example:
 *        10
 *       /  \
 *      5    15
 *     / \     \
 *    2   7    20
 *
 * IPL = (depth of 10) + (depth of 5) + (depth of 15) + (depth of 2) + (depth of 7) + (depth of 20)
 *     = 0 + 1 + 1 + 2 + 2 + 2 = 8
 *
 * @param root Pointer to the root node of the BST.
 * @param depth Current depth of the node (default is 0 for the root call).
 * @return The sum of depths of all nodes (Internal Path Length).
 */
int internalPathLength(Node *root, int depth = 0) {
    if (!root)
        return 0; // Base case: Empty subtree contributes 0 to IPL
    return depth + internalPathLength(root->left, depth + 1) + internalPathLength(root->right, depth + 1);
}

// Example usage:
// Node* root = new Node(10);
// root->left = new Node(5);
// root->right = new Node(15);
// root->left->left = new Node(2);
// root->left->right = new Node(7);
// root->right->right = new Node(20);
// std::cout << "Internal Path Length: " << internalPathLength(root) << std::endl;
