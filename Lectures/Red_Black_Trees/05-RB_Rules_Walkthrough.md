## Red-Black Tree: Rules Checklist & Violation Walkthroughs

---

## Part 1 — Post-Insertion Checklist

After **every** insertion, run through this checklist **top to bottom**. Fix violations before moving on.

> **New nodes are always inserted RED.**

---

### The Five Rules

| #   | Rule                                                                   | Automatically Satisfied?                                    |
| --- | ---------------------------------------------------------------------- | ----------------------------------------------------------- |
| 1   | Every node is Red or Black                                             | Yes — no action needed                                      |
| 2   | The root is Black                                                      | **Check every insert**                                      |
| 3   | Every NULL leaf is Black                                               | Yes — treat all NULLs as black sentinels                    |
| 4   | No double-red: a red node's parent must be black                       | **Check every insert**                                      |
| 5   | Every root→NULL path has the same number of black nodes (black-height) | Maintained automatically if Cases 1–3 are applied correctly |

---

### Rule 2 Fix

| Violation   | Fix                         |
| ----------- | --------------------------- |
| Root is Red | Recolor root → Black. Done. |

---

### Rule 4 Fixes — Three Cases

When you find a **double-red** (new red node `N`, red parent `P`, grandparent `G`, uncle `U`):

```
Determine uncle U = the sibling of P (the other child of G)
```

---

#### Case 1 — Uncle is RED

```
       G(B)                       G(R)  ← check G next (recurse upward)
      /    \        →            /    \
    P(R)   U(R)               P(B)   U(B)
    /                          /
  N(R)  ← double red         N(R)  ✓ (locally fixed)
```

**Fix:** Recolor P → Black, U → Black, G → Red. Then treat G as the "new node" and re-check upward (G may now be a double-red with _its_ parent, or G may be the root).

---

#### Case 2 — Uncle is BLACK, N is an "inner" (triangle) child

N is the **right** child of a **left** parent, or the **left** child of a **right** parent.

```
      G(B)                       G(B)
      /                          /
    P(R)          →            N(R)       ← N promoted, P demoted
       \                       /
       N(R)  ← inner child   P(R)
```

**Fix:** Rotate at **P** (away from N's side). This converts the triangle into a line — now apply **Case 3** treating the old P as the "new node".

---

#### Case 3 — Uncle is BLACK, N is an "outer" (line) child

N is the **left** child of a **left** parent, or the **right** child of a **right** parent.

```
      G(B)                     P(B)
      /        →              /    \
    P(R)                    N(R)   G(R)
    /
  N(R)  ← outer child
```

**Fix:** Rotate at **G** (away from P's side). Then swap colors of G and P (P takes G's old color, G becomes Red).

---

### Quick Decision Tree (after finding a double-red)

```
Double-red found?
    │
    ├── Uncle is RED?
    │       └── YES → Case 1: recolor P, U → Black; G → Red; recurse at G
    │
    └── Uncle is BLACK (or NULL)?
            │
            ├── N is INNER child (triangle shape)?
            │       └── YES → Case 2: rotate at P → converts to Case 3
            │
            └── N is OUTER child (line shape)?
                    └── YES → Case 3: rotate at G; swap colors of G and P
```

---

---

## Part 2 — Violation Walkthroughs (From Empty)

Each walkthrough uses the **fewest insertions** needed to trigger the target rule/case.

| Walkthrough | Sequence        | Triggers                                        |
| :---------: | :-------------- | :---------------------------------------------- |
|      A      | 10              | Rule 2 only (root recolor)                      |
|      B      | 10, 15, 20      | Case 3 — line/right-right                       |
|      C      | 10, 5, 7        | Case 2 → Case 3 (triangle then line)            |
|      D      | 10, 5, 15, 3    | Case 1 — uncle red, recolor + propagate to root |
|      E      | 10, 5, 15, 3, 1 | Builds on D, then Case 3 closes it              |

---

### Walkthrough A: Violate Rule 2 (Root Must Be Black)

**Insert sequence:** `10`

```
Step 1: Insert 10
  New node is always colored RED. 10 becomes the root.

    10(R)

  ✗ Rule 2 violated: root is Red.

Fix: Recolor root → Black.

    10(B)

  ✓ All rules satisfied.
```

**Takeaway:** Every single insertion triggers a Rule 2 check. The root recolor costs nothing and happens often.

---

### Walkthrough B: Violate Rule 4 — Case 3 (Line, Uncle BLACK)

**Insert sequence:** `10, 15, 20`

```
Step 1: Insert 10 → Red → recolor root → Black.

    10(B)


Step 2: Insert 15 (right child of 10)
  15 is Red, parent 10 is Black → no double-red.

    10(B)
       \
       15(R)

  ✓ No violations.


Step 3: Insert 20 (right child of 15)
  20 is Red, parent 15 is Red → DOUBLE-RED.

    10(B)
       \
       15(R)
          \
          20(R)   ← violation

  Identify: P = 15, G = 10, U = left child of 10 = NULL (BLACK)
  Uncle is BLACK. N(20) is RIGHT child of RIGHT parent → OUTER / LINE → Case 3.

  Fix Case 3:
    • Rotate LEFT at G (10).
    • Swap colors: P(15) takes G's old color (Black), G(10) becomes Red.

  After left-rotate at 10:

        15(?)
       /     \
     10(?)   20(R)

  After color swap (15 → Black, 10 → Red):

        15(B)
       /     \
     10(R)   20(R)

  ✓ All rules satisfied.
  Black-height check: every NULL path passes through exactly one black node (15). ✓
```

**Takeaway:** Case 3 is one operation — a single rotation plus two recolors. The tree is done.

---

### Walkthrough C: Violate Rule 4 — Case 2 → Case 3 (Triangle, Uncle BLACK)

**Insert sequence:** `10, 5, 7`

```
Step 1: Insert 10 → recolor root → 10(B).

    10(B)


Step 2: Insert 5 (left child of 10)
  5 is Red, parent 10 is Black → no violation.

    10(B)
    /
  5(R)

  ✓ No violations.


Step 3: Insert 7 (right child of 5)
  7 is Red, parent 5 is Red → DOUBLE-RED.

      10(B)
      /
    5(R)
       \
       7(R)   ← violation

  Identify: N = 7, P = 5, G = 10, U = right child of 10 = NULL (BLACK)
  Uncle is BLACK. N(7) is RIGHT child of LEFT parent → INNER / TRIANGLE → Case 2.

  Fix Case 2: Rotate LEFT at P (5).

  After left-rotate at 5:

      10(B)
      /
    7(R)
    /
  5(R)

  Now N = 5, P = 7, G = 10. N(5) is LEFT child of LEFT parent → LINE → apply Case 3.

  Fix Case 3: Rotate RIGHT at G (10). Swap colors: P(7) → Black, G(10) → Red.

  After right-rotate at 10 + color swap:

      7(B)
     /   \
  5(R)   10(R)

  ✓ All rules satisfied.
  Black-height check: every NULL path passes through exactly one black node (7). ✓
```

**Takeaway:** Case 2 never fixes the violation by itself — it always feeds into Case 3. Two rotations total.

---

### Walkthrough D: Violate Rule 4 — Case 1 (Uncle RED, Recolor + Recurse)

**Insert sequence:** `10, 5, 15, 3`

```
Step 1: Insert 10 → recolor root → 10(B).

    10(B)


Step 2: Insert 5 (left child of 10). Parent is Black. ✓

    10(B)
    /
  5(R)


Step 3: Insert 15 (right child of 10). Parent is Black. ✓

      10(B)
     /    \
   5(R)  15(R)


Step 4: Insert 3 (left child of 5)
  3 is Red, parent 5 is Red → DOUBLE-RED.

        10(B)
       /    \
     5(R)  15(R)
     /
   3(R)   ← violation

  Identify: N = 3, P = 5, G = 10, U = 15 (RED)
  Uncle is RED → Case 1.

  Fix Case 1: Recolor P(5) → Black, U(15) → Black, G(10) → Red.

        10(R)   ← G is now Red; must check G next
       /    \
     5(B)  15(B)
     /
   3(R)

  Now check G (10): 10 is the root and it's Red.
  ✗ Rule 2 violated.

  Fix: Recolor root → Black.

        10(B)
       /    \
     5(B)  15(B)
     /
   3(R)

  ✓ All rules satisfied.
  Black-height check:
    Path 10→5→3→NULL: black nodes = 10, 5 = 2
    Path 10→5→NULL (right of 5): black nodes = 10, 5 = 2
    Path 10→15→NULL (left): black nodes = 10, 15 = 2
    Path 10→15→NULL (right): black nodes = 10, 15 = 2
  All paths = 2. ✓
```

**Takeaway:** Case 1 costs no rotations but _propagates upward_ — the grandparent becomes red and must be re-checked. In the worst case this bubbles all the way to the root (where Rule 2 catches it).

---

### Walkthrough E: Case 1 Propagates into Case 3

**Insert sequence:** `10, 5, 15, 3, 1`

_(Builds on Walkthrough D — start from the final tree there.)_

```
Starting tree (from Walkthrough D):

        10(B)
       /    \
     5(B)  15(B)
     /
   3(R)


Insert 1 (left child of 3)
  1 is Red, parent 3 is Red → DOUBLE-RED.

          10(B)
         /    \
       5(B)  15(B)
       /
     3(R)
     /
   1(R)   ← violation

  Identify: N = 1, P = 3, G = 5, U = right child of 5 = NULL (BLACK)
  Uncle is BLACK. N(1) is LEFT child of LEFT parent → LINE → Case 3.

  Fix Case 3: Rotate RIGHT at G (5). Swap colors: P(3) → Black, G(5) → Red.

  After right-rotate at 5 + color swap:

          10(B)
         /    \
       3(B)  15(B)
       /   \
     1(R)  5(R)

  ✓ All rules satisfied.
  Black-height check: all root→NULL paths pass through 10(B) + one of {3(B),15(B)} = 2 black nodes. ✓
```

**Takeaway:** Case 1 didn't propagate here (uncle was BLACK), so Case 3 closed it directly. But notice how each new insertion only triggers _one_ case — the cases don't stack on the same violation.

---

## Summary Reference Card

| Scenario                          | Action                       | Rotations | Recurse?      |
| --------------------------------- | ---------------------------- | --------- | ------------- |
| Root is Red                       | Recolor root → Black         | 0         | No            |
| Double-red, Uncle RED             | Recolor P+U → Black, G → Red | 0         | Yes (check G) |
| Double-red, Uncle BLACK, triangle | Rotate at P (→ becomes line) | 1         | No (→ Case 3) |
| Double-red, Uncle BLACK, line     | Rotate at G, swap G/P colors | 1         | No            |

**Maximum rotations per insertion: 2** (Case 2 + Case 3 back-to-back).  
**Recoloring can propagate O(log n) steps upward** (Case 1 chains), but no rotations occur during propagation.
