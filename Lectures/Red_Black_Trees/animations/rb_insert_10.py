"""
RB Tree Animation: Insert 10
Frames:
  0 - Empty tree (just a label)
  1 - Insert 10 as RED (new node always starts red)
  2 - Recolor root to BLACK (Rule 2 fix)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from PIL import Image
import io

# ── layout constants ──────────────────────────────────────────────────────────
FIG_W, FIG_H = 6, 4
NODE_R = 0.35          # circle radius
FONT_SIZE = 16
BG_COLOR = "#f9f9f9"
EDGE_COLOR = "#555555"

# node colors
RED_FILL   = "#e74c3c"
BLACK_FILL = "#2c2c2c"
TEXT_LIGHT = "white"


def draw_frame(ax, nodes, edges, title, annotation=None):
    """
    nodes  : list of (x, y, label, fill_color)
    edges  : list of (x1,y1, x2,y2)
    title  : string shown at top
    annotation : optional string shown at bottom
    """
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 4)
    ax.axis("off")
    ax.set_title(title, fontsize=13, fontweight="bold", pad=10)

    # draw edges first (so circles sit on top)
    for (x1, y1, x2, y2) in edges:
        ax.annotate(
            "", xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(arrowstyle="-", color=EDGE_COLOR, lw=2)
        )

    # draw nodes
    for (x, y, label, color) in nodes:
        circle = mpatches.Circle(
            (x, y), NODE_R,
            facecolor=color, edgecolor="white", linewidth=2.5,
            zorder=3
        )
        ax.add_patch(circle)
        ax.text(
            x, y, str(label),
            ha="center", va="center",
            fontsize=FONT_SIZE, fontweight="bold",
            color=TEXT_LIGHT, zorder=4
        )

    if annotation:
        ax.text(
            3, 0.35, annotation,
            ha="center", va="center",
            fontsize=11, color="#c0392b",
            style="italic"
        )


def fig_to_pil(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=120, bbox_inches="tight",
                facecolor=BG_COLOR)
    buf.seek(0)
    return Image.open(buf).copy()


# ── define frames ─────────────────────────────────────────────────────────────

frames = []

# Frame 0: empty tree
fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
fig.patch.set_facecolor(BG_COLOR)
draw_frame(ax, nodes=[], edges=[], title="Start: Empty Tree")
ax.text(3, 2, "(empty)", ha="center", va="center",
        fontsize=14, color="#aaaaaa", style="italic")
frames.append(fig_to_pil(fig))
plt.close(fig)

# Frame 1: insert 10 as RED
fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
fig.patch.set_facecolor(BG_COLOR)
draw_frame(
    ax,
    nodes=[(3, 2.2, 10, RED_FILL)],
    edges=[],
    title="Insert 10  →  new node is always RED",
    annotation="✗  Rule 2 violated: root must be Black"
)
frames.append(fig_to_pil(fig))
plt.close(fig)

# Frame 2: recolor root to BLACK
fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
fig.patch.set_facecolor(BG_COLOR)
draw_frame(
    ax,
    nodes=[(3, 2.2, 10, BLACK_FILL)],
    edges=[],
    title="Fix Rule 2  →  Recolor root to BLACK",
    annotation="✓  All rules satisfied"
)
# swap annotation color to green for the "ok" state
ax.texts[-1].set_color("#27ae60")
frames.append(fig_to_pil(fig))
plt.close(fig)


# ── save as GIF ───────────────────────────────────────────────────────────────

out_path = "rb_insert_10.gif"
frames[0].save(
    out_path,
    save_all=True,
    append_images=frames[1:],
    duration=1800,   # ms per frame
    loop=0           # loop forever
)
print(f"Saved → {out_path}")
