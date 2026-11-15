"""Verificación de fis2b-evau-madrid-2019-ext-b4 (trampolín y piscina)."""

import math
from scipy.optimize import brentq

n, H, P, ang = 1.33, 4.0, 3.0, math.radians(30)


def resolver() -> dict:
    r = math.asin(math.sin(ang) / n)
    return {"d": H * math.tan(ang) + P * math.tan(r), "L": math.degrees(math.asin(1 / n))}


def comprobar(res: dict) -> None:
    # Principio de Fermat: el punto de cruce de la superficie minimiza el tiempo de Carlos a Laura.
    d = res["d"]
    dt = lambda x: x / math.hypot(x, H) - n * (d - x) / math.hypot(d - x, P)
    x = brentq(dt, 0, d)
    assert math.isclose(math.degrees(math.atan(x / H)), 30, rel_tol=1e-9)
