"""Verificación de fis2b-evau-madrid-2020-mod-a1 (satélite UARS)."""

import math

G, M, R, m = 6.67e-11, 5.97e24, 6.371e6, 5800
T = 86400 / 15


def resolver() -> dict:
    r = (G * M * T**2 / (4 * math.pi**2)) ** (1 / 3)
    return {"h": r - R, "E": -G * M * m / (2 * r)}


def comprobar(res: dict) -> None:
    r = res["h"] + R
    v = math.sqrt(G * M / r)
    assert math.isclose(2 * math.pi * r / v, T, rel_tol=1e-12)
    assert math.isclose(0.5 * m * v**2 - G * M * m / r, res["E"], rel_tol=1e-12)
    # Solución oficial: h = 571 701 m y E = −1,66·10¹¹ J.
    assert math.isclose(res["h"], 571701.05, rel_tol=1e-6) and math.isclose(res["E"], -1.66e11, rel_tol=3e-3)
