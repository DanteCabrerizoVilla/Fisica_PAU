"""Verificación de fis2b-evau-madrid-2018-mod-a1 (masas de 2 y 10 kg)."""

import math
from scipy.optimize import brentq

G, m1, m2, d = 6.67e-11, 2.0, 10.0, 5.0


def resolver() -> dict:
    x = d / (1 + math.sqrt(m2 / m1))
    return {"x": x, "V": -G * (m1 / x + m2 / (d - x))}


def comprobar(res: dict) -> None:
    g = lambda x: -G * m1 / x**2 + G * m2 / (d - x) ** 2
    assert math.isclose(brentq(g, 0.01, 4.99), res["x"], rel_tol=1e-10)
    # Oficial: x = 1,55 m, V = −2,79·10⁻¹⁰ J/kg.
    assert math.isclose(res["V"], -2.79e-10, rel_tol=2e-3)
