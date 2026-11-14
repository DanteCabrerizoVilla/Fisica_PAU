"""Verificación de fis2b-evau-madrid-2020-ext-a1 (Calisto)."""

import math

G, MJ = 6.67e-11, 1.90e27
rho, R, T = 1830.0, 2.41e6, 16.89 * 86400


def resolver() -> dict:
    M = rho * 4 / 3 * math.pi * R**3
    r = (G * MJ * T**2 / (4 * math.pi**2)) ** (1 / 3)
    v = 2 * math.pi * r / T
    return {"M": M, "g": G * M / R**2, "Ec": 0.5 * M * v**2, "Em": -G * MJ * M / (2 * r)}


def comprobar(res: dict) -> None:
    assert math.isclose(res["Ec"], -res["Em"], rel_tol=1e-9)
    assert math.isclose(res["g"], 4 / 3 * math.pi * G * rho * R, rel_tol=1e-12)
    assert math.isclose(res["M"], 1.07e23, rel_tol=3e-3) and math.isclose(res["g"], 1.23, rel_tol=3e-3)
    assert math.isclose(res["Ec"], 3.58e30, rel_tol=2e-3)
