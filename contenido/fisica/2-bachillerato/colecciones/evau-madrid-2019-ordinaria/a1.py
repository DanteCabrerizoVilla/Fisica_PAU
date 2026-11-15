"""Verificación de fis2b-evau-madrid-2019-ord-a1 (masa en (4, 3) m)."""

import math
import numpy as np

G, m1, m2 = 6.67e-11, 5.0, 0.5
p1 = np.array([4.0, 3.0])


def campo(p, masas):
    return sum(G * m * (c - p) / np.linalg.norm(c - p) ** 3 for m, c in masas)


def resolver() -> dict:
    g = campo(np.zeros(2), [(m1, p1)])
    d1 = np.linalg.norm(p1)
    return {"gx": g[0], "gy": g[1], "W": G * m1 * m2 / d1, "d": d1 / (1 + math.sqrt(m1 / m2))}


def comprobar(res: dict) -> None:
    masas = [(m1, p1), (m2, np.zeros(2))]
    punto = res["d"] * p1 / np.linalg.norm(p1)
    assert np.linalg.norm(campo(punto, masas)) < 1e-12 * G
    # Trabajo como integral de la fuerza desde el infinito hasta el origen, por la recta que une m1 y el origen.
    from scipy.integrate import quad
    u = -p1 / np.linalg.norm(p1)                       # del origen hacia fuera, alejándose de m1
    f = lambda s: m2 * campo(s * u, [(m1, p1)]) @ (-u)  # componente de la fuerza en el sentido del movimiento
    W = quad(f, 0, 10, epsabs=0, epsrel=1e-12)[0] + quad(f, 10, np.inf, epsabs=0, epsrel=1e-12)[0]
    assert math.isclose(W, res["W"], rel_tol=1e-8)
