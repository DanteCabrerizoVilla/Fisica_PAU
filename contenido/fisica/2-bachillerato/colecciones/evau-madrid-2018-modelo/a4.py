"""Verificación de fis2b-evau-madrid-2018-mod-a4 (lente con aumentos −2 y +2)."""

import math

desplazamiento = 20.0


def resolver() -> dict:
    # s = f(1/M − 1): s2 − s1 = f[(1/2 − 1) − (−1/2 − 1)] = f
    f = desplazamiento / ((1 / 2 - 1) - (-1 / 2 - 1))
    return {"f": f, "P": 100 / f}


def comprobar(res: dict) -> None:
    f = res["f"]
    for s, M in ((-30.0, -2.0), (-10.0, 2.0)):
        sp = 1 / (1 / f + 1 / s)
        assert math.isclose(sp / s, M, rel_tol=1e-12)
    # Oficial: f′ = 20 cm, P = 5 D.
    assert math.isclose(f, 20) and math.isclose(res["P"], 5)
