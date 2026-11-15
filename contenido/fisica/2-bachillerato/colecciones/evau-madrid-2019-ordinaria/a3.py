"""Verificación de fis2b-evau-madrid-2019-ord-a3 (dos hilos paralelos al eje z)."""

import numpy as np

mu0, I = 4e-7 * np.pi, 5.0
O, A = np.array([0, 0, 0.0]), np.array([0.02, 0.02, 0])
P, Q = np.array([0, 0.02, 0]), np.array([0.01, 0.01, 0])
k = np.array([0, 0, 1.0])


def campo(p, hilos):
    B = np.zeros(3)
    for c in hilos:
        r = p - c
        d = np.linalg.norm(r)
        B += mu0 * I / (2 * np.pi * d) * np.cross(k, r / d)
    return B


def resolver() -> dict:
    BP = campo(P, [O, A])
    F = I * np.cross(k, campo(A, [O]))           # F/L = I (dl/L × B)
    return {"BPx": BP[0], "BPy": BP[1], "BQ": np.linalg.norm(campo(Q, [O, A])), "FL": np.linalg.norm(F)}


def comprobar(res: dict) -> None:
    F = I * np.cross(k, campo(A, [O]))
    assert F @ (O - A) > 0, "la fuerza sobre A apunta hacia O (atracción)"
    assert np.allclose(F[:2], [-1.25e-4, -1.25e-4], rtol=1e-9)
    assert np.isclose(res["BPx"], -5e-5) and np.isclose(res["BPy"], -5e-5) and res["BQ"] < 1e-18
