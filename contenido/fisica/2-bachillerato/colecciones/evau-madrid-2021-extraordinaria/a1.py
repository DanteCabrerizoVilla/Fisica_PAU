"""Verificación de fis2b-evau-madrid-2021-ext-a1 (planeta desconocido)."""

import math

G = 6.67e-11
v, T, rho = 25000 / 3.6, 5 * 3600, 16150


def resolver() -> dict:
    r = v * T / (2 * math.pi)
    M = r * v**2 / G
    R = (3 * M / (4 * math.pi * rho)) ** (1 / 3)
    return {"r": r, "M": M, "R": R, "g": G * M / R**2}


def comprobar(res: dict) -> None:
    # Segunda vía para la masa: tercera ley de Kepler con r y T.
    assert math.isclose(4 * math.pi**2 * res["r"] ** 3 / (G * T**2), res["M"], rel_tol=1e-12)
    # Segunda vía para g: g = (4/3)·π·G·ρ·R.
    assert math.isclose(4 / 3 * math.pi * G * rho * res["R"], res["g"], rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["r"], 1.989437e7, rel_tol=1e-6) and math.isclose(res["M"], 1.44e25, rel_tol=2e-3)
    assert math.isclose(res["R"], 5968.60e3, rel_tol=1e-4) and math.isclose(res["g"], 26.93, rel_tol=1e-3)
