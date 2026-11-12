"""Verificación de fis2b-evau-madrid-2022-mod-a3 (dos hilos con corrientes opuestas)."""

import math

import numpy as np

MU0 = 4e-7 * math.pi
I, a = 2.0, 0.20
hilos = [(-I, np.array([0.0, a, 0.0])), (+I, np.array([2 * a, 0.0, 0.0]))]   # corriente con signo según z
Z = np.array([0.0, 0.0, 1.0])


def campo(corriente, pos, punto):
    r = punto - pos
    d = np.linalg.norm(r)
    return MU0 * corriente / (2 * math.pi * d) * np.cross(Z, r / d)


def resolver() -> dict:
    O = np.zeros(3)
    B = campo(*hilos[0], O) + campo(*hilos[1], O)
    # Fuerza por unidad de longitud sobre el hilo 2: I2 (ẑ × B1), con B1 el campo del hilo 1 donde está el 2.
    F = hilos[1][0] * np.cross(Z, campo(*hilos[0], hilos[1][1]))
    return {"B_x": B[0], "B_y": B[1], "F_x": F[0], "F_y": F[1], "modulo": float(np.linalg.norm(F))}


def comprobar(res: dict) -> None:
    # Segunda vía para la fuerza: fórmula de los hilos paralelos y repulsión a lo largo de la línea que los une.
    d = hilos[1][1] - hilos[0][1]
    dist = np.linalg.norm(d)
    modulo = MU0 * I * I / (2 * math.pi * dist)
    assert math.isclose(modulo, res["modulo"], rel_tol=1e-12)
    F = modulo * d / dist                       # se repelen: sobre el 2, alejándose del 1
    assert math.isclose(F[0], res["F_x"], rel_tol=1e-12) and math.isclose(F[1], res["F_y"], rel_tol=1e-12)
    # Tercera ley de Newton: la fuerza sobre el hilo 1 es la opuesta.
    F21 = hilos[0][0] * np.cross(Z, campo(*hilos[1], hilos[0][1]))
    assert np.allclose(F21[:2], -F[:2], rtol=1e-12)
    # Cada campo es perpendicular a la línea hilo-punto.
    for corriente, pos in hilos:
        assert abs(np.dot(campo(corriente, pos, np.zeros(3)), pos)) < 1e-20
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["B_x"], -2e-6, rel_tol=1e-9) and math.isclose(res["B_y"], -1e-6, rel_tol=1e-9)
    assert math.isclose(res["F_x"], 1.6e-6, rel_tol=1e-9) and math.isclose(res["F_y"], -8e-7, rel_tol=1e-9)
