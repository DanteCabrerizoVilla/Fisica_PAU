"""Verificación de fis2b-evau-madrid-2020-ext-a2 (violines)."""

import math

P, f, vs, I0, n, d = 5e-3, 698.0, 340.0, 1e-12, 15, 20.0


def resolver() -> dict:
    return {"longitud": vs / f, "nivel": 10 * math.log10(n * P / (4 * math.pi * d**2) / I0)}


def comprobar(res: dict) -> None:
    uno = 10 * math.log10(P / (4 * math.pi * d**2) / I0)
    assert math.isclose(res["nivel"], uno + 10 * math.log10(n), abs_tol=1e-9)
    assert math.isclose(res["longitud"], 0.487, rel_tol=1e-3) and math.isclose(res["nivel"], 71.74, abs_tol=0.01)
