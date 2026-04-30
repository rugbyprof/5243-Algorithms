
# 🌳 Tree Traversal — One-Page Comparison Sheet  
**(Pin this to your brain. Or your monitor. Same effect.)**

---

## The Three Traversals (Binary Trees)

| Traversal     | Order               | Mnemonic                 | What It *Feels* Like         |
| ------------- | ------------------- | ------------------------ | ---------------------------- |
| **Preorder**  | Root → Left → Right | *“Visit, then children”* | Top-down, structure-first    |
| **Inorder**   | Left → Root → Right | *“Sorted vibes”*         | Calm, symmetrical            |
| **Postorder** | Left → Right → Root | *“Clean up last”*        | Bottom-up, destructor energy |

---

## Visual Intuition (No Diagrams, Just Truth)

- **Preorder**:  
  “I care about *who* you are before what’s under you.”
- **Inorder**:  
  “Show me everything in order… if that order exists.”
- **Postorder**:  
  “I’m not touching you until your children are gone.”

---

## What Each Traversal Is *Good For*

| Traversal     | Primary Use                          | Why It Works                   |
| ------------- | ------------------------------------ | ------------------------------ |
| **Preorder**  | Copying / serializing tree structure | Root comes first → rebuildable |
| **Inorder**   | Sorted output (BST only)             | Left < Root < Right            |
| **Postorder** | Deletion / freeing memory            | Children die before parent     |

💀 **Rule of thumb:**  
If you delete a node *before* its children, enjoy your segmentation fault.

---

## Complexity (They All Look Innocent Here)

| Traversal | Time | Space (recursive) |
| --------- | ---- | ----------------- |
| Preorder  | O(n) | O(h)              |
| Inorder   | O(n) | O(h)              |
| Postorder | O(n) | O(h)              |

Where:
- `n` = number of nodes  
- `h` = height of tree  
  - Balanced: `O(log n)`
  - Worst case: `O(n)` (aka “congratulations, it’s a linked list”)

---

## Recursive vs Iterative Reality Check

| Approach  | Uses           | Hidden Cost                    |
| --------- | -------------- | ------------------------------ |
| Recursive | Call stack     | Stack overflow if tree is deep |
| Iterative | Explicit stack | More code, same logic          |

🧠 **Key insight:**  
Recursive traversal = DFS with the compiler holding your hand.

---

## BST-Specific Truths (This Will Be Tested)

- **Inorder traversal of a BST produces sorted output**
- Preorder and Postorder do **not**
- If your inorder output is not sorted, your BST is lying to you

---

## Tree Reconstruction (Exam Favorite)

**Question:**  
> Which traversal(s) allow you to rebuild a binary tree?

**Answer (non-negotiable):**

| Traversals Given    | Can Rebuild? |
| ------------------- | ------------ |
| Inorder alone       | ❌ No         |
| Preorder alone      | ❌ No         |
| Postorder alone     | ❌ No         |
| Inorder + Preorder  | ✅ Yes        |
| Inorder + Postorder | ✅ Yes        |

📌 **Why inorder is mandatory:**  
It tells you *relative positioning*.  
The others tell you *who comes first*.

---

## Common Student Mistakes (Learn From Others’ Pain)

- “Inorder always sorts” → ❌ *Only for BSTs*
- “Preorder is faster” → ❌ *Same complexity*
- “Postorder is weird” → ❌ *You just haven’t deleted anything yet*
- “Traversal order doesn’t matter” → ❌ *Tell that to memory management*

---

## One-Sentence Mental Models (Steal These)

- **Preorder**: *Design first*
- **Inorder**: *Order matters*
- **Postorder**: *Destroy responsibly*