"""
Walkthrough C: Insert 10, 5, 7
Triggers: Case 2 (triangle) → Case 3 (line)

BST indices:
  After insert 7:          1=10(B)  2=5(R)   5=7(R)   ← triangle
  After Case 2 (rot-L 5):  1=10(B)  2=7(R)   4=5(R)   ← now a line
  After Case 3 (rot-R 10): 1=7(B)   2=5(R)   3=10(R)  ← done

Frames:
  0 - Empty tree
  1 - Insert 10 as RED  (Rule 2 violation)
  2 - Fix Rule 2: root → 10(B)
  3 - Insert 5: left child of 10(B), no violation
  4 - Insert 7: right child of 5(R) → DOUBLE RED, triangle → Case 2
  5 - Rotate LEFT at P(5): 7 promoted, 5 demoted — now a line → Case 3
  6 - Rotate RIGHT at G(10): 7 becomes root, pre-recolor
  7 - Color swap: P(7)→BLACK, G(10)→RED → valid tree
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

FOLDER = os.path.join(os.path.dirname(__file__), "walkthrough_c")
TITLE  = "Walkthrough C — Insert 10, 5, 7  (Case 2 → Case 3: Triangle → Line)"

STEPS = [
    "Step 0: Start with an empty tree",
    "Step 1: Insert 10 — new nodes are always RED",
    "Step 2: Fix Rule 2 — recolor root to BLACK",
    "Step 3: Insert 5 — left child of 10(B), no violation",
    "Step 4: Insert 7 — double-red! Uncle = NULL (BLACK), right child of left parent → Case 2 (triangle)",
    "Step 5: Rotate LEFT at P(5) — 7 promoted, 5 demoted — double-red remains but now it's a LINE → Case 3",
    "Step 6: Rotate RIGHT at G(10) — 7 becomes root (colors not yet swapped)",
    "Step 7: Swap colors — P(7) → BLACK, G(10) → RED  ✓ all rules satisfied",
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
    nodes=tree_nodes(nodes), edges=tree_edges(nodes),
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
    nodes=tree_nodes(nodes), edges=tree_edges(nodes),
    title="Fix Rule 2  →  Recolor root to BLACK",
    caption="✓  Rule 2 satisfied",
    caption_color=ANNOT_OK,
)
save_frame(f, FOLDER, idx); idx += 1

# ── Frame 3: insert 5 (index 2 = left child of root) ────────────────────────
nodes = {1: (10, BLACK_FILL), 2: (5, RED_FILL)}
f, a = fig()
draw_frame(a,
    nodes=tree_nodes(nodes), edges=tree_edges(nodes),
    title="Insert 5  →  left child of 10(B)",
    caption="✓  No violation — parent 10 is Black",
    caption_color=ANNOT_OK,
)
save_frame(f, FOLDER, idx); idx += 1

# ── Frame 4: insert 7 (index 5 = right child of index 2) ─────────────────────
# Triangle: 10(B)-left→5(R)-right→7(R)
nodes = {1: (10, BLACK_FILL), 2: (5, RED_FILL), 5: (7, RED_FILL)}
f, a = fig()
draw_frame(a,
    nodes=tree_nodes(nodes), edges=tree_edges(nodes),
    title="Insert 7  →  DOUBLE RED  (5R → 7R)",
    caption="Uncle = NULL = BLACK  |  Right child of Left parent  →  TRIANGLE  →  Case 2",
    caption_color=ANNOT_FAIL,
    highlights=tree_highlights(nodes, [2, 5]),
)
save_frame(f, FOLDER, idx); idx += 1

# ── Frame 5: rotate LEFT at P(5) — Case 2 fix ────────────────────────────────
# 7 takes 5's spot (index 2), 5 becomes left child of 7 (index 4)
# Colors unchanged: 10=BLACK, 7=RED, 5=RED  — still double-red, but now a LINE
nodes = {1: (10, BLACK_FILL), 2: (7, RED_FILL), 4: (5, RED_FILL)}
f, a = fig()
draw_frame(a,
    nodes=tree_nodes(nodes), edges=tree_edges(nodes),
    title="Rotate LEFT at P(5)  →  7 promoted, 5 demoted",
    caption="Still double-red — but now LEFT child of LEFT parent  →  LINE  →  Case 3",
    caption_color=ANNOT_INFO,
    highlights=tree_highlights(nodes, [2, 4]),
)
save_frame(f, FOLDER, idx); idx += 1

# ── Frame 6: rotate RIGHT at G(10) — Case 3, pre-recolor ─────────────────────
# 7 becomes root (index 1), 5 left child of 7 (index 2), 10 right child of 7 (index 3)
# Colors before swap: 7=RED (original), 5=RED (original), 10=BLACK (original)
nodes = {1: (7, RED_FILL), 2: (5, RED_FILL), 3: (10, BLACK_FILL)}
f, a = fig()
draw_frame(a,
    nodes=tree_nodes(nodes), edges=tree_edges(nodes),
    title="Rotate RIGHT at G(10)  →  7 becomes root",
    caption="Colors not yet swapped — next: P(7) → BLACK,  G(10) → RED",
    caption_color=ANNOT_INFO,
)
save_frame(f, FOLDER, idx); idx += 1

# ── Frame 7: color swap → valid ───────────────────────────────────────────────
nodes = {1: (7, BLACK_FILL), 2: (5, RED_FILL), 3: (10, RED_FILL)}
f, a = fig()
draw_frame(a,
    nodes=tree_nodes(nodes), edges=tree_edges(nodes),
    title="Swap colors: P(7) → BLACK,  G(10) → RED",
    caption="✓  All rules satisfied — black-height = 1 on every path",
    caption_color=ANNOT_OK,
)
save_frame(f, FOLDER, idx); idx += 1

# ── generate viewer ───────────────────────────────────────────────────────────
generate_viewer(FOLDER, idx, TITLE, STEPS)
print(f"Done — {idx} frames in {FOLDER}/")
