"""Verificación de fis2b-evau-madrid-2023-mod-b3 (dos hilos paralelos al eje x y electrón)."""

import math

import numpy as np

MU0 = 4e-7 * math.pi
e = 1.6e-19
I1 = 3.0
y1, y2 = 0.0, -2.0                      # posición de cada hilo en el eje y
P = np.array([0.0, -0.5, 0.0])
Q = np.array([0.0, 2.0, 0.0])
v = np.array([5e6, 0.0, 0.0])


def campo(I, y_hilo, punto):
    """Campo de un hilo paralelo al eje x (corriente hacia +x) que pasa por (0, y_hilo, 0)."""
    r = np.array([0.0, punto[1] - y_hilo, punto[2]])
    d = np.linalg.norm(r)
    return MU0 * I / (2 * math.pi * d) * np.cross([1.0, 0.0, 0.0], r / d)


def resolver() -> dict:
    I2 = I1 * abs(P[1] - y2) / abs(P[1] - y1)
    B = campo(I1, y1, Q) + campo(I2, y2, Q)
    F = -e * np.cross(v, B)
    return {"I2": I2, "B": B[2], "F": F[1]}


def biot_savart(I, y_hilo, punto, L=4000.0, n=400001):
    """Segunda vía: integrar la ley de Biot-Savart sobre un hilo muy largo."""
    x = np.linspace(-L, L, n)
    dl = np.array([x[1] - x[0], 0.0, 0.0])
    r = punto - np.stack([x, np.full(n, y_hilo), np.zeros(n)], axis=1)
    dist = np.linalg.norm(r, axis=1)
    return MU0 * I / (4 * math.pi) * np.sum(np.cross(dl, r) / dist[:, None] ** 3, axis=0)


def comprobar(res: dict) -> None:
    I2 = res["I2"]
    # El campo total se anula en P.
    BP = campo(I1, y1, P) + campo(I2, y2, P)
    assert np.linalg.norm(BP) < 1e-18
    # Biot-Savart numérico en Q.
    BQ = biot_savart(I1, y1, Q) + biot_savart(I2, y2, Q)
    assert math.isclose(BQ[2], res["B"], rel_tol=1e-4) and abs(BQ[0]) < 1e-12 and abs(BQ[1]) < 1e-12
    # La fuerza es perpendicular a la velocidad y al campo, y nula si v es paralela a B.
    B = np.array([0.0, 0.0, res["B"]])
    F = -e * np.cross(v, B)
    assert abs(np.dot(F, v)) < 1e-30 and F[1] > 0
    assert np.linalg.norm(np.cross(np.array([0.0, 0.0, 1e6]), B)) == 0
    # Valores de la solución orientativa oficial.
    assert math.isclose(I2, 9) and math.isclose(res["B"], 7.5e-7, rel_tol=1e-9)
    assert math.isclose(res["F"], 6e-19, rel_tol=1e-9)
