"""Verificación de fis2b-evau-madrid-2020-ord-b2 (potencia del foco y nivel a 2 m)."""

import math

I0, b1, r1, r2 = 1e-12, 20.0, 10.0, 2.0


def resolver() -> dict:
    P = I0 * 10 ** (b1 / 10) * 4 * math.pi * r1**2
    return {"P": P, "nivel": 10 * math.log10(P / (4 * math.pi * r2**2) / I0)}


def comprobar(res: dict) -> None:
    assert math.isclose(res["nivel"], b1 + 20 * math.log10(r1 / r2), abs_tol=1e-9)
    assert math.isclose(res["P"], 4 * math.pi * 1e-8, rel_tol=1e-12) and math.isclose(res["nivel"], 33.98, abs_tol=0.01)
