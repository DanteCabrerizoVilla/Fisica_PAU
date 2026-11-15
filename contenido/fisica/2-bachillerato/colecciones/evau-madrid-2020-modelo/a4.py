"""Verificación de fis2b-evau-madrid-2020-mod-a4 (lente planoconvexa de 10 D)."""

import math

P, n, s = 10.0, 1.6, -20.0
f = 100 / P   # cm


def resolver() -> dict:
    r = (n - 1) / P * 100
    sp = 1 / (1 / f + 1 / s)
    s_b = f * (1 / 2 - 1)        # M = +2 → s = f(1/M − 1)
    return {"r": r, "sp": sp, "s_b": s_b}


def comprobar(res: dict) -> None:
    r = res["r"] / 100
    assert math.isclose((n - 1) * (1 / r - 0), P, rel_tol=1e-12)
    assert math.isclose((n - 1) * (0 - 1 / -r), P, rel_tol=1e-12)    # dada la vuelta
    sb = res["s_b"]
    spb = 1 / (1 / f + 1 / sb)
    assert spb < 0 and math.isclose(spb / sb, 2, rel_tol=1e-12)
    assert math.isclose(res["sp"], 20) and math.isclose(sb, -5)
