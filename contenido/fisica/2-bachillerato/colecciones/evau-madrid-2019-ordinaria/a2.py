"""Verificación de fis2b-evau-madrid-2019-ord-a2 (80 dB a doble distancia)."""

import math

I0, b1 = 1e-12, 80.0


def resolver() -> dict:
    I2 = I0 * 10 ** (b1 / 10) / 4
    return {"I": I2, "beta": 10 * math.log10(I2 / I0)}


def comprobar(res: dict) -> None:
    # Con una distancia y una potencia concretas cualesquiera.
    for r in (0.7, 3.0, 50.0):
        P = I0 * 10 ** (b1 / 10) * 4 * math.pi * r**2
        assert math.isclose(P / (4 * math.pi * (2 * r) ** 2), res["I"], rel_tol=1e-12)
    assert math.isclose(res["beta"], b1 - 10 * math.log10(4), rel_tol=1e-12)
