"""
Case 3 — Uncle is BLACK, N is OUTER (line) child
  N is left child of a left parent  (or mirror: right child of right parent)

Fix: rotate at G, then swap colors of G and P.

BST indices:
  Initial:              1=G(B)  2=P(R)  4=N(R)   ← line (left of left)
  After rotate-right G: 1=P(B)  2=N(R)  3=G(R)   ← done
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from rb_draw import SlideBuilder, generate_viewer

BLACK   = (44, 44, 44)
RED     = (0.91, 0.30, 0.24)
BLUE    = "#2980b9"
CRIMSON = "#c0392b"
GREEN   = "#27ae60"
INFO    = "#2471a3"
OUT     = os.path.dirname(__file__)
W, H    = 9, 6
ASIZE   = 16

slides = []

s = SlideBuilder(width=W, height=H, title="Case 3 — Uncle BLACK, Line (Outer Child)",
                 annot_size=ASIZE, out_dir=OUT)

# ── Slide 1: setup — G(B), P(R) ───────────────────────────────────────────────
(s.node(1, "G", BLACK, annotations=[("Grandparent", "N")])
  .node(2, "P", RED,   annotations=[("Parent",      "N")])
  .snapshot("3.1.png"))
slides.append(("3.1.png", "Setup: G(B) with left child P(R)"))

# ── Slide 2: insert N as left child of P — line ────────────────────────────────
# idx 4 = left child of idx 2
(s.node(4, "N", RED, annotations=[("New", "N", BLUE)])
  .snapshot("3.2.png"))
slides.append(("3.2.png", "Insert N — left child of left parent P → LINE shape"))

# ── Slide 3: call out violation + shape ───────────────────────────────────────
(s.highlight(2).highlight(4)
  .text((W/2, 0.5), "Double red! Uncle=NULL(Black). N is LEFT child of LEFT parent → LINE → Case 3",
        fontsize=13, color=CRIMSON, fontweight="bold", ha="center")
  .snapshot("3.3.png"))
slides.append(("3.3.png", "Violation: line shape — Uncle BLACK → Case 3 (one rotation)"))

# ── Slide 4: rotate RIGHT at G — pre-recolor ──────────────────────────────────
# P(2) moves up to root idx 1, G(1) drops to right child idx 3, N(4) becomes left of P → idx 2
(s.remove(1).remove(2).remove(4)
  .node(1, "P", RED,   annotations=[("P (new root, pre-recolor)", "N")])
  .node(2, "N", RED,   annotations=[("N", "N", BLUE)])
  .node(3, "G", BLACK, annotations=[("G", "N")])
  .clear_transients()
  .text((W/2, 0.5), "Rotate RIGHT at G — P becomes root. Colors not yet swapped.",
        fontsize=13, color=INFO, fontweight="bold", ha="center")
  .snapshot("3.4.png"))
slides.append(("3.4.png", "Rotate RIGHT at G — P promoted to root, pre-recolor"))

# ── Slide 5: color swap — P takes G's old color (Black), G→Red ───────────────
(s.update(1, color=BLACK, annotations=[("P", "N")])
  .update(3, color=RED,   annotations=[("G", "N")])
  .clear_transients()
  .text((W/2, 0.5), "Swap colors: P→Black (G's old color), G→Red  ✓  All rules satisfied",
        fontsize=13, color=GREEN, fontweight="bold", ha="center")
  .snapshot("3.5.png"))
slides.append(("3.5.png", "Color swap: P→BLACK, G→RED  ✓  All rules satisfied"))

generate_viewer(OUT, slides, "Case 3 — Uncle BLACK, Line (Outer Child)")
print("Case 3 done.")
