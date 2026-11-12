"""Verificación de fis2b-evau-madrid-2023-ordc-b3 (dos cargas: trabajo y fuerza sobre una tercera)."""

import math

import numpy as np

K = 9e9
cargas = [(-3e-6, np.array([-2.0, 0.0])), (2e-6, np.array([3.0, 0.0]))]
q3, P = 4e-6, np.array([0.0, 4.0])


def potencial(p):
    return sum(K * q / np.linalg.norm(p - r) for q, r in cargas)


def campo(p):
    return sum(K * q * (p - r) / np.linalg.norm(p - r) ** 3 for q, r in cargas)


def resolver() -> dict:
    F = q3 * campo(P)
    return {"W": -q3 * potencial(P), "F_x": F[0], "F_y": F[1]}


def comprobar(res: dict) -> None:
    # Segunda vía para la fuerza: gradiente numérico de la energía potencial, F = −∇(q3·V).
    h = 1e-5
    Fx = -q3 * (potencial(P + [h, 0]) - potencial(P - [h, 0])) / (2 * h)
    Fy = -q3 * (potencial(P + [0, h]) - potencial(P - [0, h])) / (2 * h)
    assert math.isclose(Fx, res["F_x"], rel_tol=1e-6) and math.isclose(Fy, res["F_y"], rel_tol=1e-6)
    # Segunda vía para el trabajo: integral de línea de la fuerza desde muy lejos, por la vertical.
    ys = np.geomspace(4e8, 4.0, 40001)                 # de muy lejos hasta P
    Fy_camino = np.array([q3 * campo(np.array([0.0, y]))[1] for y in ys])
    W = float(np.sum(0.5 * (Fy_camino[1:] + Fy_camino[:-1]) * np.diff(ys)))
    assert math.isclose(W, res["W"], rel_tol=1e-4), W
    # Sentidos: atraída por la negativa (izquierda y abajo) y repelida por la positiva.
    assert res["F_x"] < 0 and res["F_y"] < 0 and res["W"] > 0
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["W"], 9.75e-3, rel_tol=1e-3)
    assert math.isclose(res["F_x"], -4.14e-3, rel_tol=2e-3) and math.isclose(res["F_y"], -2.53e-3, rel_tol=2e-3)
