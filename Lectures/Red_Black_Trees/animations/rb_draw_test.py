"""
Smoke test for rb_draw.py
Produces test_output/rb_draw_test.png — visually verify annotations hit all 8 directions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from rb_draw import new_figure, draw_node, draw_edge, draw_highlight, save_figure

fig, ax = new_figure(9, 6, xlim=(0, 9), ylim=(0, 6))
ax.set_title("rb_draw.py — annotation direction test", fontsize=12, fontweight="bold")

# ── center node: all 8 annotation directions ──────────────────────────────────
draw_node(ax,
    id=1,
    location=(4.5, 3.5),
    label="10",
    color=(44, 44, 44),           # dark black node  (0-255 RGB)
    annotation_list=[
        ("N",  "N"),
        ("NE", "NE"),
        ("E",  "E"),
        ("SE", "SE"),
        ("S",  "S"),
        ("SW", "SW"),
        ("W",  "W"),
        ("NW", "NW"),
    ],
    show_id=True,
    annot_size=10,
    annot_color="#c0392b",
)

# ── red node with per-annotation color override ───────────────────────────────
draw_node(ax,
    id=2,
    location=(1.8, 1.8),
    label="5",
    color=(0.91, 0.30, 0.24),     # red node  (0.0-1.0 RGB)
    annotation_list=[
        ("P (parent)", "W",  "#2980b9"),   # 3-tuple with custom color
        ("violation",  "S",  "#c0392b"),
    ],
    annot_size=10,
)

# ── black node, no annotations ────────────────────────────────────────────────
draw_node(ax,
    id=3,
    location=(7.2, 1.8),
    label="15",
    color="#2c2c2c",              # mpl hex string
    annotation_list=[("U (uncle)", "E")],
    annot_size=10,
)

# ── edges ─────────────────────────────────────────────────────────────────────
draw_edge(ax, from_xy=(4.5, 3.5), to_xy=(1.8, 1.8))
draw_edge(ax, from_xy=(4.5, 3.5), to_xy=(7.2, 1.8))

# ── highlight ring on the red node ────────────────────────────────────────────
draw_highlight(ax, (1.8, 1.8))

out = os.path.join(os.path.dirname(__file__), "test_output", "rb_draw_test.png")
save_figure(fig, out)
print(f"Saved → {out}")
