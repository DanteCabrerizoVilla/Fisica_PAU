"""Verificación de fis2b-evau-madrid-2020-ext-a3 (dipolo: potencial y campo en la mediatriz)."""

import math

import numpy as np

K = 9e9
cargas = [(5e-9, np.array([-0.04, 0.0])), (-5e-9, np.array([0.04, 0.0]))]


def V(p):
    return sum(K * q / np.linalg.norm(p - r) for q, r in cargas)


def E(p):
    return sum(K * q * (p - r) / np.linalg.norm(p - r) ** 3 for q, r in cargas)


def resolver() -> dict:
    O, P = np.zeros(2), np.array([0.0, 0.03])
    return {"V0": round(V(O), 9), "E0": E(O)[0], "V3": round(V(P), 9), "E3": E(P)[0]}


def comprobar(res: dict) -> None:
    for p in (np.zeros(2), np.array([0.0, 0.03])):
        assert abs(E(p)[1]) < 1e-9 and abs(V(p)) < 1e-9
    assert math.isclose(res["E0"], 5.62e4, rel_tol=2e-3) and math.isclose(res["E3"], 2.88e4, rel_tol=1e-9)
