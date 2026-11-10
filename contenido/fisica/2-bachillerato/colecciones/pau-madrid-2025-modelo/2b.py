"""Verificación de fis2b-pau-madrid-2025-mod-2b (dos hilos paralelos al eje x)."""

import math

import numpy as np

# Datos del enunciado (SI)
MU0 = 4 * math.pi * 1e-7
i = np.array([1.0, 0.0, 0.0])
HILOS = [(5.0, np.array([0.0, 0.0, 0.02])), (-3.0, np.array([0.0, 0.02, 0.0]))]   # intensidad con signo según +x


def campo_hilo(intensidad, hilo, punto):
    r = punto - hilo
    r = r - np.dot(r, i) * i              # componente perpendicular al hilo
    d = np.linalg.norm(r)
    return MU0 * intensidad / (2 * math.pi * d) * np.cross(i, r / d)


def resolver() -> dict:
    B = sum(campo_hilo(I, h, np.zeros(3)) for I, h in HILOS)
    D = np.linalg.norm(HILOS[0][1] - HILOS[1][1])
    fuerza = MU0 * abs(HILOS[0][0] * HILOS[1][0]) / (2 * math.pi * D)
    return {"B_y": float(B[1]), "B_z": float(B[2]), "fuerza": float(fuerza)}


def comprobar(res: dict) -> None:
    B = sum(campo_hilo(I, h, np.zeros(3)) for I, h in HILOS)
    assert abs(B[0]) < 1e-20, "el campo no puede tener componente a lo largo de los hilos"
    # Segunda vía para la fuerza: F/L = I2 · (u2 × B1) evaluado sobre el hilo 2.
    I1, h1 = HILOS[0]
    I2, h2 = HILOS[1]
    B1_en_2 = campo_hilo(I1, h1, h2)
    f = I2 * np.cross(i, B1_en_2)
    assert math.isclose(np.linalg.norm(f), res["fuerza"], rel_tol=1e-12)
    # Repulsiva: la fuerza sobre el hilo 2 lo aleja del hilo 1.
    assert np.dot(f, h2 - h1) > 0, "corrientes opuestas deben repelerse"
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["B_y"], 5e-5, rel_tol=1e-9) and math.isclose(res["B_z"], 3e-5, rel_tol=1e-9)
    assert math.isclose(res["fuerza"], 1.06e-4, rel_tol=2e-3)
