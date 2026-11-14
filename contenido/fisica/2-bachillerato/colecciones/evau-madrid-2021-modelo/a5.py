"""Verificación de fis2b-evau-madrid-2021-mod-a5 (fotoeléctrico en el oro)."""

import math

e, me, h, c = 1.6e-19, 9.1e-31, 6.63e-34, 3e8
lam, Ec = 150e-9, 3.17 * 1.6e-19


def resolver() -> dict:
    W = h * c / lam - Ec
    return {"W": W / e, "corte": h * c / W, "broglie": h / math.sqrt(2 * me * Ec)}


def comprobar(res: dict) -> None:
    v = math.sqrt(2 * Ec / me)
    assert math.isclose(h / (me * v), res["broglie"], rel_tol=1e-12)
    assert res["corte"] > lam
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["W"], 5.12, abs_tol=0.005) and math.isclose(res["corte"], 2.43e-7, rel_tol=2e-3)
    assert math.isclose(res["broglie"], 6.90e-10, rel_tol=1e-3)
