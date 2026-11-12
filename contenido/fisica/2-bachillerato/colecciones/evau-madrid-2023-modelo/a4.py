"""Verificación de fis2b-evau-madrid-2023-mod-a4 (dos lentes, aumento total +3)."""

import math

import numpy as np

s1, s1p = -15.0, 30.0
f2, M_total = 12.0, 3.0


def resolver() -> dict:
    f1 = 1 / (1 / s1p - 1 / s1)
    M1 = s1p / s1
    M2 = M_total / M1
    s2p = f2 * (1 - M2)          # de 1/s' − 1/s = 1/f con s = s'/M
    s2 = s2p / M2
    return {"f": f1, "M": M1, "D": s1p - s2 + s2p}


def comprobar(res: dict) -> None:
    f1 = res["f"]
    # Segunda vía: matrices de transferencia de rayos (altura, pendiente).
    lente = lambda f: np.array([[1, 0], [-1 / f, 1]])
    tramo = lambda d: np.array([[1, d], [0, 1]])
    d = 50.0                                     # separación entre lentes que sale de la solución
    total = tramo(res["D"] - d) @ lente(f2) @ tramo(d) @ lente(f1) @ tramo(-s1)
    # Hay imagen donde la altura final no depende de la pendiente inicial (B = 0);
    # el aumento es el elemento A.
    assert abs(total[0, 1]) < 1e-9, "en D no se forma la imagen"
    assert math.isclose(total[0, 0], M_total, rel_tol=1e-9)
    # Tercera vía: buscar la separación barriendo valores, sin usar el razonamiento del aumento.
    mejor = None
    for sep in np.arange(31, 120, 0.001):
        s2 = s1p - sep                       # posición de la primera imagen vista desde la lente 2
        s2p = 1 / (1 / f2 + 1 / s2)
        M = (s1p / s1) * (s2p / s2)
        if mejor is None or abs(M - M_total) < abs(mejor[1] - M_total):
            mejor = (sep, M, sep + s2p)
    assert math.isclose(mejor[0], d, abs_tol=2e-3) and math.isclose(mejor[2], res["D"], abs_tol=0.02)
    # Valores de la solución orientativa oficial.
    assert math.isclose(f1, 10) and math.isclose(res["M"], -2) and math.isclose(res["D"], 80)
