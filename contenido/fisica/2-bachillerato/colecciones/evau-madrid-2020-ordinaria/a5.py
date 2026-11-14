"""Verificación de fis2b-evau-madrid-2020-ord-a5 (dos fuentes radiactivas)."""

import math


def resolver() -> dict:
    d = math.log(2) / 10
    return {"diferencia": d, "relacion": math.exp(d * 20)}


def comprobar(res: dict) -> None:
    # Con constantes concretas que cumplen la diferencia, simular las dos fuentes.
    for l1 in (0.01, 0.05, 0.2):
        l2 = l1 + res["diferencia"]
        A0 = 1000.0
        N1, N2 = A0 / l1, A0 / l2                     # misma actividad hoy
        A = lambda lam, N, t: lam * N * math.exp(-lam * t)
        assert math.isclose(A(l1, N1, 10) / A(l2, N2, 10), 2, rel_tol=1e-12)
        assert math.isclose(A(l1, N1, 20) / A(l2, N2, 20), res["relacion"], rel_tol=1e-12)
    assert math.isclose(res["relacion"], 4) and math.isclose(res["diferencia"], 6.93e-2, rel_tol=1e-3)
