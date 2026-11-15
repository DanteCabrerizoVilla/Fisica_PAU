"""Verificación de fis2b-evau-madrid-2019-ext-a1 (satélites LAGEOS)."""

import math

G, M, R, m, h = 6.67e-11, 5.97e24, 6.37e6, 405, 5.9e6


def resolver() -> dict:
    r = R + h
    return {"T": 2 * math.pi * math.sqrt(r**3 / (G * M)), "dE": G * M * m * (1 / R - 1 / (2 * r))}


def comprobar(res: dict) -> None:
    r = R + h
    v = math.sqrt(G * M / r)
    dEp = -G * M * m / r + G * M * m / R
    assert math.isclose(dEp + 0.5 * m * v**2, res["dE"], rel_tol=1e-12)
    assert math.isclose(2 * math.pi * r / v, res["T"], rel_tol=1e-12)
