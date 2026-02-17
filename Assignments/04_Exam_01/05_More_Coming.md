## 1️⃣ “Algorithm vs Data Structure” — A Reality Check Handout  
**(This one pays dividends all semester)**

### Why This Matters

Students *say* they understand the difference.  
They absolutely do not.

They still think:
- “Binary search tree” is one thing
- “Heap” is just a different tree
- “Graph” magically implies BFS/DFS

This handout nails the distinction *once* so you don’t have to keep re-teaching it.

### Core Sections
- What a **container** guarantees
- What an **algorithm** assumes
- Why the *same algorithm* behaves differently on different containers
- Insert / Delete / Search as **policies**, not operations

### Killer Table
| Container   | Algorithm         | Works? | Why / Why Not |
| ----------- | ----------------- | ------ | ------------- |
| Array       | Binary Search     | ✅      | Random access |
| Linked List | Binary Search     | ❌      | No indexing   |
| Tree        | DFS               | ✅      | Hierarchical  |
| Graph       | Inorder Traversal | ❌      | No left/right |

### Where It Fits
Right after:
- stacks & queues refresher
- before trees

This becomes the **mental lens** for everything else.

---

## 2️⃣ “When Recursion Is a Feature vs a Liability”  
**(Short, brutal, clarifying)**

### Why This Matters
Students think recursion is:
- either “elegant magic”
- or “evil forbidden syntax”

Neither is correct.

### Focus
- When recursion **matches the shape of the data**
- When iteration is safer
- When recursion is just a stack cosplay

### Includes
- Tree traversal (good recursion)
- Graph traversal (danger recursion)
- Binary search (either)
- DFS (recursive *or* iterative stack)

### One Key Rule (Students Remember This)
> If the data structure is recursive, the algorithm probably should be too.

### Where It Fits
Between:
- Recursion vs Iteration
- Trees & Graphs

---

## 3️⃣ “Traversal Intent Cheat Sheet” (Graphs + Trees Together)  
**(You already did trees — this completes the set)**

### Why This Matters
Students memorize traversal names without **intent**.

This handout forces them to answer:
> “Why this traversal and not the other?”

### Contents
- DFS vs BFS
- Stack vs Queue
- Shortest path vs reachability
- Cycle detection
- Tree vs Graph traversal differences

### Key Comparison Table
| Goal            | Traversal          |
| --------------- | ------------------ |
| Sorted output   | Inorder (BST only) |
| Shortest path   | BFS                |
| Cycle detection | DFS                |
| Tree deletion   | Postorder          |
| Level-by-level  | BFS                |

### Where It Fits
Right after:
- Graphs intro
- BFS/DFS discussion

---

## 4️⃣ “Binary Search: Algorithm vs Assumption”  
**(This one quietly fixes a LOT of confusion)**

### Why This Matters
Students think binary search is:
- about speed

It’s actually about **assumptions**.

### Focus
- Preconditions (sorted + random access)
- Why violating assumptions breaks correctness
- Binary search vs BST search
- Iterative vs recursive costs

### Great Trick Question
> “What’s the complexity of binary search on a linked list?”

Correct answer:
- **O(n)** (because access dominates)

### Where It Fits
Right before:
- heaps
- priority queues

---

## 5️⃣ “Tree vs Graph — Same DNA, Different Rules”  
**(Conceptual unifier handout)**

### Why This Matters
You *explicitly* say you introduce graphs to explain trees.

This handout formalizes that move.

### Contents
- Tree as a constrained graph
- Why trees are easier
- What breaks when cycles exist
- Why traversal logic suddenly needs visited sets

### One-Line Truth Bomb
> Trees don’t need cycle detection because they promised not to lie.

### Where It Fits
Immediately after:
- graph definitions
- before heavy BFS/DFS

---

# 🧪 Practice Test Question Sets (Low Effort, High Signal)

These are **thinking questions**, not coding exercises.

---

## A️ “Choose the Container” Mini Exam (10–15 minutes)

Give 4 scenarios.  
Students must choose:
- Container
- Algorithm
- Complexity
- One-sentence justification

Example:
> You must repeatedly remove the highest-priority item from a dynamic dataset.

Wrong answers become obvious *fast*.

---

## B️ “What Breaks If…” Questions  
**(These are evil and effective)**

Examples:
- What breaks if a heap isn’t complete?
- What breaks if a BST becomes unbalanced?
- What breaks if you BFS without a queue?
- What breaks if you DFS without a visited set?

These expose **structural dependence**, not syntax.

---

## C️ “Spot the Lie” (Students Love/Hate This)

Give 5 statements:
- 3 true
- 2 subtly false

Examples:****
- “Heapify is O(n log n)” ❌
- “Inorder traversal always sorts” ❌
- “DFS always uses recursion” ❌

Require justification.

---

## D️ “Same Data, Different Guarantees”

Ask:
> You store the same data in:
> - array
> - BST
> - heap
>
> What operations improve? What get worse?

This reinforces **tradeoffs**, which is your throughline.

