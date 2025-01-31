## Assignment 3 - BST Delete

#### Due: 02-04-2025 (Tuesday)

# **Assignment: Implementing Delete in a Binary Search Tree (BST)**

## **Objective**

Your task is to extend the Binary Search Tree (BST) implementation provided in the following Replit instance which I downloaded here:

[bst.cpp](./bst.cpp)

Specifically, you will implement a **delete** method for the BST. You may refer to any external sources to understand how to implement deletion in a BST, but you must integrate the method into the provided BST class here: [bst.cpp](./bst.cpp)

## **Key Learning Points**

1. **Understanding Node Deletion Cases:**
   - Deleting a **leaf node** (node with no children).
   - Deleting a **node with one child**.
   - Deleting a **node with two children**.
2. **Maintaining BST Order:**
   - Ensuring that the BST remains correctly structured after deletion.
3. **Choosing a Replacement Value:**
   - When deleting an inner node with two children, two values can be used as replacements:
     - **Inorder Successor** (smallest value in the right subtree)
     - **Inorder Predecessor** (largest value in the left subtree)
   - Discuss which option you chose and why.

## **Assignment Requirements**

1. **Ensure that your delete method correctly handles all deletion cases.**
2. **Test your delete function thoroughly** with various BST structures.
3. **Write a short explanation (minimum 200 words)** covering:
   - The cases you handled for deletion.
   - The logic behind choosing a replacement value for nodes with two children.
   - Any challenges you faced while implementing deletion.

## **Deliverables**

- Create a folder called `A03` and place it into your `assignments` folder.
- That folder should include:
  - your altered modified **BST class code** with the `delete` method included in a file called bst.cpp
  - Provide a **README.md** file with a written explanation describing the key learning points mentioned above.
- In addition your bst.cpp should contain a main function that incorporates test cases demonstrating the correctness of your delete method. What does this mean? You should prove that your code works with an empty tree, a tree with one node, a tree with many nodes, a tree that has sequencial values in it (linked list), etc.. Think of every possible case and make sure your delete method works.
