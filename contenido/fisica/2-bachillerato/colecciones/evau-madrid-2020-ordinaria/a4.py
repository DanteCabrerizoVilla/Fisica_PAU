"""Verificación de fis2b-evau-madrid-2020-ord-a4 (imagen doble real y virtual)."""

import math

f = 50.0


def posicion(M):
    # s' = M s y 1/s' − 1/s = 1/f  ⇒  s = f (1 − M)/M
    s = f * (1 - M) / M
    return s, M * s


def resolver() -> dict:
    s1, s1p = posicion(-2)
    s2, s2p = posicion(2)
    return {"s1": s1, "s1p": s1p, "s2": s2, "s2p": s2p}


def comprobar(res: dict) -> None:
    for s, sp, M in ((res["s1"], res["s1p"], -2), (res["s2"], res["s2p"], 2)):
        assert math.isclose(1 / sp - 1 / s, 1 / f, rel_tol=1e-12) and math.isclose(sp / s, M)
    assert -2 * f < res["s1"] < -f and -f < res["s2"] < 0
    assert (res["s1"], res["s1p"], res["s2"], res["s2p"]) == (-75, 150, -25, -50)
