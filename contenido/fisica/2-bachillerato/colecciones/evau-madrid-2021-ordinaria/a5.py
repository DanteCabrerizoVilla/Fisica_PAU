"""Verificación de fis2b-evau-madrid-2021-ord-a5 (tres niveles de energía)."""

import math

e, h, c = 1.6e-19, 6.63e-34, 3e8
abs_nm, emi_nm, N = 450e-9, 600e-9, 4e15


def resolver() -> dict:
    E2, E1 = h * c / abs_nm, h * c / emi_nm
    return {"E1": E1 / e, "E2": E2 / e, "P": N * E1}


def comprobar(res: dict) -> None:
    # Segunda vía: con frecuencias.
    assert math.isclose(h * (c / emi_nm) / e, res["E1"], rel_tol=1e-12)
    # El fotón emitido tiene menos energía que el absorbido.
    assert res["E1"] < res["E2"]
    # La transición 2→1 corresponde a radiación infrarroja (≈ 1,8 μm).
    lam21 = h * c / ((res["E2"] - res["E1"]) * e)
    assert math.isclose(lam21, 1.8e-6, rel_tol=1e-3)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["E2"], 2.76, abs_tol=0.005) and math.isclose(res["E1"], 2.07, abs_tol=0.005)
    assert math.isclose(res["P"], 1.33e-3, rel_tol=5e-3)
