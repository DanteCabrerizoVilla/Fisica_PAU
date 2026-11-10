"""Verificación de fis2b-pau-madrid-2025-ord-2b (corriente máxima inducida en una espira)."""

import math

import numpy as np

# Datos del enunciado (SI)
r = 0.20
R = 40.0
S = math.pi * r**2
B_a, w_a = 0.150, 50.0
B_b, w_b = 0.200, 75.0


def resolver() -> dict:
    return {"I_a": B_a * S * w_a / R, "I_b": B_b * S * w_b / R}


def comprobar(res: dict) -> None:
    # Segunda vía: derivar numéricamente el flujo y buscar el máximo de |fem| en un periodo.
    def maximo(flujo, w):
        t = np.linspace(0, 2 * math.pi / w, 200001)
        fem = -np.gradient(flujo(t), t)
        return float(np.max(np.abs(fem)))

    fem_a = maximo(lambda t: B_a * S * np.cos(w_a * t), w_a)
    fem_b = maximo(lambda t: B_b * np.sin(w_b * t) * S, w_b)
    assert math.isclose(fem_a / R, res["I_a"], rel_tol=1e-6), f"caso a: {fem_a / R}"
    assert math.isclose(fem_b / R, res["I_b"], rel_tol=1e-6), f"caso b: {fem_b / R}"
    assert math.isclose(res["I_b"], 2 * res["I_a"], rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["I_a"], 0.0236, rel_tol=2e-3) and math.isclose(res["I_b"], 0.0471, rel_tol=2e-3)
