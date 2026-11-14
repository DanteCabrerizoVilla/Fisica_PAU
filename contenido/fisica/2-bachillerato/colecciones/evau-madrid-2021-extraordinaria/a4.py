"""Verificación de fis2b-evau-madrid-2021-ext-a4 (dos lentes, resolución hacia atrás)."""

import math

import numpy as np

fB, d, s, y, spB = 30.0, 80.0, -15.0, 5.0, 75.0


def resolver() -> dict:
    sB = 1 / (1 / spB - 1 / fB)
    spA = d + sB
    fA = 1 / (1 / spA - 1 / s)
    sA_inf = 1 / (1 / (d - fB) - 1 / fA)
    return {"fA": fA, "y_im": (spA / s) * (spB / sB) * y, "s": sA_inf}


def comprobar(res: dict) -> None:
    lente = lambda f: np.array([[1, 0], [-1 / f, 1]])
    tramo = lambda t: np.array([[1, t], [0, 1]])
    # Hacia delante, con la focal obtenida, la imagen sale a 75 cm de B.
    M = tramo(spB) @ lente(fB) @ tramo(d) @ lente(res["fA"]) @ tramo(-s)
    assert abs(M[0, 1]) < 1e-9 and math.isclose(M[0, 0] * y, res["y_im"], rel_tol=1e-9)
    # Con el objeto en el apartado b, los rayos de un punto salen paralelos.
    S = lente(fB) @ tramo(d) @ lente(res["fA"]) @ tramo(-res["s"])
    assert abs(S[1, 1]) < 1e-12
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["fA"], 10) and math.isclose(res["y_im"], 15) and math.isclose(res["s"], -12.5)
