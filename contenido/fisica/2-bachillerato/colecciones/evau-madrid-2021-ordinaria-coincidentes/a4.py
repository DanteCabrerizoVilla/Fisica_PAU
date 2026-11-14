"""Verificación de fis2b-evau-madrid-2021-ordc-a4 (dos lentes convergentes)."""

import math

import numpy as np

fA, fB, d, s, y = 4.0, 7.0, 25.0, -5.0, 2.0


def resolver() -> dict:
    sA = 1 / (1 / fA + 1 / s)
    sB = sA - d
    spB = 1 / (1 / fB + 1 / sB)
    return {"s_im": spB, "y_im": (sA / s) * (spB / sB) * y}


def comprobar(res: dict) -> None:
    # Segunda vía: matrices de transferencia hasta el plano de la imagen final.
    lente = lambda f: np.array([[1, 0], [-1 / f, 1]])
    tramo = lambda t: np.array([[1, t], [0, 1]])
    M = tramo(res["s_im"]) @ lente(fB) @ tramo(d) @ lente(fA) @ tramo(-s)
    assert abs(M[0, 1]) < 1e-9 and math.isclose(M[0, 0] * y, res["y_im"], rel_tol=1e-9)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["s_im"], -17.5) and math.isclose(res["y_im"], -28)
