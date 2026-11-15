"""Verificación de fis2b-evau-madrid-2019-ord-b1 (satélite geoestacionario)."""

import math

G, M, R, m, T = 6.67e-11, 5.97e24, 6.37e6, 5900, 86400


def resolver() -> dict:
    r = (G * M * T**2 / (4 * math.pi**2)) ** (1 / 3)
    v = 2 * math.pi * r / T
    return {"h": r - R, "v": v, "F": m * v**2 / r, "E": -G * M * m / (2 * r)}


def comprobar(res: dict) -> None:
    r = res["h"] + R
    assert math.isclose(res["F"], G * M * m / r**2, rel_tol=1e-12)
    assert math.isclose(res["v"], math.sqrt(G * M / r), rel_tol=1e-12)
    assert math.isclose(res["E"], 0.5 * m * res["v"] ** 2 - G * M * m / r, rel_tol=1e-12)
