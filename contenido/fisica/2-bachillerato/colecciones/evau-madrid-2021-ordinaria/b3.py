"""Verificación de fis2b-evau-madrid-2021-ord-b3 (hilo sobre el eje x y electrón)."""

import math

import numpy as np

MU0, e = 4e-7 * math.pi, 1.6e-19
I = 25.0
P = np.array([0.0, 0.05, 0.0])
v = np.array([0.0, 1000.0, 0.0])


def resolver() -> dict:
    d = np.linalg.norm(P[1:])
    B = MU0 * I / (2 * math.pi * d) * np.cross([1.0, 0, 0], P / d)
    F = -e * np.cross(v, B)
    return {"B": B[2], "F": F[0]}


def comprobar(res: dict) -> None:
    # Segunda vía: Biot-Savart numérico a lo largo de un hilo largo.
    x = np.linspace(-500, 500, 1_000_001)
    r = P[None, :] - np.stack([x, np.zeros_like(x), np.zeros_like(x)], axis=1)
    dl = np.array([x[1] - x[0], 0.0, 0.0])
    B = MU0 * I / (4 * math.pi) * np.sum(np.cross(dl, r) / np.linalg.norm(r, axis=1)[:, None] ** 3, axis=0)
    assert math.isclose(B[2], res["B"], rel_tol=1e-4) and abs(B[0]) < 1e-12 and abs(B[1]) < 1e-12
    # La fuerza es perpendicular a la velocidad.
    F = np.array([res["F"], 0, 0])
    assert np.dot(F, v) == 0
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["B"], 1e-4, rel_tol=1e-9) and math.isclose(res["F"], -1.6e-20, rel_tol=1e-9)
