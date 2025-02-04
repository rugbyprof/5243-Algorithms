# **Validating "An Empirical Study of Insertion and Deletion in Binary Search Trees"**

## **Objective**

The goal of this assignment is to replicate and validate the findings from the paper _"An Empirical Study of Insertion and Deletion in Binary Search Trees"_ by Jeffrey L. Eppinger. Specifically, students will implement the described experimental setup and analyze whether the results hold under modern computational conditions.

## **Background**

The paper examines the impact of **random insertions and deletions** on the **internal path length (IPL)** of **random binary search trees (BSTs)**. The key claims are:

1. **Repeated insertions and asymmetric deletions** cause the BST to become more unbalanced, eventually leading to IPL values worse than those of a purely random tree.
2. **Repeated insertions and symmetric deletions** tend to improve tree balance, resulting in IPL values better than a random tree.
3. The expected IPL follows a well-defined pattern that changes with increasing insertion/deletion (I/D) pairs.
4. The behavior of IPL after insertions and deletions does not align with purely theoretical expectations.

## **Tasks**

Your task is to implement the BST insertion and deletion algorithms as described in the paper, conduct the same experiment using a large number of I/D pairs, and analyze whether the findings hold.

### **Part 1: Implementation**

1. **Implement a BST** that supports:
   - Random **insertions** of unique values.
   - **Asymmetric deletion** (always replacing a deleted node with its **successor**).
   - **Symmetric deletion** (alternating between replacement by **successor** and **predecessor**).
2. **Compute the Internal Path Length (IPL)**:
   - IPL is the sum of the depths of all nodes in the BST.
   - Implement a function to compute IPL at any point in the experiment.

### **Part 2: Experimental Setup**

1. **Generate random BSTs**:

   - Start with trees of size `n = {64, 128, 256, 512, 1024, 2048}`.
   - Populate each tree using **random insertions**.

2. **Perform Insertion/Deletion (I/D) Cycles**:

   - Apply a sequence of I/D pairs.
   - For each step, ensure that the BST maintains a size of `n`.
   - Run **asymmetric deletion** trials.
   - Run **symmetric deletion** trials.

3. **Gather IPL Data**:
   - Compute IPL **before and after each batch** of I/D pairs.
   - Repeat experiments multiple times (`≥ 50 runs per configuration`).
   - Compare IPL values across different tree sizes and deletion methods.

### **Part 3: Analysis and Reporting**

1. **Visualize IPL Trends**:

   - Plot IPL as a function of the number of I/D pairs.
   - Compare IPL growth across different deletion strategies.
   - Identify points where IPL worsens (asymmetric deletion) or improves (symmetric deletion).

2. **Compare Findings with the Paper**:
   - Does asymmetric deletion cause BSTs to become "worse than random"?
   - Does symmetric deletion improve balance?
   - Are your results consistent with the paper’s empirical trends?
3. **Discuss Observations**:
   - Any discrepancies between your results and the paper?
   - How might modern computational differences (e.g., better random number generators, different memory management) influence the outcomes?
   - Propose any theoretical explanations for your findings.

## **Bonus Challenge** (Optional)

- Implement **alternative deletion strategies** (e.g., randomly choosing successor/predecessor at runtime).
- Compare results across different **random number generation techniques**.

## Next Assignment

- Extend the experiment to **AVL trees** and compare IPL trends with a balanced tree.

## **Deliverables**

1. **Code Submission**: Well-documented implementation of BST, insert/delete functions, and IPL computation.
2. **Experimental Results**: Data tables and IPL plots from various tree sizes and deletion strategies.
3. **Analysis Report**:
   - Summary of methodology and key observations.
   - Discussion comparing findings with the paper’s claims.
   - Reflection on potential sources of variance or error.
4. All code and related documents will go in a folder called `P01` in your `Assignments` folder on your course repository.
5. Every assignment folder will have a README.md file with a summary of the assignment with links to relevant code and other documents. See [HERE](../../Resources/01-Readmees/README.md) for help with readme's.
