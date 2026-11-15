"""Verificación de fis2b-evau-madrid-2019-ord-a4 (lupa y lente para miopía)."""

import math

f, M, remoto = 0.30, 2.0, -0.5


def resolver() -> dict:
    return {"s": f * (1 / M - 1), "P": 1 / remoto}


def comprobar(res: dict) -> None:
    s = res["s"]
    sp = 1 / (1 / f + 1 / s)
    assert sp < 0 and math.isclose(sp / s, M, rel_tol=1e-12)
    # Objeto muy lejano con la lente de −2 D: la imagen tiende al punto remoto.
    sp_lejos = 1 / (res["P"] + 1 / -1e9)
    assert math.isclose(sp_lejos, remoto, rel_tol=1e-8)
    assert math.isclose(s, -0.15)
