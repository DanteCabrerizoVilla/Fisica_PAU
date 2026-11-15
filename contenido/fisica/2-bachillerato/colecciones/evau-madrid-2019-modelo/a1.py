"""Verificación de fis2b-evau-madrid-2019-mod-a1 (masa de un planeta)."""

import math

G, m, T, v = 6.67e-11, 150, 1800, 2.3e4


def resolver() -> dict:
    r = v * T / (2 * math.pi)
    M = v**2 * r / G
    return {"M": M, "E": 0.5 * m * v**2 - G * M * m / r}


def comprobar(res: dict) -> None:
    r = (G * res["M"] * T**2 / (4 * math.pi**2)) ** (1 / 3)   # tercera ley de Kepler
    assert math.isclose(2 * math.pi * r / T, v, rel_tol=1e-12)
    assert math.isclose(res["E"], -0.5 * m * v**2, rel_tol=1e-12)
    # Oficial: M = 5,22·10²⁵ kg (truncado; sale 5,226·10²⁵), E = −3,97·10¹⁰ J.
    assert math.isclose(res["M"], 5.22e25, rel_tol=3e-3) and math.isclose(res["E"], -3.97e10, rel_tol=1e-3)
