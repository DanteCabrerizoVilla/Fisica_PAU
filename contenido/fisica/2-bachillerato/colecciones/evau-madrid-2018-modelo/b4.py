"""Verificación de fis2b-evau-madrid-2018-mod-b4 (prisma de 60°)."""

import math

n, A, i = 1.5, 60.0, 45.0
sen, asen = lambda g: math.sin(math.radians(g)), lambda x: math.degrees(math.asin(x))


def resolver() -> dict:
    r = asen(sen(i) / n)
    rp = A - r
    L = asen(1 / n)
    return {"r": r, "rp": rp, "e": asen(n * sen(rp)), "imin": asen(n * sen(A - L))}


def comprobar(res: dict) -> None:
    # Barrido: el rayo sale (n·sen r′ ≤ 1) justo a partir de i_mín.
    sale = lambda inc: n * sen(A - asen(sen(inc) / n)) <= 1
    assert sale(res["imin"] + 1e-6) and not sale(res["imin"] - 1e-6)
    # Desviación total: i + e − A.
    assert math.isclose(i + res["e"] - A, 37.38, abs_tol=0.01)
    # Oficial: r = 28,13°, r′ = 31,87°, e = 52,38°, i_mín = 27,92°.
    assert math.isclose(res["imin"], 27.92, abs_tol=0.01)
