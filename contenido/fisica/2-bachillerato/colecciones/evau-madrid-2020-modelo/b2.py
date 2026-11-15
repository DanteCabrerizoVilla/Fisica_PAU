"""Verificación de fis2b-evau-madrid-2020-mod-b2 (sirena a 50 y 70 dB)."""

import math

I0, b1, b2, d = 1e-12, 50.0, 70.0, 50.0


def resolver() -> dict:
    q = math.sqrt(10 ** ((b2 - b1) / 10))     # r / (r − d)
    r = q * d / (q - 1)
    I = I0 * 10 ** (b1 / 10)
    return {"r": r, "I": I, "P": I * 4 * math.pi * r**2}


def comprobar(res: dict) -> None:
    P, r = res["P"], res["r"]
    nivel = lambda x: 10 * math.log10(P / (4 * math.pi * x**2) / I0)
    assert math.isclose(nivel(r), b1, rel_tol=1e-12) and math.isclose(nivel(r - d), b2, rel_tol=1e-12)
    # La solución oficial usa 5 m en vez de 50 m: r = 5,55 m. Con 5 m sale exactamente eso.
    assert math.isclose(10 * 5 / 9, 5.555, rel_tol=1e-3)
    assert math.isclose(r, 500 / 9) and math.isclose(P, 3.8785e-3, rel_tol=1e-4)
