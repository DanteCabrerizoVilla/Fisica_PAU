"""Verificación de fis2b-pau-madrid-2025-ext-4b (campo magnético de dos hilos paralelos)."""

import math

import numpy as np

# Datos del enunciado (SI)
MU0 = 4 * math.pi * 1e-7
I1 = 5.0
hilo1 = np.array([0.0, 0.06, 0.0])
hilo2 = np.array([0.06, 0.0, 0.0])
P = np.array([0.04, 0.02, 0.0])
k = np.array([0.0, 0.0, 1.0])


def campo_hilo(intensidad: float, hilo, punto):
    """Campo de un hilo infinito paralelo a z; intensidad positiva = sentido +z."""
    r = punto - hilo
    d = np.linalg.norm(r)
    return MU0 * intensidad / (2 * math.pi * d) * np.cross(k, r / d)


def resolver() -> dict:
    B1 = campo_hilo(I1, hilo1, P)
    I2 = I1 * np.linalg.norm(P - hilo2) / np.linalg.norm(P - hilo1)
    return {"B_x": float(B1[0]), "B_y": float(B1[1]), "I2": float(I2)}


def comprobar(res: dict) -> None:
    # Con I2 en el sentido +z el campo total en P se anula; en sentido −z, se duplica.
    total = campo_hilo(I1, hilo1, P) + campo_hilo(res["I2"], hilo2, P)
    assert np.allclose(total, 0, atol=1e-18), f"el campo total no es nulo: {total}"
    opuesto = campo_hilo(I1, hilo1, P) + campo_hilo(-res["I2"], hilo2, P)
    assert math.isclose(np.linalg.norm(opuesto), 2 * math.hypot(res["B_x"], res["B_y"]), rel_tol=1e-9)
    # Segunda vía: ley de Biot-Savart integrada numéricamente sobre un hilo muy largo.
    z = np.linspace(-50, 50, 2_000_001)
    dz = z[1] - z[0]
    r = P - hilo1
    d2 = r[0] ** 2 + r[1] ** 2 + z**2
    factor = MU0 * I1 / (4 * math.pi) * np.sum(dz / d2**1.5)      # dl × r = dz (k × r)
    B = factor * np.cross(k, r)
    assert math.isclose(B[0], res["B_x"], rel_tol=1e-3) and math.isclose(B[1], res["B_y"], rel_tol=1e-3)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["B_x"], 1.25e-5, rel_tol=1e-3) and math.isclose(res["I2"], 2.5, rel_tol=1e-9)
