# **Understanding Internal Path Length in Binary Search Trees (BSTs)**

## **Introduction**

In a **Binary Search Tree (BST)**, the **Internal Path Length (IPL)** is the sum of the depths of all **internal nodes** (non-leaf nodes). While the number of edges in any tree with **_\( n \)_** nodes is always **_\( n - 1 \)_**, the **distribution of node depths varies based on the tree’s structure**, affecting the IPL.

### **Formula for Internal Path Length**

Given a BST with internal nodes **_\( v \)_**, the **IPL** is calculated as:

$$
I(T) = \sum_{v \in \text{internal nodes}} \text{depth}(v)
$$

where:

- **Depth** of a node is the number of edges from the root to that node.
- **Internal nodes** are all nodes that have at least one child.

---

### Steps to Compute IPL

1. Traverse the BST using preorder traversal (or any traversal method that visits all internal nodes).
2. Calculate the depth of each internal node.
3. Sum up all the depths.

#### Example Calculation

**Example BST:**

```txt
         15
       /   \
      10    20
     /  \     \
    8    12    25
   / \   / \   / \
  3   9 11 14 22 27
```

#### Step 1: Identify Internal Nodes and Their Depths

| Node |  Depth   |
| :--: | :------: |
|  15  | (root) 0 |
|  10  |    1     |
|  20  |    1     |
|  8   |    2     |
|  12  |    2     |
|  25  |    2     |

#### Step 2: Sum the Depths

**_IPL = 0 + 1 + 1 + 2 + 2 + 2 = 8_**

## **Why IPL Varies Across BSTs with the Same Number of Nodes**

### **Balanced BST (Low IPL)**

**Consider a balanced BST:**

```
        4
       / \
      2   6
     / \ / \
    1  3 5  7
```

- Internal Nodes: **{4, 2, 6}**
- Depths: **0, 1, 1**
- **IPL = 0 + 1 + 1 = 2**

### **Skewed BST (High IPL)**

**Now, consider a right-skewed BST:**

```txt
    1
     \
      2
       \
        3
         \
          4
           \
            5
```

- Internal Nodes: **{1, 2, 3, 4}**
- Depths: **0, 1, 2, 3**
- **IPL = 0 + 1 + 2 + 3 = 6**

### **Observations:**

- **Balanced trees** distribute nodes evenly, leading to a lower IPL and better efficiency in BST operations.
- **Skewed trees** have higher IPL, making operations like search, insertion, and deletion inefficient.
- **Self-balancing BSTs** (e.g., **AVL Trees, Red-Black Trees**) adjust node placement to keep IPL low, ensuring **O(log n) operations**.

---

## **Recursive Calculation of IPL in C++**

Here’s a C++ program that computes the Internal Path Length of a BST:

```cpp
#include <iostream>
using namespace std;

struct Node {
    int data;
    Node* left;
    Node* right;
};

Node* createNode(int data) {
    return new Node{data, nullptr, nullptr};
}

Node* insert(Node* root, int data) {
    if (!root) return createNode(data);
    if (data < root->data)
        root->left = insert(root->left, data);
    else
        root->right = insert(root->right, data);
    return root;
}

int computeIPL(Node* root, int depth = 0) {
    if (!root) return 0;
    return depth + computeIPL(root->left, depth + 1) + computeIPL(root->right, depth + 1);
}

int main() {
    Node* root = nullptr;
    int values[] = {4, 2, 6, 1, 3, 5, 7}; // Balanced BST
    for (int v : values) root = insert(root, v);

    cout << "Internal Path Length (IPL): " << computeIPL(root) << endl;
    return 0;
}
```

### **Explanation:**

- **`insert()`** builds a BST by inserting nodes recursively.
- **`computeIPL()`** calculates the IPL by summing the depth of all internal nodes.
- This example builds a **balanced BST**, ensuring **low IPL**.

---

## **Conclusion**

- The number of **edges** in a BST is always **_\( n - 1 \)_**, but the **Internal Path Length (IPL) depends on node distribution**.
- **Balanced BSTs** have lower IPL, leading to better search and update efficiency.
- **Skewed BSTs** have higher IPL, making operations inefficient.
- **Self-balancing trees** minimize IPL, optimizing BST performance.
- The **C++ program** demonstrates how to compute IPL recursively.

Understanding **IPL and tree balancing** is crucial for designing efficient BST-based applications!
