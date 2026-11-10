"""Verificación de fis2b-evau-madrid-2024-ord-a1 (Halimede y Neptuno)."""

import math

from scipy.integrate import quad

# Datos del enunciado (SI)
G = 6.67e-11
M_H = 1.60e15
M_N = 1.02e26
r_p, r_a = 12e9, 21e9
E_m = -2.5e20


def resolver() -> dict:
    W = G * M_N * M_H * (1 / r_a - 1 / r_p)
    v = math.sqrt(2 / M_H * (E_m + G * M_N * M_H / r_p))
    return {"W": W, "v": v}


def comprobar(res: dict) -> None:
    # Trabajo como integral de la fuerza radial (hacia dentro) entre r_p y r_a.
    integral, _ = quad(lambda r: -G * M_N * M_H / r**2, r_p, r_a)
    assert math.isclose(integral, res["W"], rel_tol=1e-9)
    # Con la energía del enunciado, la velocidad en el punto más distante es menor.
    ec_lejos = E_m + G * M_N * M_H / r_a
    assert 0 < ec_lejos < 0.5 * M_H * res["v"] ** 2
    # Nota de la solución: la energía que corresponde a esas distancias sería −3,3e20 J y 850 m/s.
    coherente = -G * M_N * M_H / (r_p + r_a)
    assert math.isclose(coherente, -3.3e20, rel_tol=1e-2)
    v_coherente = math.sqrt(2 / M_H * (coherente + G * M_N * M_H / r_p))
    assert math.isclose(v_coherente, 850, rel_tol=1e-2)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["W"], -3.89e20, rel_tol=2e-3) and math.isclose(res["v"], 9.06e2, rel_tol=2e-3)
