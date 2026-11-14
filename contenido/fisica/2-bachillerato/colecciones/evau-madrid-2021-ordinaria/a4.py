"""Verificación de fis2b-evau-madrid-2021-ord-a4 (lente de 40 D y segunda lente)."""

import math

import numpy as np

P, s, y = 40.0, -15.0, 2.0          # D, cm, mm
f2 = 6.0


def resolver() -> dict:
    f1 = 100 / P
    sp = 1 / (1 / f1 + 1 / s)
    return {"s_im": sp, "y_im": sp / s * y, "d": sp + f2}


def comprobar(res: dict) -> None:
    f1 = 100 / P
    # Segunda vía: matrices de transferencia (altura, pendiente).
    lente = lambda f: np.array([[1, 0], [-1 / f, 1]])
    tramo = lambda d: np.array([[1, d], [0, 1]])
    M1 = tramo(res["s_im"]) @ lente(f1) @ tramo(-s)
    assert abs(M1[0, 1]) < 1e-12 and math.isclose(M1[0, 0], res["y_im"] / y, rel_tol=1e-12)
    # Con la segunda lente a d, el sistema es afocal para ese objeto: la pendiente de salida
    # no depende de la pendiente de entrada desde el punto objeto (C = 0 tras la segunda lente).
    sistema = lente(f2) @ tramo(res["d"]) @ lente(f1) @ tramo(-s)
    assert abs(sistema[1, 1]) < 1e-12, "los rayos de un mismo punto salen paralelos"
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["s_im"], 3) and math.isclose(res["y_im"], -0.4) and math.isclose(res["d"], 9)
