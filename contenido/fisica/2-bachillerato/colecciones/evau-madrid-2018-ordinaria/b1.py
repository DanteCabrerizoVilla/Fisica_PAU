"""Verificación de fis2b-evau-madrid-2018-ord-b1 (órbita con periodo doble)."""

import math

G, M, m, T1 = 6.67e-11, 5.97e24, 1000.0, 86400.0


def radio(T):
    return (G * M * T**2 / (4 * math.pi**2)) ** (1 / 3)


def resolver() -> dict:
    r1, r2 = radio(T1), radio(2 * T1)
    return {"r2": r2, "dE": -G * M * m / (2 * r2) + G * M * m / (2 * r1)}


def comprobar(res: dict) -> None:
    r2 = res["r2"]
    assert math.isclose(2 * math.pi * r2 / math.sqrt(G * M / r2), 2 * T1, rel_tol=1e-12)
    assert math.isclose(r2 / radio(T1), 2 ** (2 / 3), rel_tol=1e-12)
    assert res["dE"] > 0
