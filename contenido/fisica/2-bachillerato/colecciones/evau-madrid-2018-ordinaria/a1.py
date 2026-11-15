"""Verificación de fis2b-evau-madrid-2018-ord-a1 (atracción entre dos masas frente al peso)."""

import math

G, M, R = 6.67e-11, 5.97e24, 6.37e6
m1, m2, d = 10.0, 20.0, 1.0


def resolver() -> dict:
    F = G * m1 * m2 / d**2
    P = m2 * G * M / R**2
    return {"F12": F, "P2": P, "cociente": P / F}


def comprobar(res: dict) -> None:
    assert math.isclose(res["cociente"], (M / m1) * (d / R) ** 2, rel_tol=1e-12)
    assert math.isclose(res["P2"] / m2, 9.81, rel_tol=1e-3)
