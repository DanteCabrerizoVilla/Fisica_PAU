"""Verificación de fis2b-evau-madrid-2018-ext-a2 (sirena de un barco)."""

import math

I0, beta, r = 1e-12, 80.0, 10.0


def resolver() -> dict:
    I10 = I0 * 10 ** (beta / 10)
    P = I10 * 4 * math.pi * r**2
    dist = lambda b: math.sqrt(P / (4 * math.pi * I0 * 10 ** (b / 10)))
    return {"P": P, "I": P / (4 * math.pi * 1000**2), "r70": dist(70), "r0": dist(0)}


def comprobar(res: dict) -> None:
    nivel = lambda d: 10 * math.log10(res["P"] / (4 * math.pi * d**2) / I0)
    assert math.isclose(nivel(res["r70"]), 70, rel_tol=1e-12)
    assert abs(nivel(res["r0"])) < 1e-9
    assert math.isclose(nivel(1000), 40, rel_tol=1e-12)
