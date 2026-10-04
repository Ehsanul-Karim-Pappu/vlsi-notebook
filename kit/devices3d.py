"""3D devices built from box geometry in nanometres (FET Lab's format).

Each part is a list of boxes [cx, cy, cz, w, h, d]: x runs along the channel, y is height and
z is across the channel. Manim's z axis points up, so FET Lab's (x, y, z) becomes (x, z, y).
"""

from manim import Prism, VGroup

from kit.style import BG


def part_mobject(part, materials, scale, opacity=1.0, keep=None, color=None):
    """One part as Prisms. keep="back" or "front" keeps only the half behind or in front of
    the plane through the channel's centre (FET Lab z = 0), for cutaways."""
    color = color or materials.get(part["material"], {}).get("color", "#888888")
    boxes = VGroup()
    for cx, cy, cz, w, h, d in part["boxes"]:
        lo, hi = cz - d / 2, cz + d / 2
        if keep == "back":
            lo = max(lo, 0.0)
        elif keep == "front":
            hi = min(hi, 0.0)
        if hi - lo <= 1e-6:
            continue
        box = Prism(dimensions=[w * scale, (hi - lo) * scale, h * scale])
        box.move_to([cx * scale, (lo + hi) / 2 * scale, cy * scale])
        box.set_fill(color, opacity=opacity)
        box.set_stroke(BG, width=0.6, opacity=0.6)
        boxes.add(box)
    return boxes


def build_device(geometry, scale=0.045, groups=None, skip=(), opacity=1.0, keep=None, recolor=None):
    """Return (device, by_group): the whole device and a dict of its parts by FET Lab group.

    groups: an optional list of group names to keep, in build order.
    skip: part ids to leave out (contacts, say, to keep a picture simple).
    keep: "back" or "front" for one half of a cutaway (see part_mobject).
    recolor: {part id: colour} to pick parts out, such as the channel.
    """
    recolor = recolor or {}
    materials = geometry["materials"]
    by_group = {}
    for part in geometry["parts"]:
        if part["id"] in skip or (groups is not None and part["group"] not in groups):
            continue
        mob = part_mobject(part, materials, scale, opacity, keep, recolor.get(part["id"]))
        by_group.setdefault(part["group"], VGroup()).add(mob)
    order = groups or list(by_group)
    device = VGroup(*[by_group[g] for g in order if g in by_group])
    return device, by_group
