"""Verificación de fis2b-evau-madrid-2018-ord-a5 (frecuencia para una velocidad dada)."""

import math

h, e, me = 6.63e-34, 1.6e-19, 9.11e-31
W, v = 2 * e, 7e5


def resolver() -> dict:
    return {"f": (W + 0.5 * me * v**2) / h}


def comprobar(res: dict) -> None:
    Ec = h * res["f"] - W
    assert math.isclose(math.sqrt(2 * Ec / me), v, rel_tol=1e-12)
    assert res["f"] > W / h
