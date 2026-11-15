"""Verificación de fis2b-evau-madrid-2018-mod-a2 (altavoces iguales)."""

import math

b1, bT = 60.0, 70.0


def resolver() -> dict:
    n = 10 ** ((bT - b1) / 10)
    return {"n": n, "fraccion": 1 / n}


def comprobar(res: dict) -> None:
    I0, r = 1e-12, 3.0
    P1 = I0 * 10 ** (b1 / 10) * 4 * math.pi * r**2
    total = 10 * math.log10(res["n"] * P1 / (4 * math.pi * r**2) / I0)
    assert math.isclose(total, bT, rel_tol=1e-12)
    assert math.isclose(res["n"], 10)
