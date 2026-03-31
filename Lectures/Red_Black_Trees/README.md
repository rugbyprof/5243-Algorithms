## Red Black Trees - Overview with Slides

#### Due: N/A

### Files

|     | Name                                                 | Description                            |
| :-: | :--------------------------------------------------- | :------------------------------------- |
| 01  | [RedBlack Trees](01_RedBlack-Trees.ppt)              | Power point presentation               |
| 02  | [Insertion Handout](02-RB_Tree_Insertion_Handout.md) | Red Black tree rules                   |
| 03  | [Tree Rotations](03-Tree_Rotations.md)               | cpp code for left and right rotations. |
| 04  | [Worksheet](04-RB_Worksheet.md)                      | Practice problems.                     |
| 05  | [Rules Walkthrough](05-RB_Rules_Walkthrough.md)      | Rules checklist + per-case walkthroughs from empty tree. |

---

## Red-Black Trees: Overview

### What They Are

A Red-Black (RB) tree is a self-balancing BST where every node carries a **color bit** (red or black) that encodes balance constraints. The five invariants:

1. Every node is red or black
2. The root is black
3. Every `NULL` leaf is black
4. No two consecutive red nodes (a red node's parent must be black)
5. Every path from any node to its descendant `NULL` leaves has the **same number of black nodes** (black-height)

These rules together guarantee the tree's height is at most **2 log(n+1)**, keeping all operations O(log n).

---

### Similarities to AVL Trees (and Other Self-Balancing BSTs)

| Property | Red-Black | AVL | B-Tree / 2-3-4 | Splay |
|---|---|---|---|---|
| O(log n) search | Yes | Yes | Yes | Amortized |
| O(log n) insert/delete | Yes | Yes | Yes | Amortized |
| Uses rotations | Yes | Yes | No | Yes |
| Stores balance metadata per node | Color bit | Height/BF | — | — |
| Worst-case height | 2 log n | 1.44 log n | — | O(n) |

All self-balancing BSTs share the same core contract: **maintain a height bound after every mutation by restructuring the tree**. The structural operations (rotations, recoloring/rebalancing) differ, but the motivation is identical.

**RB trees are actually isomorphic to 2-3-4 trees** — every valid RB tree maps 1:1 to a 2-3-4 B-tree. A black node with red children corresponds to a 3- or 4-node. This is the deepest conceptual link across balancing schemes.

---

### RB vs AVL: The Core Trade-off

#### AVL is More Strictly Balanced

AVL enforces that for every node, `|height(left) - height(right)| ≤ 1`. This tighter constraint means:
- **Shorter trees** (max height ~1.44 log n vs 2 log n for RB)
- **Faster lookups** on average — fewer comparisons

#### But RB Trees Pay Less on Mutations

The looser RB invariants mean **fewer rotations per insert or delete**:

| Operation | RB Tree | AVL Tree |
|---|---|---|
| Insert rotations (worst case) | **2** | O(log n) |
| Delete rotations (worst case) | **3** | O(log n) |
| Recoloring (RB) / rebalancing passes (AVL) | O(log n) | O(log n) |

After an RB insertion, at most 2 rotations are ever needed — the rest is just recoloring up the tree. AVL deletions can trigger a rotation at every ancestor all the way to the root.

---

### Why RB Trees Are Preferred in Practice

**1. Write-heavy workloads**
Real-world data structures see far more insertions and deletions than pure lookups. The cheaper mutation cost of RB trees wins on the workload that actually matters.

**2. Easier to implement correctly (especially deletion)**
AVL deletion requires carefully tracking and propagating balance factors back up the tree. RB deletion (while non-trivial) has a fixed set of cases that can be enumerated and handled without counting heights.

**3. Persistent / functional data structures**
RB trees compose better in functional/persistent settings because the rebalancing is more localized — fewer nodes need to be copied on a path update.

**4. Used in every major systems library**
- Linux kernel `rbtree` — scheduler, memory manager, file system
- C++ `std::map` / `std::set` (virtually all implementations)
- Java `TreeMap` / `TreeSet`
- Python's `sortedcontainers` internals
- `epoll` and `nginx` timer wheels

AVL trees do appear, but mostly in **read-heavy / database index** contexts (e.g., in-memory query caches) where the tighter height bound pays off.

---

### When AVL Wins

- **Read-to-write ratio is very high** — the shorter AVL height pays off when lookups dominate
- **Predictable, cache-friendly access patterns** — tighter balance = fewer cache misses on deep trees
- **Teaching** — AVL's balance factor is easier to reason about conceptually

---

### Rotation Review

The two building blocks used in both AVL and RB trees:

```
Left Rotation:             Right Rotation:
    x                           y
     \           →            /
      y                      x
```

The same rotation code is shared between both tree types — the difference is purely in *when* and *how many times* they're triggered.

---

### Summary

RB trees sacrifice a small amount of search performance (slightly taller trees than AVL) in exchange for **significantly cheaper writes**. Since most real applications are write-heavy and lookups are still O(log n), this trade-off almost always wins. That's why the Linux kernel, the C++ STL, and Java all chose RB over AVL.
