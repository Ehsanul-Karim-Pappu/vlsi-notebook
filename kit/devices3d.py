"""Devices built from box geometry in nanometres (FET Lab's format): in 3D, whole or cut away,
and flat, as the top view a layout tool shows.

Each part is a list of boxes [cx, cy, cz, w, h, d]: x runs along the channel, y is height and
z is across the channel. Manim's z axis points up, so FET Lab's (x, y, z) becomes (x, z, y).
"""

import numpy as np
from manim import Prism, Rectangle, Union, VGroup

from kit.style import BG

# Fills for plan_view() that read like a layout tool: thin channel layers (fins, sheets) nearly
# solid, so they show through the contacts, gates and metal drawn over them.
LAYOUT_OPACITY = {"default": 0.5, "pwell": 0.3, "nwell": 0.3, "nanowire": 0.95, "po": 0.55, "md": 0.35, "m0": 0.35}

AXES = {"x": 0, "y": 1, "z": 2}


def _clip_box(box, clip):
    """The box's [lo, hi] along each FET Lab axis, cut to CLIP ({"x": (lo, hi), ...}, None for
    an open end). None if nothing is left."""
    cx, cy, cz, w, h, d = box
    spans = [[cx - w / 2, cx + w / 2], [cy - h / 2, cy + h / 2], [cz - d / 2, cz + d / 2]]
    for axis, (lo, hi) in (clip or {}).items():
        s = spans[AXES[axis]]
        if lo is not None:
            s[0] = max(s[0], lo)
        if hi is not None:
            s[1] = min(s[1], hi)
        if s[1] - s[0] <= 1e-6:
            return None
    return spans


def part_mobject(part, materials, scale, opacity=1.0, keep=None, color=None, clip=None):
    """One part as Prisms. keep="back" or "front" keeps only the half behind or in front of
    the plane through the channel's centre (FET Lab z = 0); clip={"x": (None, 0)} keeps what
    lies in a range along any axis, for other cutaways."""
    color = color or materials.get(part["material"], {}).get("color", "#888888")
    clip = dict(clip or {})
    if keep == "back":
        clip["z"] = (0.0, None)
    elif keep == "front":
        clip["z"] = (None, 0.0)
    boxes = VGroup()
    for b in part["boxes"]:
        spans = _clip_box(b, clip)
        if spans is None:
            continue
        (x0, x1), (y0, y1), (z0, z1) = spans
        box = Prism(dimensions=[(x1 - x0) * scale, (z1 - z0) * scale, (y1 - y0) * scale])
        box.move_to([(x0 + x1) / 2 * scale, (z0 + z1) / 2 * scale, (y0 + y1) / 2 * scale])
        box.set_fill(color, opacity=opacity)
        box.set_stroke(BG, width=0.6, opacity=0.6)
        boxes.add(box)
    return boxes


def build_device(geometry, scale=0.045, groups=None, skip=(), opacity=1.0, keep=None, recolor=None, clip=None):
    """Return (device, by_group): the whole device and a dict of its parts by FET Lab group.

    groups: an optional list of group names to keep, in build order.
    skip: part ids to leave out (contacts, say, to keep a picture simple).
    keep, clip: cut the device open (see part_mobject).
    recolor: {part id: colour} to pick parts out, such as the channel.
    """
    recolor = recolor or {}
    materials = geometry["materials"]
    by_group = {}
    for part in geometry["parts"]:
        if part["id"] in skip or (groups is not None and part["group"] not in groups):
            continue
        mob = part_mobject(part, materials, scale, opacity, keep, recolor.get(part["id"]), clip)
        by_group.setdefault(part["group"], VGroup()).add(mob)
    order = groups or list(by_group)
    device = VGroup(*[by_group[g] for g in order if g in by_group])
    return device, by_group


def beside(theta, dx):
    """For a 3D slide: the point the camera should look at (its frame_center) so that a device
    at the origin appears DX units right of the screen's centre (left if DX < 0), seen from
    azimuth THETA. Leaves room for text beside it."""
    right = np.array([-np.sin(theta), np.cos(theta), 0.0])
    return -dx * right


def plan_view(geometry, scale=0.03, skip=(), opacity=0.6, recolor=None):
    """The device seen from above, the way a layout tool draws it: each part's outline in the
    x-z plane, filled with its material's colour, the higher parts drawn over the lower. On
    screen, x (along the channel) runs right and z (across it) runs up, so gates run up the
    page and power rails across it.

    opacity: one fill opacity for every part, or {material: opacity} (with "default"), so thin
    layers such as fins can show through the ones drawn over them.

    Returns (view, by_id): the whole view, and each part's shape by part id.
    """
    recolor = recolor or {}
    materials = geometry["materials"]
    shapes = []
    for part in geometry["parts"]:
        if part["id"] in skip:
            continue
        color = recolor.get(part["id"]) or materials.get(part["material"], {}).get("color", "#888888")
        rects = [Rectangle(width=w * scale, height=d * scale).move_to([cx * scale, cz * scale, 0])
                 for cx, cy, cz, w, h, d in part["boxes"]]
        shape = rects[0] if len(rects) == 1 else Union(*rects)
        alpha = opacity.get(part["material"], opacity.get("default", 0.6)) if isinstance(opacity, dict) else opacity
        shape.set_fill(color, opacity=alpha).set_stroke(color, width=1.5, opacity=1.0)
        top = max(cy + h / 2 for cx, cy, cz, w, h, d in part["boxes"])
        shapes.append((top, part["id"], shape))
    shapes.sort(key=lambda s: s[0])
    view = VGroup(*[s for _, _, s in shapes])
    return view, {pid: s for _, pid, s in shapes}
