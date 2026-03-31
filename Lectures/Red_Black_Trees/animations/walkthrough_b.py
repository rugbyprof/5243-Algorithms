"""
Walkthrough B: Insert 10, 15, 20
Triggers: Case 3 — Uncle BLACK, right child of right parent (line / zig-zig)

BST indices:
  Before rotation:  1=10(B)  3=15(R)  7=20(R)
  After rotation:   1=15(B)  2=10(R)  3=20(R)

Frames:
  0 - Empty tree
  1 - Insert 10 as RED  (Rule 2 violation)
  2 - Fix Rule 2: root → 10(B)
  3 - Insert 15: right child of 10(B), no violation
  4 - Insert 20: right child of 15(R) → DOUBLE RED  (Case 3 identified)
  5 - Rotate LEFT at G(10): 15 promoted to root, pre-recolor
  6 - Color swap: 15→BLACK, 10→RED → valid tree
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import matplotlib.pyplot as plt
from anim_utils import (
    FIG_W, FIG_H, BG_COLOR,
    RED_FILL, BLACK_FILL,
    ANNOT_FAIL, ANNOT_OK, ANNOT_INFO,
    draw_frame, save_frame, generate_viewer,
    tree_nodes, tree_edges, tree_highlights,
)

FOLDER = os.path.join(os.path.dirname(__file__), "walkthrough_b")
TITLE  = "Walkthrough B — Insert 10, 15, 20  (Case 3: Line / Right-Right)"

STEPS = [
    "Step 0: Start with an empty tree",
    "Step 1: Insert 10 — new nodes are always RED",
    "Step 2: Fix Rule 2 — recolor root to BLACK",
    "Step 3: Insert 15 — right child of 10(B), no violation",
    "Step 4: Insert 20 — double-red! Uncle = NULL (BLACK), right of right → Case 3",
    "Step 5: Rotate LEFT at G(10) — 15 promoted to root (colors not yet swapped)",
    "Step 6: Swap colors — P(15) → BLACK, G(10) → RED  ✓ all rules satisfied",
]

idx = 0

def fig():
    f, a = plt.subplots(figsize=(FIG_W, FIG_H))
    f.patch.set_facecolor(BG_COLOR)
    return f, a


# ── Frame 0: empty ────────────────────────────────────────────────────────────
f, a = fig()
draw_frame(a, [], [], "Start: Empty Tree")
a.text(3.5, 2.25, "(empty)", ha="center", va="center",
       fontsize=14, color="#aaaaaa", style="italic")
save_frame(f, FOLDER, idx); idx += 1

# ── Frame 1: insert 10 as RED ─────────────────────────────────────────────────
nodes = {1: (10, RED_FILL)}
f, a = fig()
draw_frame(a,
    nodes=tree_nodes(nodes),
    edges=tree_edges(nodes),
    title="Insert 10  →  new node is always RED",
    caption="✗  Rule 2 violated: root must be Black",
    caption_color=ANNOT_FAIL,
    highlights=tree_highlights(nodes, [1]),
)
save_frame(f, FOLDER, idx); idx += 1

# ── Frame 2: fix root → 10(B) ─────────────────────────────────────────────────
nodes = {1: (10, BLACK_FILL)}
f, a = fig()
draw_frame(a,
    nodes=tree_nodes(nodes),
    edges=tree_edges(nodes),
    title="Fix Rule 2  →  Recolor root to BLACK",
    caption="✓  Rule 2 satisfied",
    caption_color=ANNOT_OK,
)
save_frame(f, FOLDER, idx); idx += 1

# ── Frame 3: insert 15 (bst index 3 = right child of root) ───────────────────
nodes = {1: (10, BLACK_FILL), 3: (15, RED_FILL)}
f, a = fig()
draw_frame(a,
    nodes=tree_nodes(nodes),
    edges=tree_edges(nodes),
    title="Insert 15  →  right child of 10(B)",
    caption="✓  No violation — parent 10 is Black",
    caption_color=ANNOT_OK,
)
save_frame(f, FOLDER, idx); idx += 1

# ── Frame 4: insert 20 (bst index 7 = right child of 3) ──────────────────────
nodes = {1: (10, BLACK_FILL), 3: (15, RED_FILL), 7: (20, RED_FILL)}
f, a = fig()
draw_frame(a,
    nodes=tree_nodes(nodes),
    edges=tree_edges(nodes),
    title="Insert 20  →  DOUBLE RED  (15R → 20R)",
    caption="Uncle = NULL = BLACK  |  Right child of Right parent  →  Case 3",
    caption_color=ANNOT_FAIL,
    highlights=tree_highlights(nodes, [3, 7]),
)
save_frame(f, FOLDER, idx); idx += 1

# ── Frame 5: rotate left at G(10) — pre-recolor ───────────────────────────────
# After left-rotate at 10:  15 is new root (idx 1), 10 is left child (idx 2),
# 20 stays right child of 15 (idx 3).
# Colors are still their pre-rotation values: 15=RED, 10=BLACK, 20=RED.
nodes = {1: (15, RED_FILL), 2: (10, BLACK_FILL), 3: (20, RED_FILL)}
f, a = fig()
draw_frame(a,
    nodes=tree_nodes(nodes),
    edges=tree_edges(nodes),
    title="Rotate LEFT at G(10)  →  15 promoted to root",
    caption="Colors not yet swapped — next: P(15) → BLACK,  G(10) → RED",
    caption_color=ANNOT_INFO,
)
save_frame(f, FOLDER, idx); idx += 1

# ── Frame 6: color swap → valid ───────────────────────────────────────────────
nodes = {1: (15, BLACK_FILL), 2: (10, RED_FILL), 3: (20, RED_FILL)}
f, a = fig()
draw_frame(a,
    nodes=tree_nodes(nodes),
    edges=tree_edges(nodes),
    title="Swap colors: P(15) → BLACK,  G(10) → RED",
    caption="✓  All rules satisfied — black-height = 1 on every path",
    caption_color=ANNOT_OK,
)
save_frame(f, FOLDER, idx); idx += 1

# ── generate viewer ───────────────────────────────────────────────────────────
generate_viewer(FOLDER, idx, TITLE, STEPS)
print(f"Done — {idx} frames in {FOLDER}/")
