"""Verificación de fis2b-evau-madrid-2022-ext-b1 (masa a partir del trabajo gravitatorio)."""

import math

import numpy as np

G = 6.67e-11
mA, pA = 2.0, np.array([1.0, 0.0])
ini, fin = np.array([0.0, 0.0]), np.array([0.0, 2.0])
W = -2.95e-10


def resolver() -> dict:
    r1, r2 = np.linalg.norm(ini - pA), np.linalg.norm(fin - pA)
    mB = W / (G * mA * (1 / r2 - 1 / r1))
    g = G * mA * (pA - fin) / r2**3
    return {"mB": mB, "g_x": g[0], "g_y": g[1]}


def comprobar(res: dict) -> None:
    # Segunda vía: integral de línea de la fuerza sobre B a lo largo del eje y.
    n = 200000
    ys = np.linspace(0, 2, n + 1)
    medios = 0.5 * (ys[1:] + ys[:-1])
    d = pA[None, :] - np.stack([np.zeros(n), medios], axis=1)
    Fy = G * mA * res["mB"] * d[:, 1] / np.linalg.norm(d, axis=1) ** 3
    assert math.isclose(float(np.sum(Fy) * (2 / n)), W, rel_tol=1e-6)
    # El campo apunta hacia la masa A.
    assert res["g_x"] > 0 and res["g_y"] < 0
    assert math.isclose(math.hypot(res["g_x"], res["g_y"]), G * mA / 5, rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["mB"], 4.0, rel_tol=1e-3)
    assert math.isclose(res["g_x"], 1.19e-11, rel_tol=3e-3) and math.isclose(res["g_y"], -2.39e-11, rel_tol=3e-3)
