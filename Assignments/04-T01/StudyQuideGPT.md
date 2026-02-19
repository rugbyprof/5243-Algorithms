# Algorithms Study Guide  
**From Stacks to Heaps (a.k.a. Building the Skeleton Before the Muscles)**

---

# 1️⃣ Refresher: Stacks, Queues, and Container Foundations

## Core Concepts

### Stack
- LIFO (Last In First Out)
- Operations: `push`, `pop`, `peek`
- Used in: recursion, DFS, expression evaluation

### Queue
- FIFO (First In First Out)
- Operations: `enqueue`, `dequeue`
- Used in: BFS, scheduling

---

## List-Based vs Array-Based

| Feature              | Array-Based      | List-Based            |
| -------------------- | ---------------- | --------------------- |
| Memory               | Contiguous       | Non-contiguous        |
| Resize               | Costly (realloc) | Easy                  |
| Random Access        | O(1)             | O(n)                  |
| Insert/Delete Middle | O(n)             | O(1) if pointer known |
| Cache Friendly       | Yes              | No                    |

---

## Questions

1. Why is a stack a good model for recursion?
2. What operation makes a queue ideal for BFS?
3. Why is random access faster in arrays than linked lists?
4. What tradeoff exists between array resizing and linked list memory usage?
5. If you need frequent insertions at the front, which structure is better and why?

---

# 2️⃣ Recursion vs Iteration (Trees & Graphs Sneak In Here)

### Recursion
- Uses implicit stack (call stack)
- Clean for hierarchical structures
- Risk: stack overflow

### Iteration
- Uses explicit stack or queue
- More control over memory
- Often preferred in production

---

## Questions

1. Why are trees naturally recursive structures?
2. How can DFS be implemented iteratively?
3. What hidden data structure makes recursion work?
4. When might iteration be safer than recursion?

---

# 3️⃣ Graph Fundamentals

## Definition

$$
G = (V, E)
$$

- V = Vertices (nodes)
- E = Edges (connections)

---

## Core Vocabulary

- **Vertex**
- **Edge**
- **Weighted Edge**
- **Directed / Undirected**
- **Cycle**
- **InDegree**
- **OutDegree**
- **Source** (no incoming edges)
- **Sink** (no outgoing edges)

---

## Graph Types

| Type            | Description                           |
| --------------- | ------------------------------------- |
| Sparse          | Few edges                             |
| Dense           | Many edges                            |
| Fully Connected | Every vertex connected to every other |
| Bipartite       | Two sets, no intra-set edges          |
| Forest          | Collection of trees                   |

---

## Complexity & Max Edges

For **undirected graph**:
$$
\text{Max Edges} = \frac{n(n-1)}{2}
$$

For **directed graph**:
$$
\text{Max Edges} = n(n-1)
$$

---

## BFS vs DFS

| Algorithm | Uses  | Good For                           |
| --------- | ----- | ---------------------------------- |
| BFS       | Queue | Shortest path (unweighted)         |
| DFS       | Stack | Cycle detection, topological ideas |

---

## Questions

1. What does indegree represent?
2. Why is BFS guaranteed to find shortest path in unweighted graphs?
3. When is adjacency list better than adjacency matrix?
4. What is the space complexity of adjacency matrix?
5. Define a bipartite graph.
6. What is the maximum number of edges in a complete graph with n vertices?
7. What makes a graph a forest?

---

# 4️⃣ Trees (A Special Type of Graph)

A tree is:
- Connected
- Acyclic
- Has exactly \( n - 1 \) edges

---

## Relationship to Graphs

Every tree is a graph.  
Not every graph is a tree.

---

## Tree Properties

- Rooted structure
- Unique path between nodes
- No cycles
- Height
- Balanced vs Unbalanced

Balanced Tree:
Height ≈ \( \log n \)

---

## Traversals

### Preorder
Root → Left → Right  
Used for: copying tree

### Inorder
Left → Root → Right  
Used for: sorted order in BST

### Postorder
Left → Right → Root  
Used for: deleting tree

---

### Rebuilding a Tree

You can reconstruct a binary tree using:
- Inorder + Preorder  
OR  
- Inorder + Postorder  

---

## Questions

1. Why must a tree with n nodes have n−1 edges?
2. What traversal of a BST gives sorted order?
3. Why is postorder ideal for deleting a tree?
4. Define tree height.
5. What makes a tree balanced?
6. Why is a tree considered a graph?
7. What information is required to reconstruct a binary tree?

---

# 5️⃣ Binary Search Trees (Structure + Algorithm)

Rules:
- Left subtree < root
- Right subtree > root

Now you combine:
- Container structure (tree)
- Algorithm rule (ordering constraint)

This is your “structure + algorithm marriage.”

---

## Deleting in BST

Cases:
1. Leaf
2. One child
3. Two children → replace with inorder successor or predecessor

---

## InOrder Successor
- Smallest value in right subtree

## InOrder Predecessor
- Largest value in left subtree

---

## Questions

1. Why is search O(log n) in a balanced BST?
2. Why does deletion require special cases?
3. Define inorder successor.
4. What happens if a BST becomes skewed?

---

# 6️⃣ Array-Based Trees

Perfect for:
- Complete trees
- Binary heaps

---

## Index Formulas (0-based index)

- Parent: \( (i-1) // 2 \)
- Left Child: \( 2i + 1 \)
- Right Child: \( 2i + 2 \)

---

## Problems With Sparse Trees

- Wasted space
- Large unused array sections

---

## Questions

1. Why are array-based trees good for heaps?
2. Why are they bad for sparse trees?
3. What is the parent index formula?
4. Why must the tree be complete?

---

# 7️⃣ Binary Search (Array Context)

Requirements:
- Sorted array

---

## Complexity

- Best: O(1)
- Average/Worst: O(log n)

---

## Algorithm Insight

Each step eliminates half the search space.

---

## Generic vs Optimized

Generic:
- Recursive or iterative version

Speedups:
- Avoid overflow in midpoint:
  $$
  mid = low + (high - low) / 2
  $$

---

## Questions

1. Why must data be sorted?
2. Why is binary search logarithmic?
3. What happens if array is unsorted?
4. Why adjust midpoint formula?

---

# 8️⃣ Big Picture Progression

You’re building dependency layers:

1. Stacks & Queues (control flow tools)
2. Trees (hierarchical structure)
3. BSTs (ordering algorithm added)
4. Graphs (generalized trees)
5. Binary Search (ordered array logic)
6. Binary Heap (array-based complete tree + ordering rule)

---

# 9️⃣ Binary Heap (Priority Queue Done Correctly)

## Heap Properties

- Complete binary tree
- Parent ≥ children (max heap)
- OR Parent ≤ children (min heap)
- NOT a total ordering

---

## Complexity

| Operation   | Complexity |
| ----------- | ---------- |
| Insert      | O(log n)   |
| Remove root | O(log n)   |
| Peek        | O(1)       |
| Heapify     | O(n)       |

Yes. Heapify is O(n).  
Yes, it feels like it should be O(n log n).  
No, it is not.  
And yes, that’s the magic.

---

## Why Heapify is Powerful

Turns an arbitrary array into a heap efficiently.

Enables:
- Heap Sort
- Efficient priority queue

---

## Why Not Just Use Linked List?

Priority queue via linked list:
- Insert: O(n)
- Remove: O(1) or vice versa

Heap:
- Balanced tradeoff
- O(log n) both ways

---

## Questions

1. Why is a heap not totally ordered?
2. Why must it be complete?
3. Why is heapify O(n)?
4. Why is a heap better than a linked list priority queue?
5. What property allows array-based implementation?

---

# 10️⃣ Master Concept Questions (Great Exam Converters)

1. Explain the difference between a data structure and an algorithm.
2. Why is a BST both a structure and an algorithm?
3. Why does BFS require a queue?
4. Why does DFS require a stack?
5. Why does a heap not guarantee sorted order?
6. Why does binary search pair naturally with arrays?
7. Why do trees bridge the conceptual gap between stacks and graphs?
8. Why does completeness make heaps efficient?

---

# 🧠 The Unifying Insight

> Containers have strengths and weaknesses.  
> Algorithms impose rules on containers to exploit those strengths.

Stacks → Control flow  
Queues → Level exploration  
Trees → Hierarchy  
BST → Order enforcement  
Binary Search → Ordered arrays  
Heap → Ordered priority without total sorting  

---


```yaml
title: "Algorithms Concept Dependency Diagram"
course: "Algorithms"
author: "ChatGPT for Terry"
purpose: "Visual hierarchy showing how core data structures and algorithms build toward Binary Heaps"
format: "Layered dependency + graph interpretation"
```

# 🧠 Algorithms Concept Dependency Diagram  
*(a.k.a. The Skeleton Under Your Semester)*

Below is the **structural dependency map** of your progression.  
This isn’t just a topic list — it’s the “why this before that” architecture.

---

# 🔷 Layer 0 — Primitive Containers (Control Flow Backbone)

```
        Arrays
           |
     Linked Lists
           |
     ----------------
     |              |
   Stack          Queue
```

### Why this layer comes first:
- Arrays and lists define **memory model tradeoffs**
- Stack and Queue define **behavioral discipline**
- These are the tools recursion, DFS, BFS, and heaps depend on

---

# 🔷 Layer 1 — Traversal Logic (Algorithm Discipline)

```
         Stack  →  DFS
         Queue  →  BFS
```

This is your first **container → algorithm pairing**.

Students realize:
> The algorithm depends on the container discipline.

---

# 🔷 Layer 2 — Hierarchical Structure

```
                Trees
                  |
         -------------------
         |                 |
    Recursive          Iterative
    Traversal          Traversal
```

Why here?

Because:
- DFS = Tree traversal
- BFS = Level traversal
- Recursion = implicit stack

Trees are where:
- Structure becomes visible
- Recursion becomes intuitive

---

# 🔷 Layer 3 — Ordering Constraint Added

```
              Trees
                |
         Binary Trees
                |
         Binary Search Trees
```

This is the moment you introduce:

> Structure + Algorithm = Data Structure

BST is no longer “just a tree”  
It is a **tree with ordering rules**.

Now binary search suddenly makes sense.

---

# 🔷 Layer 4 — Ordered Arrays

```
     Arrays  →  Sorted Arrays  →  Binary Search
```

Binary Search is the array-world equivalent of BST search.

Now students can compare:

| Structure    | Search   |
| ------------ | -------- |
| Sorted Array | O(log n) |
| Balanced BST | O(log n) |
| Linked List  | O(n)     |

Boom. Design tradeoffs.

---

# 🔷 Layer 5 — Graph Generalization

```
            Graphs (G = (V,E))
                |
      --------------------------
      |                        |
    Trees                 General Graphs
```

Key insight:

> A tree is a special case of a graph.

So now:
- BFS/DFS are no longer tree-only
- They scale to general connectivity

---

# 🔷 Layer 6 — Complete Trees + Array Mapping

```
        Binary Trees
              |
      Complete Binary Trees
              |
         Array Mapping
```

Now we can use:

- Parent: (i-1)//2
- Left: 2i+1
- Right: 2i+2

This only works because:
> The tree is complete.

---

# 🔷 Layer 7 — Heap Property (Local Ordering)

```
       Complete Binary Tree
                +
         Local Ordering Rule
                =
            Binary Heap
```

Key distinction:

- BST → Total ordering
- Heap → Local ordering

Students must see this difference clearly.

---

# 🔷 Layer 8 — Priority Queue Realized

```
      Binary Heap
           |
     Priority Queue
```

Compare:

| Implementation | Insert   | Remove   |
| -------------- | -------- | -------- |
| Linked List PQ | O(n)     | O(1)     |
| Heap PQ        | O(log n) | O(log n) |

Now efficiency story lands.

---

# 🔷 Layer 9 — Heapify (The Power Move)

```
     Arbitrary Array
           |
        Heapify
           |
      Binary Heap
           |
       Heap Sort
```

Heapify is the conceptual payoff:
- Not O(n log n)
- O(n)
- Enables in-place sorting

---

# 📌 The Full Dependency Flow (Compressed View)

```
Arrays → Lists
   ↓
Stacks / Queues
   ↓
DFS / BFS
   ↓
Trees
   ↓
Binary Trees
   ↓
BST  ←→ Binary Search (Sorted Arrays)
   ↓
Complete Binary Trees
   ↓
Array Index Formulas
   ↓
Heap Property
   ↓
Binary Heap
   ↓
Priority Queue
   ↓
Heapify → Heap Sort
```

---

# 🎯 The Conceptual Through-Line

What students should internalize:

1. Containers define constraints.
2. Algorithms exploit those constraints.
3. Add rules → gain efficiency.
4. Efficiency requires structural discipline.
5. Completeness enables array mapping.
6. Local ordering enables priority behavior.
7. Total ordering enables binary search.

---

# 🧠 The Meta Insight

The entire semester builds toward this realization:

> You don't get efficiency for free.
> You get it by imposing structure.

---

Why do front and tail pointers not improve insertion complexity of a sorted linked list priority queue?

---

## Cheat Sheets

<a href="https://images2.imgbox.com/28/6d/JrAyZA2z_o.jpg"><img src="https://images2.imgbox.com/28/6d/JrAyZA2z_o.jpg" width="300"></a>

<a href="https://images2.imgbox.com/a5/36/z6BvQv7x_o.png"><img src="https://images2.imgbox.com/a5/36/z6BvQv7x_o.png" width="300"></a>



