"""Verificación de fis2b-pau-madrid-2025-mod-1 (masa de un planeta con un muelle)."""

import math

import numpy as np

# Datos del enunciado
G = 6.67e-11
g_T = 10.0
R = 3.5e3 * 1e3
MASAS = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0])          # kg
X_TIERRA = np.array([5, 10, 15, 20, 25, 30]) * 1e-2       # m, figura 1
X_PLANETA = np.array([1.5, 3, 4.5, 6, 7.5, 9]) * 1e-2     # m, figura 2


def resolver() -> dict:
    k = 2.0 * g_T / 0.20
    g = k * 0.06 / 2.0
    return {"k": k, "g": g, "masa": g * R**2 / G}


def comprobar(res: dict) -> None:
    # Segunda vía: pendiente de cada recta por mínimos cuadrados con todos los puntos.
    pend_T = np.polyfit(MASAS, X_TIERRA, 1)[0]
    pend_P = np.polyfit(MASAS, X_PLANETA, 1)[0]
    assert math.isclose(g_T / pend_T, res["k"], rel_tol=1e-9)
    assert math.isclose(res["k"] * pend_P, res["g"], rel_tol=1e-9)
    # La gravedad es 6/20 de la terrestre, sin pasar por k.
    assert math.isclose(res["g"], g_T * pend_P / pend_T, rel_tol=1e-9)
    # Con la masa hallada se recupera la gravedad.
    assert math.isclose(G * res["masa"] / R**2, res["g"], rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["masa"], 5.51e23, rel_tol=2e-3)
