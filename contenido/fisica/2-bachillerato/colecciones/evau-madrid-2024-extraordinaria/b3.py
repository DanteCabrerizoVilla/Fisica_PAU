"""Verificación de fis2b-evau-madrid-2024-ext-b3 (dos hilos con corrientes opuestas)."""

import math

import numpy as np

# Datos del enunciado (SI)
MU0 = 4 * math.pi * 1e-7
k = np.array([0.0, 0.0, 1.0])
HILOS = [(2.0, np.array([0.0, 0.0, 0.0])), (-2.0, np.array([4.0, 0.0, 0.0]))]    # signo: sentido en z


def campo(punto):
    total = np.zeros(3)
    for I, hilo in HILOS:
        r = punto - hilo
        d = np.linalg.norm(r)
        total += MU0 * I / (2 * math.pi * d) * np.cross(k, r / d)
    return total


def resolver() -> dict:
    BA = campo(np.array([0.0, 3.0, 0.0]))
    BB = campo(np.array([2.0, 3.0, 0.0]))
    bbx = 0.0 if abs(BB[0]) < 1e-9 * abs(BB[1]) else float(BB[0])     # se anula por simetría
    return {"BA_x": float(BA[0]), "BA_y": float(BA[1]), "BB_x": bbx, "BB_y": float(BB[1])}


def comprobar(res: dict) -> None:
    # Segunda vía: Biot-Savart integrado numéricamente sobre hilos muy largos.
    z = np.linspace(-400, 400, 4_000_001)
    dz = z[1] - z[0]

    def biot(punto):
        total = np.zeros(3)
        for I, hilo in HILOS:
            r = punto - hilo
            factor = MU0 * I / (4 * math.pi) * np.sum(dz / (r[0] ** 2 + r[1] ** 2 + z**2) ** 1.5)
            total += factor * np.cross(k, r)
        return total

    BB = biot(np.array([2.0, 3.0, 0.0]))
    assert math.isclose(BB[1], res["BB_y"], rel_tol=1e-3), f"Biot-Savart da {BB[1]}"
    BA = biot(np.array([0.0, 3.0, 0.0]))
    assert math.isclose(BA[0], res["BA_x"], rel_tol=1e-3) and math.isclose(BA[1], res["BA_y"], rel_tol=1e-3)
    # Expresión de la solución oficial para B: 2·mu0·I/(2π·raíz(13))·(2/raíz(13)).
    expresion = 2 * MU0 * 2 / (2 * math.pi * math.sqrt(13)) * 2 / math.sqrt(13)
    assert math.isclose(expresion, res["BB_y"], rel_tol=1e-12)
    assert math.isclose(expresion, 1.23e-7, rel_tol=2e-3), "la expresión oficial vale 1,23e-7 (el documento imprime 1,28e-7)"
    # Valores oficiales del apartado a.
    assert math.isclose(res["BA_x"], -8.53e-8, rel_tol=2e-3) and math.isclose(res["BA_y"], 6.40e-8, rel_tol=2e-3)
