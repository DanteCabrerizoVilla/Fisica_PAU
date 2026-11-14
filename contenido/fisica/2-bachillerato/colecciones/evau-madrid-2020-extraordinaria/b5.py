"""Verificación de fis2b-evau-madrid-2020-ext-b5 (láser de tres niveles)."""

import math

h, c, e = 6.63e-34, 3e8, 1.6e-19
E3, E2, N = 2.76 * e, 2.07 * e, 2e16


def resolver() -> dict:
    f13 = E3 / h
    return {"f13": f13, "l13": c / f13, "l21": h * c / E2, "P": N * E2}


def comprobar(res: dict) -> None:
    assert math.isclose(h * c / res["l13"], E3, rel_tol=1e-12)
    assert res["l21"] > res["l13"], "el fotón emitido tiene menos energía"
    assert math.isclose(res["f13"], 6.66e14, rel_tol=1e-3) and math.isclose(res["l13"], 450e-9, rel_tol=1e-3)
    assert math.isclose(res["l21"], 600e-9, rel_tol=2e-3) and math.isclose(res["P"], 6.62e-3, rel_tol=1e-3)
