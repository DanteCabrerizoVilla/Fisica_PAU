"""Verificación de fis2b-evau-madrid-2021-ordc-a3 (cuatro cargas en un cuadrado y electrón)."""

import math

import numpy as np

K, e, me = 9e9, 1.6e-19, 9.1e-31
cargas = [(5e-9, (-1, 1)), (5e-9, (1, 1)), (3e-9, (1, -1)), (3e-9, (-1, -1))]
v0 = 3e4


def V(p):
    return sum(K * q / math.dist(p, r) for q, r in cargas)


def E(p):
    p = np.asarray(p, float)
    return sum(K * q * (p - r) / np.linalg.norm(p - r) ** 3 for q, r in cargas)


def resolver() -> dict:
    Vi, Vf = V((0, 0)), V((0, 1))
    return {"E_y": E((0, 0))[1], "v": math.sqrt(v0**2 + 2 * e * (Vf - Vi) / me)}


def comprobar(res: dict) -> None:
    assert abs(E((0, 0))[0]) < 1e-12
    # Segunda vía: integrar el movimiento del electrón desde el centro hasta y = 1 m.
    # Por simetría se queda sobre el eje y.
    y, vy, dt = 0.0, v0, 2e-10
    while y < 1.0:
        a = -e * E((0, y))[1] / me
        vy += a * dt
        y += vy * dt
    assert math.isclose(vy, res["v"], rel_tol=1e-3)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["E_y"], -9 * math.sqrt(2), rel_tol=1e-12) and math.isclose(res["v"], 2.08e6, rel_tol=2e-3)
