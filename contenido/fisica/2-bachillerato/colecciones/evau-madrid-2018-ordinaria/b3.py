"""Verificación de fis2b-evau-madrid-2018-ord-b3 (cargas de 6 y 10 μC)."""

import math
from scipy.integrate import quad
from scipy.optimize import brentq

K, q1, q2, d = 9e9, 6e-6, 10e-6, 10.0


def resolver() -> dict:
    return {"W": q2 * K * q1 / d, "x": d / (1 + math.sqrt(q2 / q1))}


def comprobar(res: dict) -> None:
    # Trabajo externo = −(trabajo del campo) desde el infinito: integral de la repulsión.
    W = quad(lambda r: K * q1 * q2 / r**2, d, math.inf)[0]
    assert math.isclose(W, res["W"], rel_tol=1e-9)
    E = lambda x: K * q1 / x**2 - K * q2 / (d - x) ** 2
    assert math.isclose(brentq(E, 0.1, 9.9), res["x"], rel_tol=1e-10)
