"""Verificación de fis2b-evau-madrid-2020-ord-b3 (cuatro cargas alternadas en un cuadrado)."""

import math

import numpy as np

K, q, a = 9e9, 1e-6, 0.30
cargas = {(0, 0): q, (a, a): q, (0, a): -q, (a, 0): -q}


def resolver() -> dict:
    P = np.array([a, a])
    F = sum(K * Q * q * (P - np.array(p)) / np.linalg.norm(P - np.array(p)) ** 3
            for p, Q in cargas.items() if p != (a, a))
    V0 = sum(K * Q / math.dist((0, 0), p) for p, Q in cargas.items() if p != (0, 0))
    return {"F_x": F[0], "F_y": F[1], "Ep": q * V0}


def comprobar(res: dict) -> None:
    # Segunda vía para la fuerza: −gradiente de la energía de la carga en (a, a).
    def U(p):
        return sum(K * Q * q / math.dist(p, c) for c, Q in cargas.items() if c != (a, a))
    h = 1e-7
    Fx = -(U((a + h, a)) - U((a - h, a))) / (2 * h)
    assert math.isclose(Fx, res["F_x"], rel_tol=1e-6)
    assert math.isclose(res["F_x"], res["F_y"], rel_tol=1e-12)
    assert math.isclose(res["F_x"], -0.065, rel_tol=1e-2) and math.isclose(res["Ep"], -0.039, rel_tol=1e-2)
