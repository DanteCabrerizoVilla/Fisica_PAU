"""Verificación de fis2b-evau-madrid-2021-mod-a3 (dos cargas iguales y partícula que se aleja)."""

import math

import numpy as np

K, q = 9e9, 5e-9
cargas = [np.array([0.0, 3.0]), np.array([0.0, -3.0])]
m, Q, v0 = 3e-3, 3e-3, 2.0


def E(p):
    return sum(K * q * (p - r) / np.linalg.norm(p - r) ** 3 for r in cargas)


def V(p):
    return sum(K * q / np.linalg.norm(p - r) for r in cargas)


def resolver() -> dict:
    O, P = np.zeros(2), np.array([4.0, 0.0])
    return {"E": E(P)[0], "v": math.sqrt(v0**2 + 2 * Q * (V(O) - V(P)) / m)}


def comprobar(res: dict) -> None:
    assert abs(E(np.array([4.0, 0]))[1]) < 1e-12
    # Segunda vía: integrar el movimiento sobre el eje x hasta x = 4 m (Verlet).
    x, v, dt = 0.0, v0, 1e-4
    a = Q * E(np.array([x, 0.0]))[0] / m
    while x < 4.0:
        xn = x + v * dt + 0.5 * a * dt**2
        an = Q * E(np.array([xn, 0.0]))[0] / m
        v += 0.5 * (a + an) * dt
        x, a = xn, an
    assert math.isclose(v, res["v"], rel_tol=2e-3)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["E"], 2.88) and math.isclose(res["v"], 5.29, rel_tol=1e-3)
