"""Verificación de fis2b-pau-madrid-2025-ord-3b (aumento lateral en función de s y f')."""

import math

import sympy as sp


def resolver() -> dict:
    f = 1.0                      # valor absoluto de la focal (unidad arbitraria)
    focal, s = -f, -2 * f
    return {"M": focal / (focal + s)}


def comprobar(res: dict) -> None:
    # Apartado a: demostración simbólica.
    s, f = sp.symbols("s f", nonzero=True)
    s_im = sp.solve(sp.Eq(1 / sp.Symbol("x") - 1 / s, 1 / f), sp.Symbol("x"))[0]
    assert sp.simplify(s_im / s - f / (f + s)) == 0, "la expresión del aumento no se cumple"
    # Apartado b: para lente divergente y objeto real, 0 < M < 1 siempre.
    for focal in (-0.5, -3.0, -40.0):
        for objeto in (-0.01, -1.0, -7.0, -500.0):
            M = focal / (focal + objeto)
            assert 0 < M < 1, f"M = {M} con f' = {focal}, s = {objeto}"
    # Una lente convergente sí puede invertir (objeto más allá del foco).
    assert 10.0 / (10.0 - 30.0) < 0
    # Apartado c: intersección de la prolongación del rayo paralelo con el rayo central.
    focal, objeto, y = -1.0, -2.0, 1.0
    # Rayo paralelo: tras la lente, recta por (focal, 0) y (0, y). Rayo central: recta por (objeto, y) y (0, 0).
    x = sp.Symbol("x")
    corte = sp.solve(sp.Eq(y * (x - focal) / (0 - focal), y / objeto * x), x)[0]
    assert math.isclose(float(corte), -2 / 3, rel_tol=1e-12)
    assert math.isclose(float(y / objeto * corte), res["M"] * y, rel_tol=1e-12)
