"""Verificación de fis2b-evau-madrid-2018-ext-b3 (hilos con corrientes opuestas)."""

import numpy as np
from scipy.optimize import brentq

mu0 = 4e-7 * np.pi
P1, P2, I1 = np.array([0, -0.05, 0]), np.array([0, 0.05, 0]), 30.0
k = np.array([0, 0, 1.0])


def campo(p, hilos):
    B = np.zeros(3)
    for c, I in hilos:            # I con signo: + hacia +z
        r = p - c
        d = np.linalg.norm(r)
        B += mu0 * I / (2 * np.pi * d) * np.cross(k, r / d)
    return B


def resolver() -> dict:
    I2 = brentq(lambda I: np.linalg.norm(campo(np.zeros(3), [(P1, I1), (P2, -I)])) - 2.8e-4, 0, 500)
    B = campo(np.array([0, 0.10, 0]), [(P1, I1), (P2, -I2)])
    F = I1 * np.cross(k, campo(P1, [(P2, -I2)]))
    return {"I2": I2, "Bx": B[0], "FL": np.linalg.norm(F)}


def comprobar(res: dict) -> None:
    F = I1 * np.cross(k, campo(P1, [(P2, -res["I2"])]))
    assert F[1] < 0 and abs(F[0]) < 1e-15, "repulsión: el hilo 1 es empujado hacia −y"
    B = campo(np.array([0, 0.10, 0]), [(P1, I1), (P2, -res["I2"])])
    assert abs(B[1]) < 1e-15
    assert np.isclose(res["I2"], 40) and np.isclose(res["FL"], 2.4e-3)
