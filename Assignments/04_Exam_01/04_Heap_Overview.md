# 🧱 Binary Heaps  
**Or: How to Build a Priority Queue That Doesn’t Embarrass You**

If Binary Search Trees are about **ordering**,  
Binary Heaps are about **urgency**.

They answer one question extremely well:

> “Who should go next?”

Not:
- “What’s the smallest?”
- “What’s the largest?”
- “What’s everything in order?”

Just:
👉 **Next.**

---

## Part 1 — What a Binary Heap *Is* (And Is Not)

### Definition
A **binary heap** is a:

- **Complete binary tree**
- With a **heap-order property**
- Usually implemented using an **array**

Two flavors:

- **Max-Heap**: parent ≥ children  
- **Min-Heap**: parent ≤ children  

---

### What a Heap Is *Not*

Let’s clear this up early:

❌ Not a Binary Search Tree  
❌ Not fully sorted  
❌ Not good for arbitrary search  
❌ Not “basically a tree but faster”  

✅ Extremely good at:
- Finding max or min
- Inserting priorities
- Removing highest-priority elements

---

## Part 2 — The Two Rules (Tattoo These Somewhere)

### Rule 1: Shape Property (Non-Negotiable)
The heap is a **complete** binary tree.

That means:
- Every level is full
- Except possibly the last
- And nodes fill left-to-right

This rule is why heaps work **beautifully in arrays**.

---

### Rule 2: Heap Property
Depending on heap type:

- **Max-Heap**:  
  `parent ≥ left child`  
  `parent ≥ right child`

- **Min-Heap**:  
  `parent ≤ left child`  
  `parent ≤ right child`

That’s it.

No promises about siblings.  
No promises about subtrees.  
No total ordering.

This is intentional.

---

## Part 3 — Why Heaps Are Array-Based (On Purpose)

Binary heaps are almost always implemented with arrays.

Why?

Because for a **complete binary tree**, indices do all the work.

### Index Formulas (0-based indexing)

Let `i` be the index of a node:

- **Parent**:  
  `(i - 1) // 2`

- **Left Child**:  
  `2i + 1`

- **Right Child**:  
  `2i + 2`

No pointers.  
No memory allocation per node.  
No cache misery.

This is not a convenience — it’s a **design feature**.

---

## Part 4 — Core Heap Operations (The Good Stuff)

### 1. Insert

**Steps:**
1. Place new element at the end of the array
2. “Bubble up” (heapify-up / sift-up)
3. Swap with parent until heap property is restored

**Time Complexity:**  
- **O(log n)** (height of the tree)

**Why:**  
You only move up one level at a time.

---

### 2. Peek (Find Min / Max)

- Return element at index `0`

**Time Complexity:**  
- **O(1)**

This is the entire reason heaps exist.

---

### 3. Remove Min / Max

**Steps:**
1. Swap root with last element
2. Remove last element
3. “Bubble down” (heapify-down / sift-down)

**Time Complexity:**  
- **O(log n)**

Again: height matters, not size.

---

### 4. Heapify (a.k.a. “Why This Data Structure Is Cool”)

**Heapify** turns an arbitrary array into a heap.

**Time Complexity:**  
- **O(n)**

Yes.  
Not `O(n log n)`.  
Actually `O(n)`.

This fact alone has launched a thousand exam questions.

---

### Why Heapify Is O(n) (High-Level Intuition)

- Most nodes are near the bottom
- Bottom nodes have little or no work
- Only a few nodes are near the root
- Work decreases geometrically

Translation:
> The expensive work happens rarely.

---

## Part 5 — Heaps as Priority Queues

### Abstract Data Type: Priority Queue

Operations:
- Insert(item, priority)
- Remove highest priority
- Peek highest priority

### Implementations Compared

| Structure            | Insert   | Remove Max/Min | Peek |
| -------------------- | -------- | -------------- | ---- |
| Unsorted Linked List | O(1)     | O(n)           | O(n) |
| Sorted Linked List   | O(n)     | O(1)           | O(1) |
| Binary Heap          | O(log n) | O(log n)       | O(1) |

This is why heaps win.

They don’t dominate **one** operation —  
they dominate the **overall workload**.

---

## Part 6 — Why Heaps Beat Linked Lists (Blunt Version)

### Linked List Priority Queue Problems

- Either:
  - Cheap insert, expensive removal
  - OR cheap removal, expensive insert
- Poor cache locality
- Pointer overhead
- Linear scans everywhere

They work.  
They’re just… bad at scale.

---

### Heap Advantages (Why We Like Them)

- Predictable performance
- Logarithmic operations
- Cache-friendly
- Simple invariants
- Clean mental model

Heaps don’t pretend to be elegant.  
They are **effective**.

---

## Part 7 — Heaps vs BSTs (Stop Confusing These)

| Feature              | Heap | BST |
| -------------------- | ---- | --- |
| Sorted traversal     | ❌    | ✅   |
| Fast min/max         | ✅    | ❌   |
| Arbitrary search     | ❌    | ✅   |
| Structure guaranteed | ✅    | ❌   |
| Array-based          | ✅    | ❌   |

**Use a heap when:**
- You only care about “next”
- Order beyond that is irrelevant

**Use a BST when:**
- You care about relative ordering
- You need search + traversal

---

## Part 8 — Heap Sort (Brief but Important)

### Heap Sort Outline
1. Heapify the array
2. Repeatedly remove max (or min)
3. Place it at the end

**Complexity:**
- Time: **O(n log n)**
- Space: **O(1)** (in-place)

Heap sort is:
- Deterministic
- In-place
- Not stable
- Usually not fastest in practice

But it is **beautifully principled**.

---

## Part 9 — Common Student Misconceptions

❌ “A heap is sorted”  
❌ “Heaps replace BSTs”  
❌ “Heapify is O(n log n)”  
❌ “You can binary search a heap”

If you think any of those are true, pause and re-read Part 2.

---

## Final Takeaway (Read This Slowly)

Binary heaps are powerful because they:

- Enforce **just enough order**
- Avoid unnecessary guarantees
- Align perfectly with hardware
- Deliver consistent performance

They are not fancy.  
They are not flexible.  

They are **honest**.

And in algorithms, honesty scales.