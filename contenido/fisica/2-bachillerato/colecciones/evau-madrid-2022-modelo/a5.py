"""Verificación de fis2b-evau-madrid-2022-mod-a5 (constante de Planck con dos potenciales de frenado)."""

import math

import numpy as np

c, e = 3e8, 1.6e-19
f1, V1 = c / 120e-9, 7.2
f2, V2 = 1.67e15, 3.8


def resolver() -> dict:
    h = e * (V1 - V2) / (f1 - f2)
    W = h * f1 - e * V1
    return {"h": h, "W": W / e, "f0": W / h}


def comprobar(res: dict) -> None:
    # Segunda vía: resolver el sistema lineal en h y W0.
    h, W = np.linalg.solve(np.array([[f1, -1.0], [f2, -1.0]]), np.array([e * V1, e * V2]))
    assert math.isclose(h, res["h"], rel_tol=1e-9) and math.isclose(W / e, res["W"], rel_tol=1e-9)
    # La segunda ecuación da el mismo trabajo de extracción.
    assert math.isclose(res["h"] * f2 - e * V2, res["W"] * e, rel_tol=1e-9)
    # Tercera vía: la recta V_f(f) corta el eje en la frecuencia umbral.
    pendiente = (V1 - V2) / (f1 - f2)
    assert math.isclose(f1 - V1 / pendiente, res["f0"], rel_tol=1e-9)
    assert res["f0"] < f2 < f1
    # Valores de la solución orientativa oficial (3,03 eV por truncar h) y valor aceptado de h.
    assert math.isclose(res["h"], 6.55e-34, rel_tol=1e-3) and math.isclose(res["h"], 6.626e-34, rel_tol=0.015)
    assert math.isclose(res["W"], 3.03, abs_tol=0.015) and math.isclose(res["f0"], 7.42e14, rel_tol=1e-3)
