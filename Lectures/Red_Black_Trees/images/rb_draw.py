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




Level 1
  idx 2   →  (1.750, 3.1)      idx 3   →  (5.250, 3.1)

Level 2
  idx 4   →  (0.875, 2.2)      idx 5   →  (2.625, 2.2)
  idx 6   →  (4.375, 2.2)      idx 7   →  (6.125, 2.2)

Level 3
  idx 8   →  (0.438, 1.3)      idx 9   →  (1.313, 1.3)
  idx 10  →  (2.188, 1.3)      idx 11  →  (3.063, 1.3)
  idx 12  →  (3.938, 1.3)      idx 13  →  (4.813, 1.3)
  idx 14  →  (5.688, 1.3)      idx 15  →  (6.563, 1.3)
Relative offsets from any parent to its children (the pattern):


dy is always  -0.9  (every level down)

dx depends on parent's level:
  Parent at level 0  →  dx = ± 1.750
  Parent at level 1  →  dx = ± 0.875
  Parent at level 2  →  dx = ± 0.438

Rule:  dx = ± (7.0 / 2^(parent_level + 2))
       left child  = parent_x - dx
       right child = parent_x + dx
So if you know a parent's (x, y) and level, every child location is just:


left_child  = (x - dx,  y - 0.9)
right_child = (x + dx,  y - 0.9)
"""

import math
import os
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# ── defaults ──────────────────────────────────────────────────────────────────
DEFAULT_NODE_RADIUS = 0.38
DEFAULT_FONT_SIZE = 16
DEFAULT_ANNOT_SIZE = 10
DEFAULT_EDGE_COLOR = "#444444"
DEFAULT_EDGE_LW = 2.2
DEFAULT_BG = "#f9f9f9"
DEFAULT_TEXT_COLOR = (1.0, 1.0, 1.0)  # white
DEFAULT_ANNOT_COLOR = "#222222"
DEFAULT_ANNOT_OFFSET = 1.2  # multiplier of node_radius for label distance


# ── cardinal direction tables ─────────────────────────────────────────────────
# Compass-bearing degrees (clockwise from North) → (ha, va) text alignment
_DIRECTION_ALIGN = {
    "N": ("center", "bottom"),
    "NE": ("left", "bottom"),
    "E": ("left", "center"),
    "SE": ("left", "top"),
    "S": ("center", "top"),
    "SW": ("right", "top"),
    "W": ("right", "center"),
    "NW": ("right", "bottom"),
}

# ── fixed tree grid ───────────────────────────────────────────────────────────
# Nodes are addressed by 1-based BST heap index:
#   1 = root, 2 = left child of root, 3 = right child of root,
#   4 = left-left, 5 = left-right, 6 = right-left, 7 = right-right, ...
#
# Every BST index maps to a unique, FIXED (x, y) regardless of what else
# is in the tree, so nodes never jump around between animation frames.

_TREE_WIDTH = 7.0  # matches xlim 0..7
_ROOT_Y = 4.0  # y of root node center
_DY = 0.90  # vertical gap between levels


def tree_pos(bst_index, tree_width, ry=4.0, dy=0.90):
    """Return the fixed (x, y) for a node at the given 1-based BST heap index."""
    level = bst_index.bit_length() - 1  # depth: root=0, children=1, …
    slot = bst_index - (1 << level)  # 0-based position within level
    span = tree_width / (1 << level)  # horizontal slot width at this depth
    x = span * (slot + 0.5)
    y = ry - level * dy
    return (x, y)


# Compass bearing → (dx_unit, dy_unit) in matplotlib data space
# Convert clockwise-from-North bearing to counterclockwise-from-East for math:
#   math_angle = 90 - bearing
def _cardinal_to_unit(direction: str):
    """Return unit (dx, dy) for a cardinal direction string."""
    degrees = {
        "N": 0,
        "NE": 45,
        "E": 90,
        "SE": 135,
        "S": 180,
        "SW": 225,
        "W": 270,
        "NW": 315,
    }
    if direction.upper() not in degrees:
        raise ValueError(
            f"Unknown direction '{direction}'. "
            f"Must be one of: {list(degrees.keys())}"
        )
    bearing = degrees[direction.upper()]
    math_rad = math.radians(90 - bearing)  # convert bearing → standard angle
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
    if r > 1 or g > 1 or b > 1:  # looks like 0-255
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
    id,  # int  — node identifier (metadata; optionally shown)
    location,  # (x, y) in data coordinates
    label,  # str  — text rendered inside the circle
    color,  # RGB tuple (0–255 or 0.0–1.0) or mpl color string
    annotation_list=None,  # [(label_str, cardinal_dir), ...]
    *,
    node_radius=DEFAULT_NODE_RADIUS,
    font_size=DEFAULT_FONT_SIZE,
    text_color=DEFAULT_TEXT_COLOR,
    annot_size=DEFAULT_ANNOT_SIZE,
    annot_color=DEFAULT_ANNOT_COLOR,
    annot_offset=DEFAULT_ANNOT_OFFSET,
    show_id=False,  # if True, draw `id` as a small superscript above node
    edge_color="white",  # outline color of the circle
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
        (x, y),
        node_radius,
        facecolor=fill,
        edgecolor=edge_color,
        linewidth=edge_lw,
        zorder=zorder,
    )
    ax.add_patch(circle)

    # label inside circle
    ax.text(
        x,
        y,
        str(label),
        ha="center",
        va="center",
        fontsize=font_size,
        fontweight="bold",
        color=_norm_color(text_color),
        zorder=zorder + 1,
    )

    # optional id superscript (small, top-right corner of circle)
    if show_id:
        ax.text(
            x + node_radius * 0.75,
            y + node_radius * 0.75,
            str(id),
            ha="left",
            va="bottom",
            fontsize=annot_size - 2,
            color="#888888",
            zorder=zorder + 1,
        )

    # annotations
    for entry in annotation_list or []:
        # accept either (text, direction) or (text, direction, color)
        if len(entry) == 3:
            ann_text, direction, ann_col = entry
        else:
            ann_text, direction = entry
            ann_col = annot_color

        dx, dy = _cardinal_to_unit(direction)
        dist = node_radius * annot_offset
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
        "",
        xy=to_xy,
        xytext=from_xy,
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


# ── free text label ──────────────────────────────────────────────────────────


def draw_text(
    ax,
    location,
    text,
    *,
    fontsize=11,
    color="#222222",
    ha="center",
    va="center",
    fontweight="normal",
    style="normal",
    zorder=5,
):
    """
    Place a text string at an arbitrary (x, y) location.

    Parameters
    ----------
    ax         : matplotlib Axes
    location   : (x, y) in data coordinates
    text       : string to display
    fontsize   : font size
    color      : text color (any mpl color string or RGB tuple)
    ha         : horizontal alignment — "left", "center", "right"
    va         : vertical alignment  — "top", "center", "bottom"
    fontweight : "normal", "bold", etc.
    style      : "normal", "italic", "oblique"
    zorder     : draw order
    """
    ax.text(
        location[0],
        location[1],
        text,
        ha=ha,
        va=va,
        fontsize=fontsize,
        color=_norm_color(color),
        fontweight=fontweight,
        style=style,
        zorder=zorder,
    )


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
        location,
        node_radius + extra_radius,
        facecolor="none",
        edgecolor=color,
        linewidth=lw,
        linestyle="--",
        zorder=zorder,
    )
    ax.add_patch(ring)


# ── SlideBuilder ──────────────────────────────────────────────────────────────


class SlideBuilder:
    """
    Declarative pipeline for building a sequence of tree-diagram images.

    State (nodes, edges, texts, highlights) accumulates across calls.
    Each snapshot() re-renders the current state to a fresh figure and saves it.
    Methods return self so calls can be chained.

    Quick example
    -------------
        BLACK = (44, 44, 44)
        RED   = (0.91, 0.30, 0.24)

        s = SlideBuilder(width=9, height=6, title="Case 1", out_dir=".")

        # build initial tree and save
        s.node(1, "10", BLACK, annotations=[("G", "N")])
        s.node(2,  "5", RED,   annotations=[("P", "N")])
        s.node(3, "15", RED,   annotations=[("U", "N")])
        s.snapshot("img_01.png")

        # add new node — edges auto-generated from BST indices
        s.node(4, "1", RED, annotations=[("N", "N", "#2980b9")])
        s.snapshot("img_02.png")

        # recolor for Case 1 fix, drop transient text
        s.update(1, color=RED).update(2, color=BLACK).update(3, color=BLACK)
        s.text((4.5, 0.4), "Recolor: P→B, U→B, G→R", color="#c0392b")
        s.snapshot("img_03.png")

        # Rule 2 fix
        s.update(1, color=BLACK).clear_texts()
        s.snapshot("img_04.png")
    """

    def __init__(
        self,
        width=9,
        height=6,
        bg=DEFAULT_BG,
        title="",
        xlim=None,
        ylim=None,
        annot_size=12,
        out_dir=".",
    ):
        self._width  = width
        self._height = height
        self._bg     = bg
        self._title  = title
        self._xlim   = xlim or (0, width)
        self._ylim   = ylim or (0, height)
        self._out_dir       = out_dir
        self._annot_size    = annot_size
        self._auto_edges    = True        # derive edges from BST parent-child pairs

        self._nodes     = {}   # bst_id → dict of draw_node kwargs
        self._man_edges = []   # [(from_id, to_id), ...]  manual edges
        self._texts     = []   # [(location, text, kwargs), ...]
        self._highlights= []   # [(bst_id_or_xy, kwargs), ...]

    # ── tree width helper ─────────────────────────────────────────────────────
    @property
    def _tw(self):
        return self._xlim[1] - self._xlim[0]

    # ── node management ───────────────────────────────────────────────────────

    def node(self, bst_id, label, color, annotations=None, **kwargs):
        """Add or replace a node.  BST index determines position automatically."""
        self._nodes[bst_id] = dict(
            label=label,
            color=color,
            annotation_list=annotations or [],
            annot_size=kwargs.pop("annot_size", self._annot_size),
            **kwargs,
        )
        return self

    def update(self, bst_id, **kwargs):
        """Update one or more properties of an existing node."""
        if bst_id not in self._nodes:
            raise KeyError(f"Node {bst_id} not found — add it with .node() first")
        if "annotations" in kwargs:
            kwargs["annotation_list"] = kwargs.pop("annotations")
        self._nodes[bst_id].update(kwargs)
        return self

    def remove(self, bst_id):
        """Remove a node (and any manual edges that reference it)."""
        self._nodes.pop(bst_id, None)
        self._man_edges = [
            (f, t) for (f, t) in self._man_edges if f != bst_id and t != bst_id
        ]
        return self

    def move(self, from_id, to_id):
        """
        Relocate a node to a new BST index (e.g. after a rotation).
        The node data is preserved; only its grid position changes.
        """
        if from_id not in self._nodes:
            raise KeyError(f"Node {from_id} not found")
        self._nodes[to_id] = self._nodes.pop(from_id)
        return self

    # ── edge management ───────────────────────────────────────────────────────

    def auto_edges(self, enabled=True):
        """Toggle automatic BST parent→child edge generation (default: on)."""
        self._auto_edges = enabled
        return self

    def edge(self, from_id, to_id):
        """Add a manual edge by BST index pair."""
        self._man_edges.append((from_id, to_id))
        return self

    def clear_edges(self):
        """Clear all manual edges."""
        self._man_edges = []
        return self

    # ── text & highlights ─────────────────────────────────────────────────────

    def text(self, location, text, **kwargs):
        """Add a free-floating text label at (x, y)."""
        self._texts.append((location, text, kwargs))
        return self

    def highlight(self, bst_id_or_xy, **kwargs):
        """
        Add a dashed highlight ring.
        Pass a BST index (int) or an explicit (x, y) tuple.
        """
        self._highlights.append((bst_id_or_xy, kwargs))
        return self

    def clear_texts(self):
        self._texts = []
        return self

    def clear_highlights(self):
        self._highlights = []
        return self

    def clear_transients(self):
        """Clear texts and highlights (keep nodes/edges)."""
        return self.clear_texts().clear_highlights()

    # ── title ─────────────────────────────────────────────────────────────────

    def title(self, text):
        """Change the figure title for subsequent snapshots."""
        self._title = text
        return self

    # ── render ────────────────────────────────────────────────────────────────

    def snapshot(self, filename):
        """
        Render the current state to a new figure and save it.

        filename is relative to out_dir (set in __init__).
        Returns self so you can chain more mutations after saving.
        """
        fig, ax = new_figure(
            self._width, self._height, self._bg, self._xlim, self._ylim
        )
        if self._title:
            ax.set_title(self._title, fontsize=12, fontweight="bold")

        # ── edges (auto + manual, de-duplicated) ──────────────────────────────
        edge_set = set()
        if self._auto_edges:
            for nid in self._nodes:
                parent = nid >> 1
                if parent >= 1 and parent in self._nodes:
                    edge_set.add((parent, nid))
        for pair in self._man_edges:
            edge_set.add(pair)

        for (f, t) in edge_set:
            draw_edge(ax, tree_pos(f, self._tw), tree_pos(t, self._tw))

        # ── nodes ─────────────────────────────────────────────────────────────
        for nid, spec in self._nodes.items():
            draw_node(ax, id=nid, location=tree_pos(nid, self._tw), **spec)

        # ── highlights ────────────────────────────────────────────────────────
        for (ref, kwargs) in self._highlights:
            loc = tree_pos(ref, self._tw) if isinstance(ref, int) else ref
            draw_highlight(ax, loc, **kwargs)

        # ── free texts ────────────────────────────────────────────────────────
        for (loc, txt, kwargs) in self._texts:
            draw_text(ax, loc, txt, **kwargs)

        path = os.path.join(self._out_dir, filename)
        save_figure(fig, path, self._bg)
        print(f"  → {path}")
        return self


# ── HTML viewer ───────────────────────────────────────────────────────────────


def generate_viewer(folder, slides, title, bg_image="../redblacktree.jpg"):
    """
    Write a self-contained index.html slide viewer into folder.

    Parameters
    ----------
    folder    : output directory (created if needed)
    slides    : list of (filename, label) tuples — e.g. [("img1.png", "Step 1: ..."), ...]
    title     : page / h1 title
    bg_image  : path to background image relative to folder
    """
    import json
    frames_js = json.dumps([f for f, _ in slides])
    labels_js = json.dumps([l for _, l in slides])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background-color: #0d0000;
    background-image: url("{bg_image}");
    background-size: cover;
    background-position: center top;
    background-attachment: fixed;
    color: #eee;
    font-family: "Segoe UI", system-ui, sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 100vh;
    padding: 32px 16px;
    gap: 22px;
  }}
  body::before {{
    content: "";
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.68);
    z-index: 0;
  }}
  body > * {{ position: relative; z-index: 1; }}
  h1 {{
    font-size: 1.5rem;
    letter-spacing: 0.06em;
    color: #ff3c00;
    text-align: center;
    text-shadow: 0 0 12px rgba(255,60,0,0.9), 0 0 28px rgba(200,0,0,0.6), 0 0 60px rgba(160,0,0,0.35);
  }}
  .step-label {{
    font-size: 1rem;
    color: #cc9988;
    min-height: 1.4em;
    text-align: center;
    letter-spacing: 0.02em;
  }}
  .frame-box {{
    background: #f9f9f9;
    border-radius: 10px;
    box-shadow: 0 0 0 2px rgba(180,0,0,0.5), 0 0 28px rgba(220,30,0,0.4), 0 12px 40px rgba(0,0,0,0.85);
    overflow: hidden;
    max-width: 820px;
    width: 100%;
  }}
  .frame-box img {{ width: 100%; display: block; }}
  .nav {{ display: flex; align-items: center; gap: 28px; }}
  .nav button {{
    background: rgba(20,0,0,0.75);
    color: #ff6644;
    border: 2px solid #cc2200;
    border-radius: 8px;
    padding: 10px 30px;
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
    transition: background 0.15s, color 0.15s, border-color 0.15s, box-shadow 0.15s;
    letter-spacing: 0.06em;
    text-shadow: 0 0 8px rgba(255,80,0,0.6);
  }}
  .nav button:hover:not(:disabled) {{
    background: #cc2200; color: #fff; border-color: #ff4400;
    box-shadow: 0 0 18px rgba(200,30,0,0.7);
  }}
  .nav button:disabled {{ opacity: 0.25; cursor: default; }}
  .counter {{ font-size: 1.1rem; color: #bb9988; min-width: 80px; text-align: center; }}
  .hint {{ font-size: 0.78rem; color: #664444; letter-spacing: 0.04em; }}
</style>
</head>
<body>
<h1>{title}</h1>
<div class="step-label" id="step-label"></div>
<div class="frame-box">
  <img id="frame-img" src="" alt="slide">
</div>
<div class="nav">
  <button id="btn-prev" onclick="go(-1)">&#8592; Prev</button>
  <span class="counter" id="counter"></span>
  <button id="btn-next" onclick="go(1)">Next &#8594;</button>
</div>
<div class="hint">Arrow keys ← → also work</div>
<script>
  const frames = {frames_js};
  const labels = {labels_js};
  let cur = 0;
  function render() {{
    document.getElementById("frame-img").src = frames[cur];
    document.getElementById("step-label").textContent = labels[cur];
    document.getElementById("counter").textContent = (cur+1) + " / " + frames.length;
    document.getElementById("btn-prev").disabled = cur === 0;
    document.getElementById("btn-next").disabled = cur === frames.length - 1;
  }}
  function go(dir) {{
    const n = cur + dir;
    if (n >= 0 && n < frames.length) {{ cur = n; render(); }}
  }}
  document.addEventListener("keydown", e => {{
    if (e.key === "ArrowRight") go(1);
    if (e.key === "ArrowLeft")  go(-1);
  }});
  render();
</script>
</body>
</html>
"""
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "index.html")
    with open(path, "w") as f:
        f.write(html)
    print(f"  viewer → {path}")
