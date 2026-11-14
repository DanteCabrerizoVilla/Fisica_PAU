"""Verificación de fis2b-evau-madrid-2021-ext-b1 (masa a partir de g_x y trabajo)."""

import math

import numpy as np

G, gx, M = 6.67e-11, -1.18e-11, 5.0


def resolver() -> dict:
    rB = math.sqrt(8)
    m = -gx * rB**2 / (G * math.cos(math.pi / 4))
    return {"m": m, "W": G * m * M * (1 / rB - 1 / 4)}


def comprobar(res: dict) -> None:
    m = res["m"]
    B = np.array([2.0, 2.0])
    g = -G * m * B / np.linalg.norm(B) ** 3
    assert math.isclose(g[0], gx, rel_tol=1e-12)
    # Segunda vía: integral de línea de la fuerza por el segmento recto de A a B.
    A = np.array([4.0, 0.0])
    t = np.linspace(0, 1, 200001)
    pts = A + np.outer(0.5 * (t[1:] + t[:-1]), B - A)
    F = -G * m * M * pts / np.linalg.norm(pts, axis=1)[:, None] ** 3
    assert math.isclose(float(np.sum(F @ (B - A)) / 200000), res["W"], rel_tol=1e-6)
    # Valores de la solución orientativa oficial.
    assert math.isclose(m, 2.0, rel_tol=1e-3) and math.isclose(res["W"], 6.91e-11, rel_tol=1e-3)
