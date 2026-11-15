"""Verificación de fis2b-evau-madrid-2019-ext-a2 (sirena a 80 dB)."""

import math

I0, beta, r = 1e-12, 80.0, 200.0


def resolver() -> dict:
    P = I0 * 10 ** (beta / 10) * 4 * math.pi * r**2
    return {"P": P, "r": math.sqrt(2 * P / (4 * math.pi * I0 * 10 ** (beta / 10)))}


def comprobar(res: dict) -> None:
    nivel = lambda P, d: 10 * math.log10(P / (4 * math.pi * d**2) / I0)
    assert math.isclose(nivel(res["P"], r), beta, rel_tol=1e-12)
    assert math.isclose(nivel(2 * res["P"], res["r"]), beta, rel_tol=1e-12)
