"""Verificación de fis2b-evau-madrid-2022-ext-a4 (imagen real, invertida y de igual tamaño)."""

import math

import sympy as sp


def resolver() -> dict:
    s, sp_, f = sp.symbols("s s_p f", real=True)
    sol = sp.solve([sp.Eq(sp_ / s, -1), sp.Eq(1 / sp_ - 1 / s, 1 / f)], [s, sp_], dict=True)[0]
    return {"cociente": float(sol[s] / f)}


def comprobar(res: dict) -> None:
    # Con varias focales, el objeto a 2f' da imagen a 2f' con aumento −1.
    for f in (5.0, 10.0, 12.5, 40.0):
        s = res["cociente"] * f
        s_im = 1 / (1 / f + 1 / s)
        assert math.isclose(s_im, 2 * f) and math.isclose(s_im / s, -1)
    # Y es la única posición: en cualquier otra, |M| ≠ 1.
    f = 10.0
    for s in (-12.0, -15.0, -25.0, -40.0):
        assert not math.isclose(abs(1 / (1 / f + 1 / s) / s), 1, rel_tol=1e-3)
    assert math.isclose(res["cociente"], -2)
