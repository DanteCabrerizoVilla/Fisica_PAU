"""Verificación de fis2b-evau-madrid-2019-ext-a3 (cargas de 10 y 20 μC)."""

import math
import numpy as np

K, e = 9e9, 1.6e-19
cargas = [(10e-6, np.array([0.0, 0])), (20e-6, np.array([3.0, 0]))]
A, B = np.array([3.0, 4]), np.array([2.0, 0])


def V(p):
    return sum(K * q / np.linalg.norm(p - c) for q, c in cargas)


def E(p):
    return sum(K * q * (p - c) / np.linalg.norm(p - c) ** 3 for q, c in cargas)


def resolver() -> dict:
    return {"x": 3 / (1 + math.sqrt(2)), "W": -e * (V(A) - V(B))}


def comprobar(res: dict) -> None:
    assert np.linalg.norm(E(np.array([res["x"], 0]))) < 1e-6
    # Trabajo integrando la fuerza a lo largo del segmento recto de A a B.
    t = np.linspace(0, 1, 200001)
    pts = A + np.outer(t, B - A)
    F = np.array([-e * E(p) @ (B - A) for p in pts[::20]])
    W = float(np.sum((F[1:] + F[:-1]) / 2) * (t[20] - t[0]))
    assert math.isclose(W, res["W"], rel_tol=1e-6)
