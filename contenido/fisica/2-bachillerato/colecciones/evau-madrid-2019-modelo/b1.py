"""Verificación de fis2b-evau-madrid-2019-mod-b1 (planeta Cibeles y estrella Aya)."""

import math

G, Rc, h, t = 6.67e-11, 8.5e6, 10.0, 1.58
R, T = 1.8e11, 395 * 86400


def resolver() -> dict:
    g = 2 * h / t**2
    return {"g": g, "Mc": g * Rc**2 / G, "Ma": 4 * math.pi**2 * R**3 / (G * T**2)}


def comprobar(res: dict) -> None:
    # Caída con g constante: posición tras 1,58 s.
    assert math.isclose(0.5 * res["g"] * t**2, h, rel_tol=1e-12)
    v = math.sqrt(G * res["Ma"] / R)
    assert math.isclose(2 * math.pi * R / v, T, rel_tol=1e-12)
    # Oficial: g = 8,01 m/s², Mc = 8,68·10²⁴ kg, Ma = 2,96·10³⁰ kg.
    assert math.isclose(res["Mc"], 8.68e24, rel_tol=1e-3) and math.isclose(res["Ma"], 2.96e30, rel_tol=2e-3)
