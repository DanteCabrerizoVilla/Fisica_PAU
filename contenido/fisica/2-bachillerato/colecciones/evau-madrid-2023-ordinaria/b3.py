"""Verificación de fis2b-evau-madrid-2023-ord-b3 (ion He+ en campo eléctrico y magnético)."""

import math

import numpy as np

# Datos del enunciado
E = np.array([1e3, 0.0, 0.0])     # V/m
B = np.array([0.0, 0.6, 0.0])     # T
t = 20e-6                         # s
q = 1.6e-19                       # C
m = 4e-3 / 6.02e23                # kg


def resolver() -> dict:
    a = q * E / m
    v = a * t
    F = q * E + q * np.cross(v, B)
    return {"a": a[0], "F_x": F[0], "F_z": F[2]}


def comprobar(res: dict) -> None:
    # Segunda vía: integrar el movimiento paso a paso con solo el campo eléctrico
    # y aplicar la fuerza de Lorentz con la velocidad alcanzada.
    pasos = 20000
    dt = t / pasos
    v = np.zeros(3)
    for _ in range(pasos):
        v = v + q * E / m * dt
    F = q * (E + np.cross(v, B))
    assert math.isclose(F[0], res["F_x"], rel_tol=1e-9)
    assert math.isclose(F[2], res["F_z"], rel_tol=1e-6)
    assert F[1] == 0, "no hay componente y"
    # Tercera vía para la velocidad: teorema del trabajo y la energía, q·E·d = ½ m v².
    d = 0.5 * res["a"] * t**2
    assert math.isclose(math.sqrt(2 * q * E[0] * d / m), np.linalg.norm(v), rel_tol=1e-6)
    # La magnética es perpendicular a la velocidad y al campo.
    Fm = q * np.cross(v, B)
    assert abs(np.dot(Fm, v)) < 1e-30 and abs(np.dot(Fm, B)) < 1e-30
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["a"], 2.41e10, rel_tol=3e-3)
    assert math.isclose(res["F_z"], 4.63e-14, rel_tol=3e-3)
