"""Verificación de fis2b-pau-madrid-2026-ord-4a (constante de Planck con dos potenciales de frenado)."""

import math

import numpy as np

# Datos del enunciado (SI)
c = 3e8
e = 1.6e-19
lambda_1, V_1 = 150e-9, 3.55
lambda_2, V_2 = 200e-9, 1.48


def resolver() -> dict:
    h = e * (V_1 - V_2) / (c * (1 / lambda_1 - 1 / lambda_2))
    W = h * c / lambda_1 - e * V_1
    return {"h": h, "W": W / e}


def comprobar(res: dict) -> None:
    # Segunda vía: resolver el sistema lineal de dos ecuaciones (incógnitas h y W).
    matriz = np.array([[c / lambda_1, -1.0], [c / lambda_2, -1.0]])
    h, W = np.linalg.solve(matriz, np.array([e * V_1, e * V_2]))
    assert math.isclose(h, res["h"], rel_tol=1e-9) and math.isclose(W / e, res["W"], rel_tol=1e-9)
    # El trabajo de extracción sale igual con la segunda luz.
    assert math.isclose(res["h"] * c / lambda_2 / e - V_2, res["W"], rel_tol=1e-9)
    # h cerca del valor aceptado y W cerca del de la plata.
    assert math.isclose(res["h"], 6.63e-34, rel_tol=5e-3)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["h"], 6.62e-34, rel_tol=2e-3) and math.isclose(res["W"], 4.73, rel_tol=2e-3)
