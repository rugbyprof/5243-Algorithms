"""
Case 2 — Uncle is BLACK, N is INNER (triangle) child
  N is right child of a left parent  (or mirror: left child of right parent)

Fix: rotate at P to convert triangle → line, then apply Case 3.

BST indices:
  Initial:               1=G(B)  2=P(R)  5=N(R)   ← triangle (right of left)
  After rotate-left P:   1=G(B)  2=N(R)  4=P(R)   ← now a line (left of left)
  After rotate-right G:  1=N(B)  2=P(R)  3=G(R)   ← Case 3 complete
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

s = SlideBuilder(width=W, height=H, title="Case 2 — Uncle BLACK, Triangle (Inner Child)",
                 annot_size=ASIZE, out_dir=OUT)

# ── Slide 1: setup — G(B), P(R) ───────────────────────────────────────────────
(s.node(1, "G", BLACK, annotations=[("Grandparent", "N")])
  .node(2, "P", RED,   annotations=[("Parent",      "N")])
  .snapshot("2.1.png"))
slides.append(("2.1.png", "Setup: G(B) with left child P(R)"))

# ── Slide 2: insert N as right child of P — triangle ─────────────────────────
# idx 5 = right child of idx 2
(s.node(5, "N", RED, annotations=[("New", "N", BLUE)])
  .snapshot("2.2.png"))
slides.append(("2.2.png", "Insert N — right child of left parent P → TRIANGLE shape"))

# ── Slide 3: call out violation + shape ───────────────────────────────────────
(s.highlight(2).highlight(5)
  .text((W/2, 0.5), "Double red! Uncle=NULL(Black). N is RIGHT child of LEFT parent → TRIANGLE → Case 2",
        fontsize=13, color=CRIMSON, fontweight="bold", ha="center")
  .snapshot("2.3.png"))
slides.append(("2.3.png", "Violation: triangle shape — Uncle BLACK → Case 2"))

# ── Slide 4: rotate LEFT at P ─────────────────────────────────────────────────
# N(5) moves up to idx 2, P(2) drops to idx 4
# Colors unchanged: G=BLACK, N=RED, P=RED  — double red persists but now a LINE
(s.remove(2).remove(5)
  .node(2, "N", RED, annotations=[("N (was right of P)", "N", BLUE)])
  .node(4, "P", RED, annotations=[("P (was Parent)",     "N")])
  .clear_transients()
  .highlight(2).highlight(4)
  .text((W/2, 0.5), "Rotate LEFT at P — N promoted, P demoted. Now a LINE → apply Case 3",
        fontsize=13, color=INFO, fontweight="bold", ha="center")
  .snapshot("2.4.png"))
slides.append(("2.4.png", "Rotate LEFT at P → triangle becomes a line → Case 3"))

# ── Slide 5: rotate RIGHT at G (Case 3) — pre-recolor ────────────────────────
# N(2) moves up to root idx 1, G(1) drops to idx 3, P(4) becomes left of N → idx 2
(s.remove(1).remove(2).remove(4)
  .node(1, "N", RED,   annotations=[("N (new root, pre-recolor)", "N", BLUE)])
  .node(2, "P", RED,   annotations=[("P", "N")])
  .node(3, "G", BLACK, annotations=[("G", "N")])
  .clear_transients()
  .text((W/2, 0.5), "Rotate RIGHT at G — N becomes root. Colors not yet swapped.",
        fontsize=13, color=INFO, fontweight="bold", ha="center")
  .snapshot("2.5.png"))
slides.append(("2.5.png", "Rotate RIGHT at G (Case 3) — N promoted, pre-recolor"))

# ── Slide 6: color swap — P takes G's old color (Black), G→Red ───────────────
(s.update(1, color=BLACK, annotations=[("N", "N")])
  .update(3, color=RED,   annotations=[("G", "N")])
  .clear_transients()
  .text((W/2, 0.5), "Swap colors: N→Black (G's old color), G→Red  ✓  All rules satisfied",
        fontsize=13, color=GREEN, fontweight="bold", ha="center")
  .snapshot("2.6.png"))
slides.append(("2.6.png", "Color swap: N→BLACK, G→RED  ✓  All rules satisfied"))

generate_viewer(OUT, slides, "Case 2 — Uncle BLACK, Triangle (Inner Child)")
print("Case 2 done.")
