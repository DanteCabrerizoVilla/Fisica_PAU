"""Verificación de fis2b-evau-madrid-2018-ord-a2 (altavoces de 60 y 40 W)."""

import math

I0 = 1e-12
focos = [(60.0, (0.0, 0.0)), (40.0, (4.0, 0.0))]
P = (4.0, 3.0)


def intensidad(Pw, c):
    return Pw / (4 * math.pi * math.dist(P, c) ** 2)


def resolver() -> dict:
    I1, I2 = (intensidad(Pw, c) for Pw, c in focos)
    nivel = lambda I: 10 * math.log10(I / I0)
    return {"b1": nivel(I1), "b2": nivel(I2), "bT": nivel(I1 + I2)}


def comprobar(res: dict) -> None:
    # Sumando niveles a través de 10^(β/10).
    total = 10 * math.log10(10 ** (res["b1"] / 10) + 10 ** (res["b2"] / 10))
    assert math.isclose(total, res["bT"], rel_tol=1e-12)
    assert res["b2"] > res["b1"]
