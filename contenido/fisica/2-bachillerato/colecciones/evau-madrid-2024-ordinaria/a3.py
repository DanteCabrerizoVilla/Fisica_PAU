"""Verificación de fis2b-evau-madrid-2024-ord-a3 (dos hilos que se repelen)."""

import math

import numpy as np

# Datos del enunciado (SI)
MU0 = 4 * math.pi * 1e-7
d = 0.05
F_L = 5e-5
x_nulo = 0.10
k = np.array([0.0, 0.0, 1.0])


def resolver() -> dict:
    razon = x_nulo / (x_nulo - d)              # I1/I2 por el punto de campo nulo
    I2 = math.sqrt(2 * math.pi * d * F_L / (MU0 * razon))
    I1 = razon * I2
    B = MU0 / (2 * math.pi) * abs(I1 / 0.05 - I2 / 0.10)
    return {"I1": I1, "I2": I2, "B": B}


def comprobar(res: dict) -> None:
    hilos = [(res["I1"], np.zeros(3)), (-res["I2"], np.array([d, 0.0, 0.0]))]     # antiparalelas

    def campo(punto):
        total = np.zeros(3)
        for I, pos in hilos:
            r = punto - pos
            dist = np.linalg.norm(r)
            total += MU0 * I / (2 * math.pi * dist) * np.cross(k, r / dist)
        return total

    assert np.allclose(campo(np.array([x_nulo, 0.0, 0.0])), 0, atol=1e-18), "el campo no se anula en x = 10 cm"
    assert math.isclose(np.linalg.norm(campo(np.array([-0.05, 0.0, 0.0]))), res["B"], rel_tol=1e-12)
    # Fuerza sobre el hilo 2: I2·(u × B1), repulsiva y del módulo dado.
    B1_en_2 = MU0 * res["I1"] / (2 * math.pi * d) * np.cross(k, np.array([1.0, 0.0, 0.0]))
    f = -res["I2"] * np.cross(k, B1_en_2)
    assert math.isclose(np.linalg.norm(f), F_L, rel_tol=1e-12) and f[0] > 0, "debe alejar al hilo 2 del 1"
    # Con corrientes paralelas el campo no se anularía en x = 10 cm.
    assert abs(MU0 / (2 * math.pi) * (res["I1"] / 0.10 + res["I2"] / 0.05)) > 1e-6
    assert (round(res["I1"], 6), round(res["I2"], 6)) == (5.0, 2.5) and math.isclose(res["B"], 1.5e-5, rel_tol=1e-9)
