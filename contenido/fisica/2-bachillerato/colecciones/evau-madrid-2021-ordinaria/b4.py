"""Verificación de fis2b-evau-madrid-2021-ord-b4 (láser: reflexión y refracción)."""

import math

import numpy as np

c, lam0, n = 3e8, 488e-9, 1.55


def resolver() -> dict:
    i = math.radians(30)
    t = math.asin(math.sin(i) / n)
    return {"f": c / lam0, "l_aire": lam0, "l_medio": lam0 / n, "angulo": 180 - 30 - math.degrees(t)}


def comprobar(res: dict) -> None:
    # Segunda vía: con vectores. Superficie horizontal, normal (0, 1).
    i = math.radians(30)
    d = np.array([math.sin(i), -math.cos(i)])               # rayo incidente
    reflejado = d - 2 * np.dot(d, [0, 1]) * np.array([0.0, 1.0])
    assert math.isclose(math.degrees(math.acos(np.dot(-d, reflejado))), 60, abs_tol=1e-9)
    cos_i = -d[1]
    k = 1 - (1 / n) ** 2 * (1 - cos_i**2)
    refractado = (1 / n) * d + ((1 / n) * cos_i - math.sqrt(k)) * np.array([0.0, 1.0])
    angulo = math.degrees(math.acos(np.dot(reflejado, refractado)))
    assert math.isclose(angulo, res["angulo"], abs_tol=1e-9)
    # Del aire al material, k nunca es negativo: no hay reflexión total.
    assert all(1 - (1 / n) ** 2 * math.sin(math.radians(a)) ** 2 > 0 for a in range(0, 90))
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["f"], 6.15e14, rel_tol=1e-3) and math.isclose(res["l_medio"], 3.15e-7, rel_tol=1e-3)
    assert math.isclose(res["angulo"], 131.18, abs_tol=0.01)
