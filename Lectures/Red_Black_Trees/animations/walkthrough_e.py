"""
Walkthrough E: Insert 10, 5, 15, 3, 1
Builds on Walkthrough D — shows Case 3 firing after Case 1 already ran.

BST indices:
  Start (from D):      1=10(B)  2=5(B)  3=15(B)  4=3(R)
  After insert 1:      + 8=1(R)   ← left child of 3 (index 4)
  After rot-R at G(5): 1=10(B)  2=3(B)  3=15(B)  4=1(R)  5=5(R)

Frames:
  0 - Starting tree from Walkthrough D
  1 - Insert 1: left child of 3(R) → DOUBLE RED, Uncle=NULL(BLACK), left of left → Case 3
  2 - Rotate RIGHT at G(5): 3 promoted, pre-recolor
  3 - Color swap: P(3)→BLACK, G(5)→RED → valid tree
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

FOLDER = os.path.join(os.path.dirname(__file__), "walkthrough_e")
TITLE  = "Walkthrough E — Insert …, 3, 1  (Case 3 after Case 1 propagation)"

STEPS = [
    "Step 0: Starting tree — final state from Walkthrough D",
    "Step 1: Insert 1 — double-red! Uncle = NULL (BLACK), left child of left parent → Case 3",
    "Step 2: Rotate RIGHT at G(5) — 3 promoted to index 2 (colors not yet swapped)",
    "Step 3: Swap colors — P(3) → BLACK, G(5) → RED  ✓ all rules satisfied",
]

idx = 0

def fig():
    f, a = plt.subplots(figsize=(FIG_W, FIG_H))
    f.patch.set_facecolor(BG_COLOR)
    return f, a


# ── Frame 0: starting tree from D ─────────────────────────────────────────────
nodes = {1: (10, BLACK_FILL), 2: (5, BLACK_FILL), 3: (15, BLACK_FILL), 4: (3, RED_FILL)}
f, a = fig()
draw_frame(a,
    nodes=tree_nodes(nodes), edges=tree_edges(nodes),
    title="Starting point — final tree from Walkthrough D",
    caption="black-height = 2 on every path  ✓",
    caption_color=ANNOT_OK,
)
save_frame(f, FOLDER, idx); idx += 1

# ── Frame 1: insert 1 (index 8 = left child of index 4) ──────────────────────
# index 8: level=3, slot=0 → x = 7/8 * 0.5 = 0.4375, y = 4.0 - 2.7 = 1.3
nodes = {1: (10, BLACK_FILL), 2: (5, BLACK_FILL), 3: (15, BLACK_FILL),
         4: (3, RED_FILL),    8: (1, RED_FILL)}
f, a = fig()
draw_frame(a,
    nodes=tree_nodes(nodes), edges=tree_edges(nodes),
    title="Insert 1  →  DOUBLE RED  (3R → 1R)",
    caption="Uncle = NULL = BLACK  |  Left child of Left parent  →  Case 3",
    caption_color=ANNOT_FAIL,
    highlights=tree_highlights(nodes, [4, 8]),
)
save_frame(f, FOLDER, idx); idx += 1

# ── Frame 2: rotate RIGHT at G(5) — pre-recolor ───────────────────────────────
# G=5(B) at index 2, P=3(R) at index 4, N=1(R) at index 8
# After rotate right at 5:
#   3 moves to index 2 (5's old spot)
#   1 stays as left child of 3 → index 4
#   5 becomes right child of 3 → index 5
#   10 and 15 unchanged at indices 1 and 3
# Colors before swap: 3=RED (original), 5=BLACK (original), 1=RED, 10=BLACK, 15=BLACK
nodes = {1: (10, BLACK_FILL), 2: (3, RED_FILL),  3: (15, BLACK_FILL),
         4: (1,  RED_FILL),   5: (5, BLACK_FILL)}
f, a = fig()
draw_frame(a,
    nodes=tree_nodes(nodes), edges=tree_edges(nodes),
    title="Rotate RIGHT at G(5)  →  3 promoted to index 2",
    caption="Colors not yet swapped — next: P(3) → BLACK,  G(5) → RED",
    caption_color=ANNOT_INFO,
)
save_frame(f, FOLDER, idx); idx += 1

# ── Frame 3: color swap → valid ───────────────────────────────────────────────
nodes = {1: (10, BLACK_FILL), 2: (3, BLACK_FILL), 3: (15, BLACK_FILL),
         4: (1,  RED_FILL),   5: (5, RED_FILL)}
f, a = fig()
draw_frame(a,
    nodes=tree_nodes(nodes), edges=tree_edges(nodes),
    title="Swap colors: P(3) → BLACK,  G(5) → RED",
    caption="✓  All rules satisfied — black-height = 2 on every path",
    caption_color=ANNOT_OK,
)
save_frame(f, FOLDER, idx); idx += 1

# ── generate viewer ───────────────────────────────────────────────────────────
generate_viewer(FOLDER, idx, TITLE, STEPS)
print(f"Done — {idx} frames in {FOLDER}/")
