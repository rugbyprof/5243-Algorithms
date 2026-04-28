```yaml
title: Skip Lists
description: Probabilistic Ordered Data Structures
slug: SkipLists
id: skip-lists
name: skip-lists
category: lecture
```

# Skip Lists

> "The simplest data structure that gives you O(log n) without making you implement rotations."

---

## The Problem: A Sorted Linked List Is Useless for Search

A sorted linked list seems like it should be good. The data is ordered. Binary search cuts search space in half at each step. So why can't we binary search a linked list?

Because binary search requires **O(1) access to the midpoint**. On a linked list, reaching node `n/2` requires traversing `n/2` pointers. Every "jump to middle" costs O(n). The sorting buys you nothing.

| Operation | Sorted Array | Sorted Linked List |
| --------- | ------------ | ------------------ |
| Search    | O(log n)     | O(n)               |
| Insert    | O(n)         | O(1) given pointer |
| Delete    | O(n)         | O(1) given pointer |

The linked list is fast at the wrong things. We want O(log n) search _and_ O(log n) insert/delete. A skip list delivers exactly this.

---

## Building the Idea: From One Express Lane to Log n

### Step 1 — One Express Lane

Take a sorted linked list and thread a second list on top that includes only every other node.

```
L1:  -∞ ──────────────> [7] ──────────────> [16] ──> +∞
L0:  -∞ --> [3] --> [7] --> [11] --> [16] --> [20] --> +∞
```

Search for 11:

- Start on L1: -∞ → 7 (ok) → 16 (too big, drop to L0 at 7)
- L0: 7 → 11 ✓

Instead of scanning all 5 nodes, we skipped directly to the neighborhood. With two levels we cut the expected search roughly in half — still O(n), but the constant drops.

### Step 2 — Generalize to log n Levels

If two levels halve the work, `log n` levels reduce it to O(log n). The **perfect skip list** over n nodes has:

- Level 0: all n nodes
- Level 1: every 2nd node → n/2 nodes
- Level 2: every 4th node → n/4 nodes
- Level k: every 2^k node → n/2^k nodes
- Top level: 1 node

```
L3:  -∞ ──────────────────────────────────────────> [25] --> +∞
L2:  -∞ ──────────────────> [12] ────────────────> [25] --> +∞
L1:  -∞ ───────> [5] ─────> [12] ────> [18] ─────> [25] --> +∞
L0:  -∞ --> [2] --> [5] --> [12] --> [15] --> [18] --> [25] --> +∞
```

Search for 15 in the perfect skip list (n = 6, ~log₂ 6 ≈ 3 levels):

| Level | At  | Next | Decision           |
| ----- | --- | ---- | ------------------ |
| L3    | -∞  | 25   | 25 > 15, drop ↓    |
| L2    | -∞  | 12   | 12 < 15, advance → |
| L2    | 12  | 25   | 25 > 15, drop ↓    |
| L1    | 12  | 18   | 18 > 15, drop ↓    |
| L0    | 12  | 15   | 15 = target ✓      |

4 comparisons for 6 nodes. Each level eliminates roughly half the remaining candidates.

### Step 3 — The Problem with "Perfect"

The perfect skip list requires you to know n in advance and to maintain exact ratios on every insert. If you insert between two level-1 nodes you may need to promote nodes all the way up the chain — the same cascading rebalancing problem that makes AVL trees painful.

**The coin flip insight:** you don't need perfect ratios. You need _expected_ ratios. If each node is independently promoted to the next level with probability p = 0.5, then:

- Expected fraction of nodes at level 1: 1/2
- Expected fraction at level 2: 1/4
- Expected fraction at level k: 1/2^k

This is statistically identical to the perfect skip list — without any coordination. On insert, just flip coins until tails. No rotations. No cascading updates. No global knowledge required.

---

## Structure

Each node stores:

- Its **value**
- An array of **forward pointers**, one per level the node participates in

A sentinel **head** node exists at every level and holds -∞. A sentinel **tail** (or null pointer) represents +∞.

```
L3:  [-∞] ──────────────────────────────────────────────> [20] --> null
L2:  [-∞] ─────────────────> [7] ─────────────────────> [20] --> null
L1:  [-∞] ─────────────────> [7] ──> [11] ──> [16] ──> [20] --> null
L0:  [-∞] ──> [3] ──────────> [7] ──> [11] ──> [16] ──> [20] --> null
```

Nodes and their levels in this example:
| Node | Levels present |
| ---- | -------------- |
| 3 | L0 only |
| 7 | L0, L1, L2 |
| 11 | L0, L1 |
| 16 | L0, L1 |
| 20 | L0, L1, L2, L3 |

The level of each node was determined by independent coin flips at insertion time. Nothing coordinates them globally.

---

## Search

### Algorithm

Start at the top-left (head, highest level). At each position: if the next node's value is less than the target, advance right. Otherwise, drop down one level. Repeat until level 0 is exhausted.

```
search(target):
    curr = head
    for level from MAX_LEVEL down to 0:
        while curr.next[level] != null and curr.next[level].val < target:
            curr = curr.next[level]
    curr = curr.next[0]
    if curr != null and curr.val == target:
        return curr
    return NOT_FOUND
```

### Walkthrough — Search for 11

Starting structure:

```
L3:  [-∞] ──────────────────────────────────────────────> [20]
L2:  [-∞] ─────────────────> [7] ─────────────────────> [20]
L1:  [-∞] ─────────────────> [7] ──> [11] ──> [16] ──> [20]
L0:  [-∞] ──> [3] ──────────> [7] ──> [11] ──> [16] ──> [20]
```

| Level | curr | next | Decision            |
| ----- | ---- | ---- | ------------------- |
| L3    | -∞   | 20   | 20 > 11, drop ↓     |
| L2    | -∞   | 7    | 7 < 11, advance →   |
| L2    | 7    | 20   | 20 > 11, drop ↓     |
| L1    | 7    | 11   | 11 < 11? No, drop ↓ |
| L0    | 7    | 11   | 11 = target ✓       |

**Found in 5 comparisons across 5 nodes.**

### Walkthrough — Search for 13 (not present)

| Level | curr | next | Decision           |
| ----- | ---- | ---- | ------------------ |
| L3    | -∞   | 20   | 20 > 13, drop ↓    |
| L2    | -∞   | 7    | 7 < 13, advance →  |
| L2    | 7    | 20   | 20 > 13, drop ↓    |
| L1    | 7    | 11   | 11 < 13, advance → |
| L1    | 11   | 16   | 16 > 13, drop ↓    |
| L0    | 11   | 16   | 16 > 13, stop      |

`curr.next[0]` = 16 ≠ 13 → **not found**.

The search landed between 11 and 16 — exactly where 13 would live if it existed.

---

## Insert

### Algorithm

Insert does two things: (1) find the **update array** — the rightmost node at each level whose value is less than the new value; (2) determine the new node's height by flipping coins; (3) splice the node in at each level up to its height.

```
random_level():
    h = 1
    while random() < p and h < MAX_LEVEL:
        h += 1
    return h

insert(val):
    update = [head] * MAX_LEVEL          ← last node < val at each level
    curr = head
    for level from MAX_LEVEL down to 0:
        while curr.next[level] != null and curr.next[level].val < val:
            curr = curr.next[level]
        update[level] = curr

    h = random_level()
    new_node = Node(val, height = h)
    for level from 0 to h - 1:
        new_node.next[level] = update[level].next[level]
        update[level].next[level] = new_node
```

### Walkthrough — Insert 13 with coins H, T (height = 2, levels 0 and 1)

**Find update array** (last node < 13 at each level):

| Level | Scan                    | update[level] |
| ----- | ----------------------- | ------------- |
| L3    | -∞ → 20 (>13), stop     | -∞ (head)     |
| L2    | -∞ → 7 (<13) → 20 (>13) | 7             |
| L1    | 7 → 11 (<13) → 16 (>13) | 11            |
| L0    | 7 → 11 (<13) → 16 (>13) | 11            |

**Coin flips:** H, T → height = 2 (node lives at L0 and L1 only).

**Splice in at L0 and L1:**

- L0: `13.next[0] = 11.next[0]` (= 16); `11.next[0] = 13`
- L1: `13.next[1] = 11.next[1]` (= 16); `11.next[1] = 13`

Levels L2 and L3 are unchanged — 13 didn't get promoted that high.

**After insert:**

```
L3:  [-∞] ──────────────────────────────────────────────────────> [20]
L2:  [-∞] ─────────────────> [7] ──────────────────────────────> [20]
L1:  [-∞] ─────────────────> [7] ──> [11] ──> [13] ──> [16] ──> [20]
L0:  [-∞] ──> [3] ──────────> [7] ──> [11] ──> [13] ──> [16] ──> [20]
```

13 is linked in at exactly the levels determined by the coin flip. Nothing else changed.

---

## Delete

### Algorithm

Delete mirrors insert: build the same update array, verify the target exists at level 0, then relink past it at every level where it appears.

```
delete(val):
    update = [head] * MAX_LEVEL
    curr = head
    for level from MAX_LEVEL down to 0:
        while curr.next[level] != null and curr.next[level].val < val:
            curr = curr.next[level]
        update[level] = curr

    target = curr.next[0]
    if target == null or target.val != val:
        return NOT_FOUND

    for level from 0 to MAX_LEVEL - 1:
        if update[level].next[level] != target:
            break                            ← target not present above this level
        update[level].next[level] = target.next[level]

    free(target)
```

### Walkthrough — Delete 16

Using the structure after inserting 13:

**Find update array** (last node < 16 at each level):

| Level | update[level] |
| ----- | ------------- |
| L3    | head (-∞)     |
| L2    | 7             |
| L1    | 13            |
| L0    | 13            |

**Verify:** `update[0].next[0]` = 16 ✓

**16 appears at L0 and L1** (check: `update[1].next[1]` = 16 ✓; `update[2].next[2]` = 20 ≠ 16, stop).

**Relink:**

- L0: `13.next[0] = 16.next[0]` (= 20)
- L1: `13.next[1] = 16.next[1]` (= 20)

**After delete:**

```
L3:  [-∞] ──────────────────────────────────────────────> [20]
L2:  [-∞] ─────────────────> [7] ─────────────────────> [20]
L1:  [-∞] ─────────────────> [7] ──> [11] ──> [13] ──> [20]
L0:  [-∞] ──> [3] ──────────> [7] ──> [11] ──> [13] ──> [20]
```

---

## Complexity Analysis

### Expected Height

Each node is promoted independently with probability p. The height of a node follows a geometric distribution. Expected height = 1/(1-p). For p = 0.5, a node participates in **2 levels on average**.

The expected number of levels in the entire structure is O(log₁/p n) = O(log n).

### Expected Search Cost

At each level, how far do you advance before dropping down? The number of advances at a given level before a "drop" is geometrically distributed with parameter p — expected 1/p advances. For p = 0.5, that's **2 comparisons per level**.

Total expected comparisons = (comparisons per level) × (number of levels) = O(1/p × log n) = **O(log n)**.

### Summary

| Operation | Expected | Worst Case |
| --------- | -------- | ---------- |
| Search    | O(log n) | O(n)       |
| Insert    | O(log n) | O(n)       |
| Delete    | O(log n) | O(n)       |
| Space     | O(n)     | O(n log n) |

The worst case is real but astronomically unlikely. A node reaching height h requires h consecutive heads: probability (1/2)^h. For the worst case (one node promoted to height n), the probability is (1/2)^n — effectively zero for any practical n.

This is the core trade-off: **expected O(log n) with simple implementation, versus guaranteed O(log n) with complex rebalancing.**

---

## Comparison with Other Structures

| Structure          | Search       | Insert       | Delete       | Worst case     | Implementation |
| ------------------ | ------------ | ------------ | ------------ | -------------- | -------------- |
| Sorted Array       | O(log n)     | O(n)         | O(n)         | Guaranteed     | Trivial        |
| Sorted Linked List | O(n)         | O(1)\*       | O(1)\*       | Guaranteed     | Trivial        |
| BST (unbalanced)   | O(log n) avg | O(log n) avg | O(log n) avg | O(n)           | Medium         |
| AVL / RB Tree      | O(log n)     | O(log n)     | O(log n)     | **Guaranteed** | Complex        |
| Skip List          | O(log n) exp | O(log n) exp | O(log n) exp | O(n)           | **Simple**     |

\*Given a pointer to the insert/delete position — finding it still costs O(n).

The skip list occupies the space between "easy to implement but slow" and "fast but hard to implement." It gives you BST-level performance without rotations, rebalancing, or color invariants.

---

## Why This Matters in Practice

### The Honest Answer About Builtins

For single-threaded, general-purpose code: **use your language's built-in ordered map.** `std::map` (C++), `TreeMap` (Java), and Python's `sortedcontainers.SortedList` are all implemented in optimized, well-tested code. A hand-rolled skip list won't outperform them in typical use.

The places skip lists win:

### 1. Concurrent Access — The Real Reason Skip Lists Exist

Making a red-black tree thread-safe requires locking the entire tree (or complex lock-coupling protocols) because a single rotation can touch nodes far apart in the structure. A skip list insert only modifies **local pointers** — the connections immediately adjacent to the new node. This makes lock-free and wait-free skip lists tractable.

**Java's `ConcurrentSkipListMap`** exists for exactly this reason. A `ConcurrentTreeMap` doesn't exist because it would require global locking, destroying the benefit of concurrency.

### 2. Redis Sorted Sets

Redis uses skip lists to implement sorted sets (`ZSET` — the `ZADD`/`ZRANGEBYSCORE` family). The designers chose skip lists over balanced BSTs because:

- Implementation is simpler and less error-prone
- Performance is comparable in practice
- Range queries (retrieve all elements between score A and score B) map naturally to level-0 traversal

When a system handling millions of operations per second makes this choice, it's a meaningful endorsement.

### 3. LevelDB / RocksDB Memtable

Both LevelDB (Google) and RocksDB (Facebook/Meta) use skip lists as the in-memory write buffer (memtable). The skip list supports concurrent writes from multiple threads while maintaining sorted order for efficient flushing to disk.

### 4. Pedagogical Value

Skip lists are the cleanest introduction to **randomized data structures** — the idea that expected O(log n) via randomness is a legitimate engineering tool, not a hack. The same probabilistic reasoning appears in:

- Bloom filters (probabilistic set membership)
- Treaps (BST + heap via random priorities)
- Hash tables with random probing

Understanding skip lists builds the intuition for all of these.

---

## When to Use a Skip List

| Situation                      | Choice                 | Why                                     |
| ------------------------------ | ---------------------- | --------------------------------------- |
| Single-threaded ordered map    | `std::map` / `TreeMap` | Guaranteed O(log n), optimized          |
| Concurrent ordered access      | Skip list              | Lock-free implementations are practical |
| Implementing from scratch      | Skip list              | Far simpler than AVL/RB tree            |
| Range queries on ordered data  | Skip list              | Level-0 is a full sorted linked list    |
| Teaching balanced search       | Skip list              | Coin-flip balance is intuitive          |
| Worst-case guaranteed O(log n) | AVL / RB tree          | Skip list's O(n) worst case is real     |

---

## Key Takeaways

1. **The problem:** sorted linked lists can't binary search because there's no O(1) index access.
2. **The solution:** add express lanes (higher levels) that skip ahead, reducing search to O(log n).
3. **The insight:** coin flips produce the same expected structure as a perfectly balanced skip list, with no coordination overhead.
4. **The trade-off:** expected O(log n), not guaranteed. The price for simplicity.
5. **The real use case:** concurrent access. Skip lists are lock-friendly in ways balanced trees are not.
6. **The honest caveat:** if your language has a built-in ordered map, use it for single-threaded work. Skip lists shine when you need concurrency or are building the thing underneath the builtin.
