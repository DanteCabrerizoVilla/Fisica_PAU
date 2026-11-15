"""Verificación de fis2b-evau-madrid-2018-ext-b1 (satélite de 694 a 1000 km)."""

import math

G, M, R, m = 6.67e-11, 5.97e24, 6.37e6, 712.0
r1, r2 = R + 694e3, R + 1000e3


def resolver() -> dict:
    v = math.sqrt(G * M / r1)
    return {"v": v, "T": 2 * math.pi * r1 / v, "dE": G * M * m / 2 * (1 / r1 - 1 / r2)}


def comprobar(res: dict) -> None:
    E = lambda r: 0.5 * m * (G * M / r) - G * M * m / r
    assert math.isclose(E(r2) - E(r1), res["dE"], rel_tol=1e-10)
    assert math.isclose(res["T"], 2 * math.pi * math.sqrt(r1**3 / (G * M)), rel_tol=1e-12)
