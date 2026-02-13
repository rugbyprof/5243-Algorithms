# 🧠 Algorithms Study Guide  

**Or: How to Stop Treating Big-O Like a Vibe Check**

- If this document feels long, good.  
- If it feels interconnected, *excellent*.  
- If you’re hoping to memorize your way through it — I regret to inform you that algorithms notice.

This handout is doing **three jobs at once**:

1. A **refresher** (you’ve seen these parts before… allegedly)
2. A **concept map** (how things actually relate)
3. A **reality check** (performance is not a suggestion)

---

## Part 0 — Ground Rules (Read Before Skipping Ahead)

- **Data structures do not do anything by themselves**
- **Algorithms without a container are just ideas**
- **Big-O is not about speed — it’s about growth**
- If you say “it’s fast enough,” you have already lost the argument

---

## Part 1 — Refresher (The Backbone Stuff You’re Supposed to Know)

### Stacks
**Definition:**  
LIFO — *Last In, First Out*

**Canonical operations:**  
- `push`
- `pop`
- `top / peek`

**Implementations:**
- Array-based (vector)
- List-based (linked list)

**Complexity:**
- Push: **O(1)**
- Pop: **O(1)**

**Invariants (say this out loud):**  
> The only accessible element is the most recently added one.

Stacks are not clever.  
They are **predictable**, which is why they are everywhere.

---

### Queues
**Definition:**  
FIFO — *First In, First Out*

**Canonical operations:**  
- `enqueue`
- `dequeue`

**Implementations:**
- Circular array
- Linked list

**Complexity (done right):**
- Enqueue: **O(1)**
- Dequeue: **O(1)**

**Reality check:**  
Using a plain array and shifting elements = **algorithmic malpractice**

---

### List-Based vs Array-Based (The First Real Tradeoff)

| Feature                | Array-Based | List-Based                     |
| ---------------------- | ----------- | ------------------------------ |
| Memory locality        | Excellent   | Terrible                       |
| Random access          | O(1)        | O(n)                           |
| Insert/remove (middle) | O(n)        | O(1) *if you’re already there* |
| Cache friendly         | Yes         | No                             |

#### **Translation:**  

Arrays are fast *when structure is stable*.  
Lists are flexible *when movement is frequent*.

---

## Part 2 — Iteration vs Recursion (This Will Come Back Later)

### Iteration
- Explicit control
- Explicit state
- Uses loops
- Usually stack-safe

### Recursion
- Implicit stack
- Elegant
- Dangerous if misused
- Tree-shaped problems **want** recursion

**Key insight:**  
> Recursion isn’t magic — it’s a stack you didn’t write.

---

## Part 3 — Trees (Graphs That Behave)

### Tree Definition
A tree is:
- A **connected**
- **Acyclic**
- Directed or undirected graph
- With **n − 1 edges** for **n nodes**

If you have more edges, congratulations — it’s a graph now.

---

### Trees as Graphs
- Trees ⊂ Graphs
- All trees are graphs
- Not all graphs are trees
- Trees impose **structure**
- Graphs allow **chaos**

---

### Core Tree Properties

- **Root**
- **Parent / Child**
- **Leaf**
- **Height**: longest root-to-leaf path
- **Path**: sequence of connected nodes

**Balanced tree (definition that matters):**
> Height grows logarithmically with number of nodes.

---

### Tree Complexity (Binary Trees)

| Operation | Balanced | Worst Case |
| --------- | -------- | ---------- |
| Search    | O(log n) | O(n)       |
| Insert    | O(log n) | O(n)       |
| Delete    | O(log n) | O(n)       |

That “worst case” is a linked list wearing a disguise.

---

### Tree Traversals (You Will Be Asked This)

- **Preorder** (Root, Left, Right)
- **Inorder** (Left, Root, Right)
- **Postorder** (Left, Right, Root)

**Why they exist:**
- Preorder → structure first
- Inorder → sorted order (BST only)
- Postorder → safe deletion

**Critical exam question:**  
> Which traversal(s) let you reconstruct a binary tree?

Answer:
- Inorder **plus** Preorder  
- Inorder **plus** Postorder  
- Inorder alone is useless (fight me)

---

### Deleting a Node (BST Reality)

Cases:
1. Leaf → delete
2. One child → promote child
3. Two children → chaos

**Solution tools:**
- Inorder successor (smallest right subtree)
- Inorder predecessor (largest left subtree)

This is where people stop hand-waving and start sweating.

---

## Part 4 — Array-Based Trees (When Shape Matters)

### Why Sparse Trees Are a Problem
- Array indices explode
- Memory waste
- Cache sadness

### When Array-Based Trees Are Good
- **Complete trees**
- **Binary heaps**
- When structure is guaranteed

### Index Formulas (0-based)

- Parent: `(i - 1) / 2`
- Left child: `2i + 1`
- Right child: `2i + 2`

If you memorize nothing else — memorize this.

---

## Part 5 — Binary Search (The Gateway Algorithm)

### Preconditions
- Data must be **sorted**
- Random access required

### Complexity
- Time: **O(log n)**
- Space: **O(1)** iterative, **O(log n)** recursive

### Why It Matters
- Pairs perfectly with arrays
- Mirrors BST behavior
- Teaches divide-and-conquer thinking

Binary search on unsorted data is **confidence without justification**.

---

## Part 6 — Graphs (Where Structure Goes to Die)

### Formal Definition
`G = (V, E)`

- `V`: vertices
- `E`: edges

### Core Concepts
- Directed vs Undirected
- Weighted edges
- Degree
  - In-degree
  - Out-degree
- Source / Sink
- Cycles
- Paths

### Representations

| Representation   | Space    | Traversal        |
| ---------------- | -------- | ---------------- |
| Adjacency Matrix | O(V²)    | Fast edge lookup |
| Adjacency List   | O(V + E) | Fast traversal   |

Sparse graph → list  
Dense graph → matrix  

---

### BFS vs DFS (Not the Same, Stop Saying That)

**Breadth-First Search**
- Uses a **queue**
- Level-by-level
- Shortest path (unweighted)

**Depth-First Search**
- Uses a **stack**
- Goes deep first
- Cycle detection
- Topological flavor

Both:
- Time: **O(V + E)**

---

### Graph Types You’re Expected to Recognize
- Sparse
- Dense
- Fully connected
- Bipartite
- Forest (a bunch of trees pretending not to know each other)

---

## Part 7 — The Big Picture (This Is the Point)

### The Progression (On Purpose)

1. Stacks & Queues  
2. Trees  
3. Binary Trees (structure rules)
4. Binary Search Trees (structure + ordering algorithm)
5. Graphs (trees with commitment issues)
6. Array vs List tradeoffs
7. Binary Search (algorithm meets structure)
8. Heaps (priority queues done right)

This is not random.  
This is scaffolding.

---

## Part 8 — Heaps (Where It All Pays Off)

### Heap Properties
- Complete binary tree
- Parent dominates children (min or max)
- **No total ordering**

### Why Heaps Matter
They implement **priority queues** efficiently.

### Complexity

| Operation | Complexity |
| --------- | ---------- |
| Insert    | O(log n)   |
| Remove    | O(log n)   |
| Heapify   | O(n)       |

Yes — heapify is **O(n)**.  
No — that is not a typo.  
Yes — you should be suspicious until you understand why.

---

### Why Arrays Work So Well Here
- Complete tree
- No wasted indices
- Perfect cache behavior

This is where theory and hardware stop fighting.

---

## Final Takeaway (Read This Again Before Exams)

- Algorithms don’t exist in isolation
- Containers shape performance
- Structure determines complexity
- Big-O tells you **how badly things scale when you’re wrong**

If something feels “obvious” now, good.  
It wasn’t obvious when this field was invented.

That means you’re learning it **correctly**.
