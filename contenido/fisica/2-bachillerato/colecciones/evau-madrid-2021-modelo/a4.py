"""Verificación de fis2b-evau-madrid-2021-mod-a4 (dos lentes y imagen en el infinito)."""

import math

import numpy as np

f, s = 20.0, -25.0


def resolver() -> dict:
    sp1 = 1 / (1 / f + 1 / s)
    return {"d": sp1 + f}


def comprobar(res: dict) -> None:
    lente = lambda F: np.array([[1, 0], [-1 / F, 1]])
    tramo = lambda t: np.array([[1, t], [0, 1]])
    S = lente(f) @ tramo(res["d"]) @ lente(f) @ tramo(-s)
    assert abs(S[1, 1]) < 1e-12, "los rayos de un mismo punto del objeto salen paralelos"
    assert math.isclose(res["d"], 120)
