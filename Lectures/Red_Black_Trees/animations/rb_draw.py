"""
rb_draw.py
----------
Standalone primitives for drawing Red-Black tree diagrams on a matplotlib Axes.

Public API
----------
new_figure(width, height, bg)           → (fig, ax)
draw_node(ax, id, location, label,
          color, annotation_list, ...)  → None
draw_edge(ax, from_xy, to_xy, ...)      → None
save_figure(fig, path, bg)              → None

Cardinal directions for annotation placement
--------------------------------------------
Directions are compass-bearing strings mapped to degrees clockwise from North:

    N=0   NE=45   E=90   SE=135
    S=180 SW=225  W=270  NW=315

Each annotation in annotation_list is a tuple:
    (label: str,  direction: str)   e.g.  ("N", "NE")  or  ("uncle", "E")

Example
-------
    fig, ax = new_figure(8, 5)
    draw_node(ax,
              id=1,
              location=(4.0, 3.0),
              label="10",
              color=(44, 44, 44),           # dark / Black node
              annotation_list=[
                  ("root",  "S"),
                  ("G",     "NW"),
              ])
    draw_edge(ax, from_xy=(4.0, 3.0), to_xy=(2.5, 2.0))
    save_figure(fig, "out.png")
"""

import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# ── defaults ──────────────────────────────────────────────────────────────────
DEFAULT_NODE_RADIUS  = 0.38
DEFAULT_FONT_SIZE    = 16
DEFAULT_ANNOT_SIZE   = 10
DEFAULT_EDGE_COLOR   = "#444444"
DEFAULT_EDGE_LW      = 2.2
DEFAULT_BG           = "#f9f9f9"
DEFAULT_TEXT_COLOR   = (1.0, 1.0, 1.0)   # white
DEFAULT_ANNOT_COLOR  = "#222222"
DEFAULT_ANNOT_OFFSET = 1.8               # multiplier of node_radius for label distance


# ── cardinal direction tables ─────────────────────────────────────────────────
# Compass-bearing degrees (clockwise from North) → (ha, va) text alignment
_DIRECTION_ALIGN = {
    "N":  ("center", "bottom"),
    "NE": ("left",   "bottom"),
    "E":  ("left",   "center"),
    "SE": ("left",   "top"),
    "S":  ("center", "top"),
    "SW": ("right",  "top"),
    "W":  ("right",  "center"),
    "NW": ("right",  "bottom"),
}

# Compass bearing → (dx_unit, dy_unit) in matplotlib data space
# Convert clockwise-from-North bearing to counterclockwise-from-East for math:
#   math_angle = 90 - bearing
def _cardinal_to_unit(direction: str):
    """Return unit (dx, dy) for a cardinal direction string."""
    degrees = {
        "N": 0, "NE": 45, "E": 90, "SE": 135,
        "S": 180, "SW": 225, "W": 270, "NW": 315,
    }
    if direction.upper() not in degrees:
        raise ValueError(
            f"Unknown direction '{direction}'. "
            f"Must be one of: {list(degrees.keys())}"
        )
    bearing   = degrees[direction.upper()]
    math_rad  = math.radians(90 - bearing)   # convert bearing → standard angle
    return math.cos(math_rad), math.sin(math_rad)


# ── color normalisation ───────────────────────────────────────────────────────
def _norm_color(color):
    """
    Accept either:
      • (r, g, b)  with values 0–255  → normalise to 0.0–1.0
      • (r, g, b)  with values 0.0–1.0 → return as-is
      • A matplotlib color string        → return as-is
    """
    if isinstance(color, str):
        return color
    r, g, b = color
    if r > 1 or g > 1 or b > 1:          # looks like 0-255
        return (r / 255.0, g / 255.0, b / 255.0)
    return (float(r), float(g), float(b))


# ── public primitives ─────────────────────────────────────────────────────────

def new_figure(width=7, height=4.5, bg=DEFAULT_BG, xlim=(0, 7), ylim=(0, 4.5)):
    """
    Create and return a (fig, ax) pair with sane defaults for tree diagrams.

    Parameters
    ----------
    width, height : figure size in inches
    bg            : background color (applied to both figure and axes)
    xlim, ylim    : data-coordinate extents
    """
    fig, ax = plt.subplots(figsize=(width, height))
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    return fig, ax


def draw_node(
    ax,
    id,                          # int  — node identifier (metadata; optionally shown)
    location,                    # (x, y) in data coordinates
    label,                       # str  — text rendered inside the circle
    color,                       # RGB tuple (0–255 or 0.0–1.0) or mpl color string
    annotation_list=None,        # [(label_str, cardinal_dir), ...]
    *,
    node_radius=DEFAULT_NODE_RADIUS,
    font_size=DEFAULT_FONT_SIZE,
    text_color=DEFAULT_TEXT_COLOR,
    annot_size=DEFAULT_ANNOT_SIZE,
    annot_color=DEFAULT_ANNOT_COLOR,
    annot_offset=DEFAULT_ANNOT_OFFSET,
    show_id=False,               # if True, draw `id` as a small superscript above node
    edge_color="white",          # outline color of the circle
    edge_lw=2.5,
    zorder=3,
):
    """
    Draw a single RB-tree node (circle + label) with optional annotations.

    Parameters
    ----------
    ax              : matplotlib Axes
    id              : int  node identifier (used for show_id; otherwise metadata only)
    location        : (x, y) center of the node in data coordinates
    label           : text rendered inside the circle
    color           : fill color — RGB (0-255 or 0.0-1.0) or any mpl color string
    annotation_list : list of (text, cardinal_direction) tuples
                      cardinal_direction ∈ {N, NE, E, SE, S, SW, W, NW}
    node_radius     : radius of the circle in data units
    font_size       : font size of the label inside the circle
    text_color      : color of the label text
    annot_size      : font size of annotation text
    annot_color     : default color of annotation text
                      (override per-annotation by passing (text, dir, color) tuples)
    annot_offset    : distance of annotation from node center, as a multiple of node_radius
    show_id         : if True, render the node id as a tiny label above the circle
    edge_color      : circle outline color
    edge_lw         : circle outline linewidth
    zorder          : matplotlib draw order
    """
    x, y = location
    fill = _norm_color(color)

    # circle
    circle = mpatches.Circle(
        (x, y), node_radius,
        facecolor=fill,
        edgecolor=edge_color,
        linewidth=edge_lw,
        zorder=zorder,
    )
    ax.add_patch(circle)

    # label inside circle
    ax.text(
        x, y, str(label),
        ha="center", va="center",
        fontsize=font_size, fontweight="bold",
        color=_norm_color(text_color),
        zorder=zorder + 1,
    )

    # optional id superscript (small, top-right corner of circle)
    if show_id:
        ax.text(
            x + node_radius * 0.75,
            y + node_radius * 0.75,
            str(id),
            ha="left", va="bottom",
            fontsize=annot_size - 2,
            color="#888888",
            zorder=zorder + 1,
        )

    # annotations
    for entry in (annotation_list or []):
        # accept either (text, direction) or (text, direction, color)
        if len(entry) == 3:
            ann_text, direction, ann_col = entry
        else:
            ann_text, direction = entry
            ann_col = annot_color

        dx, dy = _cardinal_to_unit(direction)
        dist   = node_radius * annot_offset
        ax.text(
            x + dx * dist,
            y + dy * dist,
            str(ann_text),
            ha=_DIRECTION_ALIGN[direction.upper()][0],
            va=_DIRECTION_ALIGN[direction.upper()][1],
            fontsize=annot_size,
            color=ann_col,
            zorder=zorder + 1,
        )


def draw_edge(
    ax,
    from_xy,
    to_xy,
    *,
    color=DEFAULT_EDGE_COLOR,
    lw=DEFAULT_EDGE_LW,
    zorder=2,
):
    """
    Draw a plain line edge between two node centers.

    Parameters
    ----------
    ax       : matplotlib Axes
    from_xy  : (x, y) of the parent node center
    to_xy    : (x, y) of the child node center
    color    : line color
    lw       : line width
    zorder   : matplotlib draw order (should be below nodes)
    """
    ax.annotate(
        "", xy=to_xy, xytext=from_xy,
        arrowprops=dict(arrowstyle="-", color=color, lw=lw),
        zorder=zorder,
    )


def save_figure(fig, path, bg=DEFAULT_BG, dpi=130):
    """
    Save the figure to *path* and close it.

    Parameters
    ----------
    fig  : matplotlib Figure
    path : output file path (extension determines format: .png, .pdf, etc.)
    bg   : background color for the saved file
    dpi  : resolution
    """
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor=bg)
    plt.close(fig)


# ── convenience: draw a highlight ring around a node ─────────────────────────

def draw_highlight(
    ax,
    location,
    *,
    node_radius=DEFAULT_NODE_RADIUS,
    color="#ffcc00",
    lw=3.0,
    extra_radius=0.18,
    zorder=2,
):
    """
    Draw a dashed highlight ring around a node (used to call out violations).

    Parameters
    ----------
    location     : (x, y) center of the node
    node_radius  : radius of the node circle
    color        : ring color
    lw           : ring line width
    extra_radius : how much larger than the node the ring is
    """
    ring = mpatches.Circle(
        location, node_radius + extra_radius,
        facecolor="none",
        edgecolor=color,
        linewidth=lw,
        linestyle="--",
        zorder=zorder,
    )
    ax.add_patch(ring)
