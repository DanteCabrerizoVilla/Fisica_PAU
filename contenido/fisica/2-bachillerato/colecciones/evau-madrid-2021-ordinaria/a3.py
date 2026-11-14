"""Verificación de fis2b-evau-madrid-2021-ord-a3 (Gauss para una carga puntual)."""

import math

import numpy as np

Q, eps0, r = 2e-6, 8.85e-12, 5e-3


def resolver() -> dict:
    flujo = Q / eps0
    return {"flujo": flujo, "E": flujo / (4 * math.pi * r**2)}


def comprobar(res: dict) -> None:
    # Segunda vía: integrar numéricamente E·dS sobre esferas de radios distintos (no centradas también).
    k = 1 / (4 * math.pi * eps0)
    n = 400
    th = (np.arange(n) + 0.5) * math.pi / n
    ph = (np.arange(2 * n) + 0.5) * math.pi / n
    T, F = np.meshgrid(th, ph, indexing="ij")
    for radio, centro in ((r, np.zeros(3)), (0.02, np.array([0.005, -0.003, 0.002]))):
        normal = np.stack([np.sin(T) * np.cos(F), np.sin(T) * np.sin(F), np.cos(T)], axis=-1)
        pts = centro + radio * normal
        E = k * Q * pts / np.linalg.norm(pts, axis=-1, keepdims=True) ** 3
        dS = radio**2 * np.sin(T) * (math.pi / n) ** 2
        assert math.isclose(float(np.sum(np.sum(E * normal, axis=-1) * dS)), res["flujo"], rel_tol=1e-3)
    # Coincide con la ley de Coulomb.
    assert math.isclose(res["E"], k * Q / r**2, rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["flujo"], 2.26e5, rel_tol=1e-3) and math.isclose(res["E"], 7.20e8, rel_tol=2e-3)
