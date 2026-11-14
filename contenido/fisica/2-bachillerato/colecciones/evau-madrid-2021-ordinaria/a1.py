"""Verificación de fis2b-evau-madrid-2021-ord-a1 (masa puntual: potencial, campo y trabajo)."""

import math

import numpy as np

G, M, m = 6.67e-11, 0.05, 0.02
P = np.array([8.0, 0.0])
A, O = np.array([0.0, 6.0]), np.array([0.0, 0.0])


def V(p):
    return -G * M / np.linalg.norm(p - P)


def resolver() -> dict:
    d = P - A
    g = G * M * d / np.linalg.norm(d) ** 3
    return {"V": V(A), "g_x": g[0], "g_y": g[1], "W": m * (V(A) - V(O))}


def comprobar(res: dict) -> None:
    # Segunda vía para el campo: menos el gradiente numérico del potencial.
    h = 1e-6
    gx = -(V(A + [h, 0]) - V(A - [h, 0])) / (2 * h)
    gy = -(V(A + [0, h]) - V(A - [0, h])) / (2 * h)
    assert math.isclose(gx, res["g_x"], rel_tol=1e-6) and math.isclose(gy, res["g_y"], rel_tol=1e-6)
    # Segunda vía para el trabajo: integral de línea de la fuerza por el eje y.
    ys = np.linspace(6, 0, 200001)
    medios = 0.5 * (ys[1:] + ys[:-1])
    d = P[None, :] - np.stack([np.zeros_like(medios), medios], axis=1)
    Fy = G * M * m * d[:, 1] / np.linalg.norm(d, axis=1) ** 3
    assert math.isclose(float(np.sum(Fy * np.diff(ys))), res["W"], rel_tol=1e-6)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["V"], -3.33e-13, rel_tol=3e-3)
    assert math.isclose(res["g_x"], 2.67e-14, rel_tol=2e-3) and math.isclose(res["g_y"], -2.00e-14, rel_tol=2e-3)
    assert math.isclose(res["W"], 1.67e-15, rel_tol=3e-3)
