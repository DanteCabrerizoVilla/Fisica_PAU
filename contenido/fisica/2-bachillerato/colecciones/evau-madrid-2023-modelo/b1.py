"""Verificación de fis2b-evau-madrid-2023-mod-b1 (fuerza de dos masas y trabajo por tres caminos)."""

import math

import numpy as np

G = 6.67e-11
m1, m2, m3 = 10.0, 15.0, 5.0
p1, p2, p3 = np.array([0.0, 0.0]), np.array([2.0, 0.0]), np.array([2.0, 1.0])


def fuerza(m, origen, sobre, donde):
    """Fuerza que la masa m, en `origen`, ejerce sobre la masa `sobre` situada en `donde`."""
    d = origen - donde
    return G * m * sobre * d / np.linalg.norm(d) ** 3


def resolver() -> dict:
    F = fuerza(m1, p1, m3, p3) + fuerza(m2, p2, m3, p3)
    W = -(-G * m1 * m2 / 1.0 - (-G * m1 * m2 / 2.0))
    return {"F_x": F[0], "F_y": F[1], "W": W}


def trabajo(camino, n=20000):
    """Integral de línea de la fuerza de m1 sobre m2 a lo largo de un camino parametrizado en [0, 1]."""
    t = np.linspace(0, 1, n + 1)
    pts = np.array([camino(x) for x in t])
    medios = 0.5 * (pts[1:] + pts[:-1])
    F = np.array([fuerza(m1, p1, m2, p) for p in medios])
    return float(np.sum(F * (pts[1:] - pts[:-1])))


def comprobar(res: dict) -> None:
    ini, fin = np.array([2.0, 0.0]), np.array([0.0, 1.0])
    recto = lambda t: ini + t * (fin - ini)
    # Dos caminos curvos (Bézier) que no pasan por el origen.
    curva_b = lambda t: (1 - t) ** 2 * ini + 2 * t * (1 - t) * np.array([1.4, 1.4]) + t**2 * fin
    curva_c = lambda t: ((1 - t) ** 3 * ini + 3 * t * (1 - t) ** 2 * np.array([2.3, 1.8])
                         + 3 * t**2 * (1 - t) * np.array([1.0, 1.7]) + t**3 * fin)
    for camino in (recto, curva_b, curva_c):
        assert math.isclose(trabajo(camino), res["W"], rel_tol=1e-5), "el trabajo no debe depender del camino"
    # Segunda vía para la fuerza: campo total en el punto por la masa.
    g = (G * m1 * (p1 - p3) / 5**1.5) + (G * m2 * (p2 - p3) / 1.0)
    assert math.isclose(m3 * g[0], res["F_x"], rel_tol=1e-12)
    assert math.isclose(m3 * g[1], res["F_y"], rel_tol=1e-12)
    # Valores de la solución orientativa oficial (su F_y = −5,33e-9 es el módulo, no la componente).
    assert math.isclose(res["F_x"], -5.97e-10, rel_tol=2e-3)
    assert math.isclose(math.hypot(res["F_x"], res["F_y"]), 5.33e-9, rel_tol=2e-3)
    assert math.isclose(res["W"], 5.00e-9, rel_tol=1e-3)
