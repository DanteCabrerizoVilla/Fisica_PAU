"""Verificación de fis2b-evau-madrid-2020-ext-b4 (lente de 2,5 D)."""

import math

f = 100 / 2.5


def posicion(M):
    s = f * (1 / M - 1)
    return s, M * s


def resolver() -> dict:
    sa, spa = posicion(2)
    sb, spb = posicion(-0.5)
    return {"s_a": sa, "sp_a": spa, "s_b": sb, "sp_b": spb}


def comprobar(res: dict) -> None:
    for s, sp in ((res["s_a"], res["sp_a"]), (res["s_b"], res["sp_b"])):
        assert math.isclose(1 / sp - 1 / s, 1 / f, rel_tol=1e-12)
    assert res["sp_a"] < 0 < res["sp_b"]
    assert (res["s_a"], res["sp_a"], res["s_b"], res["sp_b"]) == (-20, -40, -120, 60)
