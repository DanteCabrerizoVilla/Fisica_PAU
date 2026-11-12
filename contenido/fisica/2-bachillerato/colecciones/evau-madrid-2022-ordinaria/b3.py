"""Verificación de fis2b-evau-madrid-2022-ord-b3 (dos cargas positivas, campo nulo en el origen)."""

import math

import numpy as np
from scipy.optimize import fsolve

K = 9e9
A = np.array([3.0, 4.0])
V0 = 1.08e4


def resolver() -> dict:
    B = -2 * A
    q1 = V0 / (K * (1 / np.linalg.norm(A) + 4 / np.linalg.norm(B)))
    return {"x2": B[0], "y2": B[1], "q1": q1, "q2": 4 * q1}


def campo_origen(q1, B):
    E = np.zeros(2)
    for q, r in ((q1, A), (4 * q1, np.asarray(B, float))):
        E += K * q * (-r) / np.linalg.norm(r) ** 3
    return E


def comprobar(res: dict) -> None:
    B = np.array([res["x2"], res["y2"]])
    # El campo se anula en el origen.
    assert np.linalg.norm(campo_origen(res["q1"], B)) < 1e-9
    # Segunda vía: buscar numéricamente la posición que anula el campo, desde varios puntos de partida.
    for inicio in ([-3.0, -2.0], [-10.0, -1.0], [-1.0, -12.0]):
        sol = fsolve(lambda p: campo_origen(1e-6, p) * 1e-3, inicio)
        assert np.allclose(sol, B, atol=1e-6)
    # En (6, 8), del mismo lado, los campos se suman.
    assert np.linalg.norm(campo_origen(res["q1"], [6.0, 8.0])) > 1
    # Potencial en el origen.
    V = K * res["q1"] / 5 + K * res["q2"] / 10
    assert math.isclose(V, V0, rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["q1"], 2e-6, rel_tol=1e-9) and math.isclose(res["q2"], 8e-6, rel_tol=1e-9)
