"""Verificación de fis2b-evau-madrid-2019-mod-a4 (lente para la presbicia)."""

import math

s, sp = -0.25, -1.0


def resolver() -> dict:
    P = 1 / sp - 1 / s
    return {"f": 1 / P, "P": P}


def comprobar(res: dict) -> None:
    # Con esa lente, el libro a 25 cm da imagen en el punto próximo (1 m, virtual).
    imagen = 1 / (1 / res["f"] + 1 / s)
    assert math.isclose(imagen, sp, rel_tol=1e-12)
    assert math.isclose(res["P"], 3.0)
