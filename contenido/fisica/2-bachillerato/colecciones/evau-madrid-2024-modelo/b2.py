"""Verificación de fis2b-evau-madrid-2024-mod-b2 (segundo foco de potencia doble)."""

import math

# Datos del enunciado (SI)
I_0 = 1e-12
r1 = 3.0
nivel_1, nivel_total = 60.0, 70.0


def resolver() -> dict:
    I1 = I_0 * 10 ** (nivel_1 / 10)
    P1 = 4 * math.pi * r1**2 * I1
    I2 = I_0 * 10 ** (nivel_total / 10) - I1
    return {"I": I1, "P": P1, "x": math.sqrt(2 * P1 / (4 * math.pi * I2))}


def comprobar(res: dict) -> None:
    # Con el segundo foco a la distancia hallada, el nivel total es de 70 dB.
    total = res["P"] / (4 * math.pi * r1**2) + 2 * res["P"] / (4 * math.pi * res["x"] ** 2)
    assert math.isclose(10 * math.log10(total / I_0), nivel_total, rel_tol=1e-12)
    assert math.isclose(res["x"], math.sqrt(2), rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["I"], 1e-6, rel_tol=1e-12) and math.isclose(res["P"], 1.13e-4, rel_tol=2e-3)
