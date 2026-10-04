"""FET Lab's device models (data/devices.json and data/geometry.json), ready for kit.devices3d.

    from devicedata import device, NANOSHEET
    fin = device("fin")        # {"parts": [...], "materials": {...}}, as build_device takes it
"""

import json
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data"
_DEVICES = json.loads((DATA / "devices.json").read_text())
_BY_KEY = {d["key"]: d for d in _DEVICES["devices"]}
NANOSHEET = json.loads((DATA / "geometry.json").read_text())


def device(key):
    """One device model from devices.json, with the shared material colours."""
    d = _BY_KEY[key]
    return {"parts": d["parts"], "materials": _DEVICES["materials"], "name": d["name"], "callouts": d.get("callouts", [])}


def rail_span_nm(key):
    """The distance between a layout cell's V_DD and GND rail centres (FET Lab's show_ models)."""
    z = {}
    for p in device(key)["parts"]:
        if p.get("net") in ("vdd", "gnd") and p["material"] == "m0":
            z[p["net"]] = p["boxes"][0][2]
    return abs(z["vdd"] - z["gnd"])
