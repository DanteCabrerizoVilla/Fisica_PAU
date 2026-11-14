"""Verificación de fis2b-evau-madrid-2021-ext-a3 (tres hilos)."""

import math

import numpy as np

MU0 = 4e-7 * math.pi
hilos = [  # (intensidad, dirección, punto por el que pasa)
    (2.0, np.array([1.0, 0, 0]), np.array([0.0, 0, 0])),
    (2.0, np.array([1.0, 0, 0]), np.array([0.0, 0, 4])),
    (3.0, np.array([0.0, 1, 0]), np.array([0.0, 0, 0])),
]
P = np.array([0.0, 0, 2])


def campo(I, u, p0, punto):
    r = punto - p0
    r = r - np.dot(r, u) * u                       # parte perpendicular al hilo
    d = np.linalg.norm(r)
    return MU0 * I / (2 * math.pi * d) * np.cross(u, r / d)


def resolver() -> dict:
    B = sum(campo(*h, P) for h in hilos)
    F = hilos[1][0] * np.cross(hilos[1][1], campo(*hilos[0], hilos[1][2]))
    return {"B": B[0], "F": F[2]}


def biot_savart(I, u, p0, punto, L=2000.0, n=400001):
    s = np.linspace(-L, L, n)
    pts = p0[None, :] + s[:, None] * u[None, :]
    r = punto[None, :] - pts
    dl = u * (s[1] - s[0])
    return MU0 * I / (4 * math.pi) * np.sum(np.cross(dl, r) / np.linalg.norm(r, axis=1)[:, None] ** 3, axis=0)


def comprobar(res: dict) -> None:
    # Segunda vía: Biot-Savart numérico para cada hilo.
    B = sum(biot_savart(*h, P) for h in hilos)
    assert math.isclose(B[0], res["B"], rel_tol=1e-4) and abs(B[1]) < 1e-12 and abs(B[2]) < 1e-12
    # Fuerza entre hilos paralelos: μ0 I1 I2 / (2π d), hacia el otro hilo (atractiva).
    assert math.isclose(res["F"], -MU0 * 2 * 2 / (2 * math.pi * 4), rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["B"], 3e-7, rel_tol=1e-9) and math.isclose(res["F"], -2e-7, rel_tol=1e-9)
