"""
Walkthrough D: Insert 10, 5, 15, 3
Triggers: Case 1 — Uncle is RED (recolor, no rotations)

BST indices stay fixed throughout (no rotations):
  1=10  2=5  3=15  4=3

Frames:
  0 - Empty tree
  1 - Insert 10 as RED  (Rule 2 violation)
  2 - Fix Rule 2: root → 10(B)
  3 - Insert 5: left child of 10(B), no violation
  4 - Insert 15: right child of 10(B), no violation
  5 - Insert 3: left child of 5(R) → DOUBLE RED, Uncle=15(R) → Case 1
  6 - Recolor: P(5)→BLACK, U(15)→BLACK, G(10)→RED  (Rule 2 now violated at root)
  7 - Fix Rule 2: recolor root 10→BLACK → valid tree
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

FOLDER = os.path.join(os.path.dirname(__file__), "walkthrough_d")
TITLE  = "Walkthrough D — Insert 10, 5, 15, 3  (Case 1: Uncle RED — Recolor)"

STEPS = [
    "Step 0: Start with an empty tree",
    "Step 1: Insert 10 — new nodes are always RED",
    "Step 2: Fix Rule 2 — recolor root to BLACK",
    "Step 3: Insert 5 — left child of 10(B), no violation",
    "Step 4: Insert 15 — right child of 10(B), no violation",
    "Step 5: Insert 3 — double-red! Uncle = 15(R)  →  Case 1 (no rotation needed)",
    "Step 6: Recolor — P(5)→BLACK, U(15)→BLACK, G(10)→RED  ✗ Rule 2 violated at root",
    "Step 7: Fix Rule 2 — recolor root to BLACK  ✓ all rules satisfied",
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

# ── Frame 3: insert 5 (index 2) ───────────────────────────────────────────────
nodes = {1: (10, BLACK_FILL), 2: (5, RED_FILL)}
f, a = fig()
draw_frame(a,
    nodes=tree_nodes(nodes), edges=tree_edges(nodes),
    title="Insert 5  →  left child of 10(B)",
    caption="✓  No violation — parent 10 is Black",
    caption_color=ANNOT_OK,
)
save_frame(f, FOLDER, idx); idx += 1

# ── Frame 4: insert 15 (index 3) ──────────────────────────────────────────────
nodes = {1: (10, BLACK_FILL), 2: (5, RED_FILL), 3: (15, RED_FILL)}
f, a = fig()
draw_frame(a,
    nodes=tree_nodes(nodes), edges=tree_edges(nodes),
    title="Insert 15  →  right child of 10(B)",
    caption="✓  No violation — parent 10 is Black",
    caption_color=ANNOT_OK,
)
save_frame(f, FOLDER, idx); idx += 1

# ── Frame 5: insert 3 (index 4 = left child of 5) ────────────────────────────
nodes = {1: (10, BLACK_FILL), 2: (5, RED_FILL), 3: (15, RED_FILL), 4: (3, RED_FILL)}
f, a = fig()
draw_frame(a,
    nodes=tree_nodes(nodes), edges=tree_edges(nodes),
    title="Insert 3  →  DOUBLE RED  (5R → 3R)",
    caption="Uncle = 15(R)  →  Case 1: recolor P(5), U(15) → BLACK,  G(10) → RED",
    caption_color=ANNOT_FAIL,
    highlights=tree_highlights(nodes, [2, 4]),   # the double-red pair
)
save_frame(f, FOLDER, idx); idx += 1

# ── Frame 6: Case 1 recolor — Rule 2 bubbles up ───────────────────────────────
nodes = {1: (10, RED_FILL), 2: (5, BLACK_FILL), 3: (15, BLACK_FILL), 4: (3, RED_FILL)}
f, a = fig()
draw_frame(a,
    nodes=tree_nodes(nodes), edges=tree_edges(nodes),
    title="Case 1: Recolor P(5)→BLACK, U(15)→BLACK, G(10)→RED",
    caption="✗  Rule 2 violated — root 10 is now Red  →  recolor root",
    caption_color=ANNOT_FAIL,
    highlights=tree_highlights(nodes, [1]),       # root is now the problem
)
save_frame(f, FOLDER, idx); idx += 1

# ── Frame 7: fix root → valid ─────────────────────────────────────────────────
nodes = {1: (10, BLACK_FILL), 2: (5, BLACK_FILL), 3: (15, BLACK_FILL), 4: (3, RED_FILL)}
f, a = fig()
draw_frame(a,
    nodes=tree_nodes(nodes), edges=tree_edges(nodes),
    title="Fix Rule 2  →  Recolor root to BLACK",
    caption="✓  All rules satisfied — black-height = 2 on every path",
    caption_color=ANNOT_OK,
)
save_frame(f, FOLDER, idx); idx += 1

# ── generate viewer ───────────────────────────────────────────────────────────
generate_viewer(FOLDER, idx, TITLE, STEPS)
print(f"Done — {idx} frames in {FOLDER}/")
