"""
Case 1 — Uncle is RED
Fix: Recolor P→BLACK, U→BLACK, G→RED  (no rotations)
Then fix Rule 2 if G was the root.

BST indices (fixed throughout — no rotations):
  1=G(B)  2=P(R)  3=U(R)  4=N(R)
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from rb_draw import SlideBuilder, generate_viewer

BLACK   = (44, 44, 44)
RED     = (0.91, 0.30, 0.24)
BLUE    = "#2980b9"
CRIMSON = "#c0392b"
GREEN   = "#27ae60"
OUT     = os.path.dirname(__file__)
W, H    = 9, 6
ASIZE   = 16

slides = []   # [(filename, label), ...]

s = SlideBuilder(width=W, height=H, title="Case 1 — Uncle is RED",
                 annot_size=ASIZE, out_dir=OUT)

# ── Slide 1: setup — G, P, U ──────────────────────────────────────────────────
(s.node(1, "G",  BLACK, annotations=[("Grandparent", "N")])
  .node(2, "P",  RED,   annotations=[("Parent",      "N")])
  .node(3, "U",  RED,   annotations=[("Uncle",       "N")])
  .snapshot("1.1.png"))
slides.append(("1.1.png", "Setup: G(B) with red children P and U"))

# ── Slide 2: insert N — double red ────────────────────────────────────────────
(s.node(4, "N", RED, annotations=[("New", "N", BLUE)])
  .snapshot("1.2.png"))
slides.append(("1.2.png", "Insert N (red) — double red: P(R) → N(R)"))

# ── Slide 3: call out the violation ───────────────────────────────────────────
(s.highlight(2).highlight(4)
  .text((W/2, 0.5), "Double red! Uncle is RED → Case 1: no rotation needed",
        fontsize=14, color=CRIMSON, fontweight="bold", ha="center")
  .snapshot("1.3.png"))
slides.append(("1.3.png", "Violation: double red — uncle U is RED → Case 1"))

# ── Slide 4: recolor P→B, U→B, G→R ───────────────────────────────────────────
(s.update(1, color=RED)
  .update(2, color=BLACK)
  .update(3, color=BLACK)
  .clear_transients()
  .highlight(1)
  .text((W/2, 0.5), "Recolor: P→Black, U→Black, G→Red  (Rule 2 now violated at root)",
        fontsize=14, color=CRIMSON, fontweight="bold", ha="center")
  .snapshot("1.4.png"))
slides.append(("1.4.png", "Recolor P→B, U→B, G→R — but root is now RED → Rule 2 violated"))

# ── Slide 5: fix Rule 2 — recolor root→B ──────────────────────────────────────
(s.update(1, color=BLACK)
  .clear_transients()
  .text((W/2, 0.5), "Fix Rule 2: recolor root → Black  ✓",
        fontsize=14, color=GREEN, fontweight="bold", ha="center")
  .snapshot("1.5.png"))
slides.append(("1.5.png", "Fix Rule 2: root → BLACK  ✓  All rules satisfied"))

generate_viewer(OUT, slides, "Case 1 — Uncle is RED")
print("Case 1 done.")
