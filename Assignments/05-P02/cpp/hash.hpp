#pragma once
#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <memory>
#include <utility>

#include "counters.hpp"
#include "structure.hpp"

// ------------------------------
// Unbalanced BST with counters
// - comparisons: key comparisons
// - structural_ops: node visits + pointer relinks
// ------------------------------
class Hash final : public Structure {
private:
    uint64_t *hash = nullptr;
    int capacity;
    Counters c_{};

    static inline uint64_t mix64(uint64_t x) {
        x += 0x9e3779b97f4a7c15ULL;
        x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
        x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
        return x ^ (x >> 31);
    }

    // Count exactly ONE key-compare per probe sequence
    int cmp_key(int x, int key) {
        c_.comparisons += 1;
        size_t idx = mix64((uint64_t)key) & (capacity - 1);
        if (x < key)
            return -1;
        if (x > key)
            return 1;
        return 0;
    }

    void destroy() {
        delete[] hash;
    }

    // structural node visit helper
    void probe_entries() { c_.structural_ops += 1; }

    // pointer relink helper (deletion rearranges pointers)
    // void relink() { c_.structural_ops += 1; }

    bool contains_impl(int x) {
        while (n) {
            visit_node();
            int r = cmp_key(x, n->data);
            if (r == 0)
                return true;
            n = (r < 0) ? n->left : n->right;
        }
        return false;
    }

    void insert_impl(int x) {
        // linear probe
    }

    // Remove a key from subtree rooted at n. Returns whether something was removed.
    bool erase_impl(Node *&n, int x) {
        if (!n)
            return false;

        visit_node();
        int r = cmp_key(x, n->data);

        if (r < 0)
            return erase_impl(n->left, x);
        if (r > 0)
            return erase_impl(n->right, x);

        // Found node to delete: n
        // Case 1: 0 children
        if (!n->left && !n->right) {
            relink();
            delete n;
            n = nullptr;
            return true;
        }

        // Case 2: 1 child
        if (!n->left || !n->right) {
            relink();
            Node *child = n->left ? n->left : n->right;
            delete n;
            n = child;
            return true;
        }

        // Case 3: 2 children
        // Replace with inorder successor (min of right subtree)
        Node *parent = n;
        Node *succ = n->right;

        // Walk to leftmost of right subtree
        while (succ->left) {
            visit_node();
            parent = succ;
            succ = succ->left;
        }

        // Copy successor's data into current node (not a pointer relink)
        // (You can count this as structural_ops if you want, but not necessary.)
        n->data = succ->data;

        // Delete successor node (which has at most one right child)
        // If successor is direct right child
        if (parent == n) {
            relink();
            parent->right = succ->right;
        } else {
            relink();
            parent->left = succ->right;
        }
        delete succ;
        return true;
    }

public:
    Hash() : capacity(0) {}
    ~Hash() override { destroy(); }
    const char *name() const override { return "BST"; }
    long long size_ = 0;

    void reset() override {
        destroy(root_);
        root_ = nullptr;
    }

    long long size() const { return size_; }

    void reset_counters() override { c_ = Counters{}; }
    Counters counters() const override { return c_; }

    void insert(int x) override {
        c_.inserts += 1;
        insert_impl(root_, x);
    }

    void erase(int x) override {
        c_.deletes += 1;
        (void)erase_impl(root_, x); // delete-missing is allowed (no-op)
    }

    bool contains(int x) override {
        c_.lookups += 1;
        return contains_impl(x);
    }
};


