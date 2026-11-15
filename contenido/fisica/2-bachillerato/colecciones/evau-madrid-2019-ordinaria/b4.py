"""Verificación de fis2b-evau-madrid-2019-ord-b4 (reflejado y refractado a 90°)."""

import math

n1, n2 = 1.6, 1.3


def resolver() -> dict:
    i1 = math.atan(n2 / n1)
    ic = math.pi / 2 - i1
    return {"i1": math.degrees(i1), "ic": math.degrees(ic), "n3": n2 * math.sin(ic)}


def comprobar(res: dict) -> None:
    i1 = math.radians(res["i1"])
    r = math.asin(n1 * math.sin(i1) / n2)            # Snell
    # Direcciones (2D, superficie horizontal): reflejado hacia arriba, refractado hacia abajo.
    refl = (math.sin(i1), math.cos(i1))
    refr = (math.sin(r), -math.cos(r))
    assert abs(refl[0] * refr[0] + refl[1] * refr[1]) < 1e-12, "forman 90°"
    assert math.isclose(math.degrees(r), res["ic"], rel_tol=1e-12)
    assert math.isclose(res["n3"], n1 * math.sin(i1), rel_tol=1e-12)
