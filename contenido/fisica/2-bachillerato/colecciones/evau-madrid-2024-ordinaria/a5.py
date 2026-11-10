"""Verificación de fis2b-evau-madrid-2024-ord-a5 (cobalto: duplicar la frecuencia)."""

import math

# Datos del enunciado
e = 1.6e-19
h = 6.63e-34
factor = 1.2
diferencia = 6.0     # V


def resolver() -> dict:
    W_eV = diferencia / (2 * factor - factor)
    return {"W": W_eV, "f0": W_eV * e / h}


def comprobar(res: dict) -> None:
    W = res["W"] * e
    f0 = res["f0"]
    f1, f2 = factor * f0, 2 * factor * f0
    V1 = (h * f1 - W) / e
    V2 = (h * f2 - W) / e
    assert V1 > 0, "con f1 > f0 debe haber emisión"
    assert math.isclose(V2 - V1, diferencia, rel_tol=1e-12)
    assert math.isclose(V1, 1.0, rel_tol=1e-9) and math.isclose(V2, 7.0, rel_tol=1e-9)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["W"], 5.0, rel_tol=1e-12) and math.isclose(res["f0"], 1.21e15, rel_tol=3e-3)
