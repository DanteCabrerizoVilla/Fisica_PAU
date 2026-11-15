"""Verificación de fis2b-evau-madrid-2019-ord-a5 (trabajo de extracción de dos metales)."""

import math

h, c, e = 6.63e-34, 3e8, 1.6e-19
lam0, lam, Vf = 579e-9, 304e-9, 4.08


def resolver() -> dict:
    W = h * c / lam0
    Ef = h * c / lam
    return {"W": W, "Ec_eV": (Ef - W) / e, "W2": Ef - e * Vf}


def comprobar(res: dict) -> None:
    # Por frecuencias: f0 = c/λ0 y Ec = h(f − f0).
    f0, f = c / lam0, c / lam
    assert math.isclose(h * (f - f0) / e, res["Ec_eV"], rel_tol=1e-12)
    # El segundo trabajo de extracción es positivo pero diminuto (0,009 eV): dato sospechoso.
    assert 0 < res["W2"] / e < 0.02
