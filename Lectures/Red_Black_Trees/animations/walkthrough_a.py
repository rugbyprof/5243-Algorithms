"""
Walkthrough A: Insert 10
Triggers: Rule 2 only (root must be black)

BST indices used:  1 = root

Frames:
  0 - Empty tree
  1 - Insert 10 as RED  (Rule 2 violation)
  2 - Recolor root → BLACK  (fixed)
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import matplotlib.pyplot as plt
from anim_utils import (
    FIG_W, FIG_H, BG_COLOR,
    RED_FILL, BLACK_FILL,
    ANNOT_FAIL, ANNOT_OK,
    draw_frame, save_frame, generate_viewer,
    tree_nodes, tree_edges, tree_highlights,
)

FOLDER = os.path.join(os.path.dirname(__file__), "walkthrough_a")
TITLE  = "Walkthrough A — Insert 10 (Rule 2: Root must be Black)"

STEPS = [
    "Step 0: Start with an empty tree",
    "Step 1: Insert 10 — new nodes are always RED",
    "Step 2: Fix Rule 2 — recolor root to BLACK",
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

# ── Frame 2: recolor root → BLACK ─────────────────────────────────────────────
nodes = {1: (10, BLACK_FILL)}
f, a = fig()
draw_frame(a,
    nodes=tree_nodes(nodes),
    edges=tree_edges(nodes),
    title="Fix Rule 2  →  Recolor root to BLACK",
    caption="✓  All rules satisfied",
    caption_color=ANNOT_OK,
)
save_frame(f, FOLDER, idx); idx += 1

# ── generate viewer ───────────────────────────────────────────────────────────
generate_viewer(FOLDER, idx, TITLE, STEPS)
print(f"Done — {idx} frames in {FOLDER}/")
