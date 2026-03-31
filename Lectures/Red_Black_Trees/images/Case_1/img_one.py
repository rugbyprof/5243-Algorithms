"""
#### Case 1 — Uncle is RED

       G(B)                       G(R)  ← check G next (recurse upward)
      /    \        →            /    /\
    P(R)   U(R)               P(B)   U(B)
    /                          /
  N(R)  ← double red         N(R)  ✓ (locally fixed)
  
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
"""

import sys, os

sys.path.insert(0, os.path.dirname(__file__))
sys.path.append("..")

from rb_draw import (
    new_figure,
    draw_node,
    draw_edge,
    draw_highlight,
    save_figure,
    tree_pos,
    draw_text,
)


img_width = 9
img_height = 6

fig, ax = new_figure(9, 6, xlim=(0, img_width), ylim=(0, img_height))
ax.set_title("Case 1 — Uncle is RED", fontsize=12, fontweight="bold")

# ── Grandparent ──────────────────────────────────
id = 1
draw_node(
    ax,
    id=id,
    location=tree_pos(id, img_width),
    label="10",
    color=(44, 44, 44),  # dark black node  (0-255 RGB)
    annotation_list=[("GrandParent", "N")],
    show_id=False,
    annot_size=18,
    annot_color="#000000",
)

# ── Parent ───────────────────────────────
id += 1
draw_node(
    ax,
    id=id,
    location=tree_pos(id, img_width),
    label="5",
    color=(0.91, 0.30, 0.24),  # red node  (0.0-1.0 RGB)
    annotation_list=[
        ("Parent", "N"),  # 3-tuple with custom color
    ],
    annot_size=18,
)

# ───────────────────────────────Uncle───────────────────────────────
id += 1
draw_node(
    ax,
    id=id,
    location=tree_pos(id, img_width),
    label="15",
    color=(0.91, 0.30, 0.24),
    annotation_list=[("Uncle", "N")],
    annot_size=18,
)

# ── edges ─────────────────────────────────────────────────────────────────────
draw_edge(ax, from_xy=(tree_pos(1, img_width)), to_xy=(tree_pos(2, img_width)))
draw_edge(ax, from_xy=(tree_pos(1, img_width)), to_xy=(tree_pos(3, img_width)))

# ── highlight ring on the red node ────────────────────────────────────────────
# draw_highlight(ax, (1.8, 1.8))

out = os.path.join(os.path.dirname(__file__), "", "case-1_img-1.png")
save_figure(fig, out)
print(f"Saved → {out}")

# ── add kid ────────────────────────────────────────────────
id += 1
draw_node(
    ax,
    id=id,
    location=tree_pos(id, img_width),
    label="1",
    color=(0.91, 0.30, 0.24),  # mpl hex string
    annotation_list=[("New", "N", "#2980b9")],
    annot_size=18,
)

draw_edge(ax, from_xy=(tree_pos(2, img_width)), to_xy=(tree_pos(4, img_width)))

# ── highlight ring on the red node ────────────────────────────────────────────
# draw_highlight(ax, (1.8, 1.8))

out = os.path.join(os.path.dirname(__file__), "", "case-1_img-2.png")
save_figure(fig, out)
print(f"Saved → {out}")


# ── add kid double red────────────────────────────────────────────────
id += 1
# draw_node(
#     ax,
#     id=id,
#     location=tree_pos(id, img_width),
#     label="1",
#     color=(0.91, 0.30, 0.24),  # mpl hex string
#     annotation_list=[("New", "N", "#2980b9"), ("← double red ", "E", "#FF0000")],
#     annot_size=18,
# )
print(tree_pos(id - 1, img_width))
draw_text(
    ax,
    (1.5, 2.2),
    "← double red ",
    fontsize=18,
    color="#ff0000",
    ha="left",
    va="center",
    fontweight="bold",
    style="normal",
    zorder=5,
)

out = os.path.join(os.path.dirname(__file__), "", "case-1_img-3.png")
save_figure(fig, out)
print(f"Saved → {out}")

sys.exit()

# ── edges ─────────────────────────────────────────────────────────────────────
draw_edge(ax, from_xy=(tree_pos(1, img_width)), to_xy=(tree_pos(2, img_width)))
draw_edge(ax, from_xy=(tree_pos(1, img_width)), to_xy=(tree_pos(3, img_width)))
draw_edge(ax, from_xy=(tree_pos(2, img_width)), to_xy=(tree_pos(4, img_width)))

# ── highlight ring on the red node ────────────────────────────────────────────
# draw_highlight(ax, (1.8, 1.8))

out = os.path.join(os.path.dirname(__file__), "", "case-1_img-2.png")
save_figure(fig, out)
print(f"Saved → {out}")


###############################################################################################################

fig, ax = new_figure(9, 6, xlim=(0, img_width), ylim=(0, img_height))
ax.set_title("Case 1 — Uncle is RED", fontsize=12, fontweight="bold")

# ── Grandparent ──────────────────────────────────
id = 1
draw_node(
    ax,
    id=id,
    location=tree_pos(id, img_width),
    label="10",
    color=(44, 44, 44),  # dark black node  (0-255 RGB)
    annotation_list=[("GrandParent", "N")],
    show_id=False,
    annot_size=18,
    annot_color="#000000",
)

# ── Parent ───────────────────────────────
id += 1
draw_node(
    ax,
    id=id,
    location=tree_pos(id, img_width),
    label="5",
    color=(0.91, 0.30, 0.24),  # red node  (0.0-1.0 RGB)
    annotation_list=[
        ("Parent", "N"),  # 3-tuple with custom color
    ],
    annot_size=18,
)

# ───────────────────────────────Uncle───────────────────────────────
id += 1
draw_node(
    ax,
    id=id,
    location=tree_pos(id, img_width),
    label="15",
    color=(0.91, 0.30, 0.24),
    annotation_list=[("Uncle", "N")],
    annot_size=18,
)

# ── add kid ────────────────────────────────────────────────
id += 1
draw_node(
    ax,
    id=id,
    location=tree_pos(id, img_width),
    label="1",
    color=(0.91, 0.30, 0.24),  # mpl hex string
    annotation_list=[("New", "N", "#2980b9")],
    annot_size=18,
)

# ── add kid double red────────────────────────────────────────────────
id += 1
draw_node(
    ax,
    id=id,
    location=tree_pos(id, img_width),
    label="1",
    color=(0.91, 0.30, 0.24),  # mpl hex string
    annotation_list=[("New", "N", "#2980b9"), ("← double red ", "E", "#FF0000")],
    annot_size=18,
)


# ── edges ─────────────────────────────────────────────────────────────────────
draw_edge(ax, from_xy=(tree_pos(1, img_width)), to_xy=(tree_pos(2, img_width)))
draw_edge(ax, from_xy=(tree_pos(1, img_width)), to_xy=(tree_pos(3, img_width)))
draw_edge(ax, from_xy=(tree_pos(2, img_width)), to_xy=(tree_pos(4, img_width)))

# ── highlight ring on the red node ────────────────────────────────────────────
# draw_highlight(ax, (1.8, 1.8))

out = os.path.join(os.path.dirname(__file__), "", "case-1_img-2.png")
save_figure(fig, out)
print(f"Saved → {out}")

