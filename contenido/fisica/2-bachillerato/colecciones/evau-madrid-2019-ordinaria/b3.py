"""Verificación de fis2b-evau-madrid-2019-ord-b3 (cargas de −4 y +2 nC)."""

import numpy as np
from scipy.optimize import brentq

K = 9e9
cargas = [(-4e-9, np.array([-0.05, 0])), (2e-9, np.array([0.03, 0]))]


def V(p):
    return sum(K * q / np.linalg.norm(p - c) for q, c in cargas)


def E(p):
    return sum(K * q * (p - c) / np.linalg.norm(p - c) ** 3 for q, c in cargas)


def resolver() -> dict:
    return {"Ex": E(np.zeros(2))[0], "V": V(np.zeros(2)), "x": (1 / 3)}


def comprobar(res: dict) -> None:
    x = brentq(lambda s: V(np.array([s, 0])), -0.0499, 0.0299) * 100
    assert np.isclose(x, res["x"], rtol=1e-9)
    assert abs(E(np.zeros(2))[1]) < 1e-9
    assert np.isclose(res["Ex"], -3.44e4) and np.isclose(res["V"], -120)
