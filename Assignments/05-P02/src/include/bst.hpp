#pragma once

class Bst {
private:
    struct Node {
        int data;
        Node *left;
        Node *right;

        explicit Node(int value)
            : data(value), left(nullptr), right(nullptr) {}
    };

    Node *root;

    // Recursive insert helper
    bool insert(Node *&node, int value) {
        if (!node) {
            node = new Node(value);
            return true;
        }

        if (value < node->data) {
            return insert(node->left, value);
        }
        if (value > node->data) {
            return insert(node->right, value);
        }

        // duplicate value: do nothing
        return false;
    }

    // Recursive search helper
    bool contains(Node *node, int value) const {
        if (!node) {
            return false;
        }

        if (value == node->data) {
            return true;
        }
        if (value < node->data) {
            return contains(node->left, value);
        }

        return contains(node->right, value);
    }

    // Find smallest node in subtree
    Node *findMin(Node *node) const {
        while (node && node->left) {
            node = node->left;
        }
        return node;
    }

    // Recursive erase helper
    bool erase(Node *&node, int value) {
        if (!node) {
            return false;
        }

        if (value < node->data) {
            return erase(node->left, value);
        }
        if (value > node->data) {
            return erase(node->right, value);
        }

        // Found node to delete

        // Case 1: leaf node
        if (!node->left && !node->right) {
            delete node;
            node = nullptr;
            return true;
        }

        // Case 2: only right child
        if (!node->left) {
            Node *temp = node;
            node = node->right;
            delete temp;
            return true;
        }

        // Case 3: only left child
        if (!node->right) {
            Node *temp = node;
            node = node->left;
            delete temp;
            return true;
        }

        // Case 4: two children
        Node *successor = findMin(node->right);
        node->data = successor->data;
        return erase(node->right, successor->data);
    }

    // Postorder cleanup helper
    void clear(Node *node) {
        if (!node) {
            return;
        }

        clear(node->left);
        clear(node->right);
        delete node;
    }

public:
    Bst() : root(nullptr) {}

    ~Bst() {
        clear(root);
    }

    bool insert(int value) {
        return insert(root, value);
    }

    bool contains(int value) const {
        return contains(root, value);
    }

    bool erase(int value) {
        return erase(root, value);
    }
};