"""Verificación de fis2b-evau-madrid-2018-ord-b4 (longitud de onda en dos medios)."""

import math

c, f, n1, n2 = 3e8, 6e14, 1.0, 1.25


def resolver() -> dict:
    return {"lam1": c / (n1 * f), "f2": f, "lam2": c / (n2 * f)}


def comprobar(res: dict) -> None:
    # La velocidad en cada medio es λ·f = c/n.
    assert math.isclose(res["lam2"] * res["f2"], c / n2, rel_tol=1e-12)
    assert math.isclose(res["lam1"] / res["lam2"], n2 / n1, rel_tol=1e-12)
