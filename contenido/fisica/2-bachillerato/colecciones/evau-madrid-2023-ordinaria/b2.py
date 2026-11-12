"""Verificación de fis2b-evau-madrid-2023-ord-b2 (fuente sonora y reducción del nivel)."""

import math

# Datos del enunciado (SI)
I_0 = 1e-12
r1 = 3.0
nivel = 53.0


def resolver() -> dict:
    I1 = I_0 * 10 ** (nivel / 10)
    P = 4 * math.pi * r1**2 * I1
    I2 = I_0 * 10 ** (nivel / 4 / 10)
    return {"I": I1, "P": P, "r": r1 * math.sqrt(I1 / I2)}


def comprobar(res: dict) -> None:
    # A la distancia hallada el nivel es 13,25 dB.
    I = res["P"] / (4 * math.pi * res["r"] ** 2)
    assert math.isclose(10 * math.log10(I / I_0), nivel / 4, rel_tol=1e-12)
    # Fórmula directa: r2 = r1·10^((b1 − b2)/20).
    assert math.isclose(res["r"], r1 * 10 ** ((nivel - nivel / 4) / 20), rel_tol=1e-12)
    # Lectura alternativa (intensidad a la cuarta parte): 6 m y 6 dB menos.
    assert math.isclose(10 * math.log10(4), 6.02, abs_tol=0.01)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["I"], 1.99e-7, rel_tol=4e-3) and math.isclose(res["P"], 2.25e-5, rel_tol=4e-3)
    assert math.isclose(res["r"], 291.3, rel_tol=2e-3)
