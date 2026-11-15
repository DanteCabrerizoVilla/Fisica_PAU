"""Verificación de fis2b-evau-madrid-2018-ext-a3 (dos cargas iguales en la diagonal)."""

import numpy as np

K, E0, qp = 9e9, 5e3, 2e-6
pos = [np.array([2.0, 2]), np.array([-2.0, -2])]


def campo(p, q):
    return sum(K * q * (p - c) / np.linalg.norm(p - c) ** 3 for c in pos)


def potencial(p, q):
    return sum(K * q / np.linalg.norm(p - c) for c in pos)


def resolver() -> dict:
    q = 9 * E0 / (4 * K)
    return {"q": q, "Ex": campo(np.array([-1.0, -1]), q)[0], "W": qp * potencial(np.array([-1.0, -1]), q)}


def comprobar(res: dict) -> None:
    q = res["q"]
    assert np.isclose(np.linalg.norm(campo(np.array([1.0, 1]), q)), E0, rtol=1e-12)
    E = campo(np.array([-1.0, -1]), q)
    assert np.isclose(E[0], E[1]) and E[0] > 0
