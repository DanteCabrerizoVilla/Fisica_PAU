"""Verificación de fis2b-evau-madrid-2019-ext-b1 (Europa y Júpiter)."""

import math

G, r, T, RJ = 6.67e-11, 6.711e8, 3.55 * 86400, 6.9911e7


def resolver() -> dict:
    M = 4 * math.pi**2 * r**3 / (G * T**2)
    return {"M": M, "ve": math.sqrt(2 * G * M / RJ)}


def comprobar(res: dict) -> None:
    v = math.sqrt(G * res["M"] / r)
    assert math.isclose(2 * math.pi * r / v, T, rel_tol=1e-12)
    # Con la velocidad de escape, la energía mecánica en la superficie es cero.
    assert abs(0.5 * res["ve"] ** 2 - G * res["M"] / RJ) < 1e-6 * G * res["M"] / RJ
