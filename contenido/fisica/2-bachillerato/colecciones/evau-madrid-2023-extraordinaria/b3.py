"""Verificación de fis2b-evau-madrid-2023-ext-b3 (electrón junto a dos hilos paralelos al eje y)."""

import math

import numpy as np

# Datos del enunciado (SI)
MU0 = 4 * math.pi * 1e-7
e = 1.6e-19
j = np.array([0.0, 1.0, 0.0])
I1 = 10.0
x1, x2 = -0.1, 0.1
v = 2e6 * j


def campo(hilos, punto):
    total = np.zeros(3)
    for I, x in hilos:                     # I con signo según +y
        r = punto - np.array([x, 0.0, 0.0])
        r = r - np.dot(r, j) * j
        d = np.linalg.norm(r)
        total += MU0 * I / (2 * math.pi * d) * np.cross(j, r / d)
    return total


def resolver() -> dict:
    I2 = I1 * (0.4 - x2) / (0.4 - x1)
    B = campo([(I1, x1), (-I2, x2)], np.zeros(3))
    F = -e * np.cross(v, B)
    return {"I2": I2, "F": float(F[0])}


def comprobar(res: dict) -> None:
    hilos = [(I1, x1), (-res["I2"], x2)]
    # El campo se anula en toda la recta x = 0,4 m y el electrón no sufre fuerza.
    for y in (-1.0, 0.0, 2.5):
        B = campo(hilos, np.array([0.4, y, 0.0]))
        assert np.allclose(-e * np.cross(v, B), 0, atol=1e-30)
    # Con corrientes paralelas no se anularía.
    assert np.linalg.norm(campo([(I1, x1), (res["I2"], x2)], np.array([0.4, 0.0, 0.0]))) > 1e-6
    # En el origen el campo es −3,2e-5 k y la fuerza solo tiene componente x positiva.
    B0 = campo(hilos, np.zeros(3))
    assert np.allclose(B0, [0, 0, -3.2e-5])
    F = -e * np.cross(v, B0)
    assert abs(F[1]) < 1e-30 and abs(F[2]) < 1e-30 and F[0] > 0
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["I2"], 6.0, rel_tol=1e-12) and math.isclose(res["F"], 1.024e-17, rel_tol=1e-9)
