"""
Case 1 — Uncle is RED  (rewritten with SlideBuilder)
Same 3 output images as img_one.py, ~1/3 the code.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from rb_draw import SlideBuilder

BLACK = (44, 44, 44)
RED   = (0.91, 0.30, 0.24)
BLUE  = "#2980b9"
CRIMSON = "#c0392b"

OUT = os.path.dirname(__file__)

s = SlideBuilder(width=9, height=6, title="Case 1 — Uncle is RED",
                 annot_size=18, out_dir=OUT)

# ── img 1: G, P, U — the setup ───────────────────────────────────────────────
(s.node(1, "10", BLACK, annotations=[("GrandParent", "N")])
  .node(2,  "5", RED,   annotations=[("Parent",      "N")])
  .node(3, "15", RED,   annotations=[("Uncle",       "N")])
  .snapshot("case-1_img-1.png"))

# ── img 2: insert new node N ──────────────────────────────────────────────────
(s.node(4, "1", RED, annotations=[("New", "N", BLUE)])
  .snapshot("case-1_img-2.png"))

# ── img 3: mark double-red ────────────────────────────────────────────────────
(s.highlight(4)
  .highlight(2)
  .text((4.5, 0.5), "← double red", fontsize=18, color=CRIMSON,
        fontweight="bold", ha="center")
  .snapshot("case-1_img-3.png"))
