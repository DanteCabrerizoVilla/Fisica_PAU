"""Verificación de fis2b-evau-madrid-2019-mod-a5 (pelota y electrones del SLAC)."""

import math
from decimal import Decimal, getcontext

h, c, e, me = 6.63e-34, 3e8, 1.6e-19, 9.1e-31
mb, Ecb = 0.020, 4.0
Ec = 5e4 * 1e6 * e


def resolver() -> dict:
    gamma = 1 + Ec / (me * c**2)
    uno_menos_beta = 1 / (gamma**2 * (1 + math.sqrt(1 - 1 / gamma**2)))   # 1 − β sin cancelación
    return {"lam": h / math.sqrt(2 * mb * Ecb), "v": c * (1 - uno_menos_beta), "uno_menos_beta": uno_menos_beta}


def comprobar(res: dict) -> None:
    # Con 40 cifras decimales, sin trucos algebraicos.
    getcontext().prec = 40
    g = 1 + Decimal(Ec) / (Decimal(me) * Decimal(c) ** 2)
    beta = (1 - 1 / g**2).sqrt()
    assert math.isclose(float(1 - beta), res["uno_menos_beta"], rel_tol=1e-9)
    assert math.isclose(res["lam"], 1.66e-33, rel_tol=2e-3)
    assert res["v"] < c
