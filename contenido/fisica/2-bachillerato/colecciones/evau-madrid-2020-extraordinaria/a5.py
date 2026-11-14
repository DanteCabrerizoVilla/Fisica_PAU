"""Verificación de fis2b-evau-madrid-2020-ext-a5 (talio-201)."""

import math

NA, M, T = 6.02e23, 201.0, 3.04 * 86400
A = 0.9e6 * 75


def resolver() -> dict:
    lam = math.log(2) / T
    return {"constante": lam, "masa": A / lam / NA * M, "t": math.log(100) / lam / 86400}


def comprobar(res: dict) -> None:
    assert math.isclose(res["t"], 3.04 * math.log2(100), rel_tol=1e-12)
    assert math.isclose(res["constante"], 2.64e-6, rel_tol=2e-3) and math.isclose(res["masa"], 8.54e-9, rel_tol=2e-3)
    assert math.isclose(res["t"], 20.2, rel_tol=2e-3)
