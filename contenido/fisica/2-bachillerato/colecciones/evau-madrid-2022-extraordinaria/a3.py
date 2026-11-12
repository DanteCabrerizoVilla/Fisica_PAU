"""Verificación de fis2b-evau-madrid-2022-ext-a3 (dos cargas: campo y potencial nulo)."""

import math

import numpy as np
from scipy.optimize import brentq

K = 9e9
cargas = [(2e-9, np.array([1.0, 0.0])), (-4e-9, np.array([3.0, 0.0]))]
A = np.array([2.0, 1.0])


def potencial(p):
    return sum(K * q / np.linalg.norm(np.asarray(p, float) - r) for q, r in cargas)


def resolver() -> dict:
    E = sum(K * q * (A - r) / np.linalg.norm(A - r) ** 3 for q, r in cargas)
    # 2/(1 − x) = 4/(3 − x)
    return {"E_x": E[0], "E_y": E[1], "x": (2 * 3 - 4 * 1) / (2 - 4)}


def comprobar(res: dict) -> None:
    # Segunda vía para el campo: menos el gradiente numérico del potencial.
    h = 1e-6
    Ex = -(potencial(A + [h, 0]) - potencial(A - [h, 0])) / (2 * h)
    Ey = -(potencial(A + [0, h]) - potencial(A - [0, h])) / (2 * h)
    assert math.isclose(Ex, res["E_x"], rel_tol=1e-6) and math.isclose(Ey, res["E_y"], rel_tol=1e-6)
    # Segunda vía para el punto: buscar numéricamente el cero del potencial en x < 1.
    raiz = brentq(lambda x: potencial([x, 0.0]), -50, 0.999)
    assert math.isclose(raiz, res["x"], abs_tol=1e-9)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["E_x"], 19.09, rel_tol=1e-3) and math.isclose(res["E_y"], -6.36, rel_tol=1e-3)
    assert math.isclose(res["x"], -1)
