"""Verificación de fis2b-evau-madrid-2018-ord-b5 (electrón con la λ de un fotón de 0,02 MeV)."""

import math

h, e, me, c = 6.63e-34, 1.6e-19, 9.11e-31, 3e8
E = 0.02e6 * e


def resolver() -> dict:
    p = E / c
    return {"v": p / me, "Ec": p**2 / (2 * me) / e, "p": p}


def comprobar(res: dict) -> None:
    lam_foton = h * c / E
    lam_e = h / (me * res["v"])
    assert math.isclose(lam_foton, lam_e, rel_tol=1e-12)
    # Corrección relativista pequeña (< 0,1 %) en la velocidad.
    p = res["p"]
    v_rel = p * c / math.sqrt(p**2 + (me * c) ** 2)
    assert abs(v_rel / res["v"] - 1) < 1e-3
