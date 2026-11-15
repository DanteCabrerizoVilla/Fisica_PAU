"""Verificación de fis2b-evau-madrid-2020-mod-b1 (nuevo sistema solar)."""

import math

G, Ms = 6.67e-11, 6.0e30
T = 3 * 365 * 24 * 3600
g, ve = 15.0, 11.2e3


def resolver() -> dict:
    R = ve**2 / (2 * g)
    return {"r": (G * Ms * T**2 / (4 * math.pi**2)) ** (1 / 3), "R": R, "M": g * R**2 / G}


def comprobar(res: dict) -> None:
    v = math.sqrt(G * Ms / res["r"])
    assert math.isclose(2 * math.pi * res["r"] / v, T, rel_tol=1e-12)
    assert math.isclose(G * res["M"] / res["R"] ** 2, g, rel_tol=1e-12)
    assert math.isclose(math.sqrt(2 * G * res["M"] / res["R"]), ve, rel_tol=1e-12)
    # Oficial: r = 4,49·10¹¹ m, R = 4180 km, M = 3,93·10²⁴ kg.
    assert math.isclose(res["r"], 4.49e11, rel_tol=1e-3) and math.isclose(res["M"], 3.93e24, rel_tol=1e-3)
