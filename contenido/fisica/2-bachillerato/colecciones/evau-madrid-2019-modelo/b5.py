"""Verificación de fis2b-evau-madrid-2019-mod-b5 (radio-226)."""

import math

T, m0, t = 1602.0, 20.0, 1800 / 12


def resolver() -> dict:
    lam = math.log(2) / T
    return {"tau": 1 / lam, "m": m0 * math.exp(-lam * t), "fraccion": math.exp(-1)}


def comprobar(res: dict) -> None:
    assert math.isclose(m0 * 0.5 ** (t / T), res["m"], rel_tol=1e-12)
    assert math.isclose(0.5 ** (res["tau"] / T), res["fraccion"], rel_tol=1e-12)
    # Oficial: τ = 2311,2 años, m = 18,74 mg, A = 0,367·A0 (es 0,3679).
    assert math.isclose(res["tau"], 2311.2, rel_tol=1e-4) and math.isclose(res["m"], 18.74, rel_tol=1e-3)
