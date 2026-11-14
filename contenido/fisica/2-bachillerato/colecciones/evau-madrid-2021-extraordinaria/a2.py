"""Verificación de fis2b-evau-madrid-2021-ext-a2 (conversación a través de una pared)."""

import math

I0 = 1e-12
b1, r, pared, alcance = 50.0, 5.0, 0.02, 100.0


def resolver() -> dict:
    I1 = I0 * 10 ** (b1 / 10)
    return {"nivel": 10 * math.log10(pared * I1 / r**2 / I0),
            "minimo": 10 * math.log10(I1 / alcance**2 / I0)}


def comprobar(res: dict) -> None:
    # Segunda vía en decibelios: −20·log r y +10·log 0,02.
    assert math.isclose(res["nivel"], b1 - 20 * math.log10(r) + 10 * math.log10(pared), abs_tol=1e-9)
    # Con la potencia de la conversación.
    P = I0 * 10 ** (b1 / 10) * 4 * math.pi
    assert math.isclose(10 * math.log10(P / (4 * math.pi * alcance**2) / I0), res["minimo"], abs_tol=1e-9)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["nivel"], 19.03, abs_tol=0.01) and math.isclose(res["minimo"], 10, abs_tol=1e-9)
