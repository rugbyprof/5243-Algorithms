#pragma once

#include "counters.hpp"
#include "statsInterface.hpp"
#include <iostream>
#include <string>
#include <vector>

using namespace std;

struct Node {
public:
    long long data;
    Node *left;
    Node *right;

    Node(int d) : data(d), left(nullptr), right(nullptr) {}
};

class Bst {
private:
    Node *root;
    Node *current;
    int size;

    bool priv_contains(Node *root, long long key) {
        if (!root) {
            current = nullptr;
            return false;
        }

        if (root->data == key) {
            current = root;
            return true;
        } else if (key < root->data) {
            return priv_contains(root->left, key);
        } else {
            return priv_contains(root->right, key);
        }
    }

    bool priv_insert(Node *&root, int val) {
        if (!root) {
            root = new Node(val);
            current = root;
            size++;
            return true;
        }

        if (val == root->data) {
            current = root;
            return false; // ignore duplicates
        } else if (val < root->data) {
            return priv_insert(root->left, val);
        } else {
            return priv_insert(root->right, val);
        }
    }

    Node *find_min(Node *root) {
        while (root && root->left) {
            root = root->left;
        }
        return root;
    }

    bool priv_erase(Node *&root, int key) {
        if (!root) {
            return false;
        }

        if (key < root->data) {
            return priv_erase(root->left, key);
        } else if (key > root->data) {
            return priv_erase(root->right, key);
        } else {
            // Case 1: leaf
            if (!root->left && !root->right) {
                delete root;
                root = nullptr;
            }
            // Case 2: only right child
            else if (!root->left) {
                Node *temp = root;
                root = root->right;
                delete temp;
            }
            // Case 3: only left child
            else if (!root->right) {
                Node *temp = root;
                root = root->left;
                delete temp;
            }
            // Case 4: two children
            else {
                Node *successor = find_min(root->right);
                root->data = successor->data;
                return priv_erase(root->right, successor->data);
            }

            size--;
            return true;
        }
    }

    void priv_print(Node *root) const {
        if (!root) {
            return;
        }

        priv_print(root->left);
        cout << root->data << " ";
        priv_print(root->right);
    }

    void priv_clear(Node *root) {
        if (!root) {
            return;
        }

        priv_clear(root->left);
        priv_clear(root->right);
        delete root;
    }

public:
    Bst() : root(nullptr), current(nullptr), size(0) {}

    ~Bst() {
        priv_clear(root);
    }

    const char *name() const { return "BST"; }

    bool contains(int key) {
        return priv_contains(root, key);
    }

    bool insert(int key) {
        return priv_insert(root, key);
    }

    bool erase(int key) {
        return priv_erase(root, key);
    }

    void print() const {
        priv_print(root);
        cout << '\n';
    }

    int get_size() const {
        return size;
    }
};