"""Verificación de fis2b-evau-madrid-2022-mod-a4 (aumento con el objeto a f'/3 y a 3f')."""

import math

import sympy as sp


def aumento(fraccion):
    f = sp.symbols("f", positive=True)
    s = -fraccion * f
    s_im = 1 / (1 / f + 1 / s)
    return sp.simplify(s_im / s), sp.simplify(s_im / f)


def resolver() -> dict:
    return {"M_a": float(aumento(sp.Rational(1, 3))[0]), "M_b": float(aumento(3)[0])}


def cruce(f, s, altura=1.0):
    """Segunda vía: cortar el rayo paralelo y el rayo central trazados como rectas."""
    m1, b1 = -altura / f, altura           # tras la lente, pasa por F'
    m2 = altura / s                        # pasa por el centro
    x = b1 / (m2 - m1)
    return x, m2 * x


def comprobar(res: dict) -> None:
    for f in (5.0, 12.0, 30.0):
        xa, ha = cruce(f, -f / 3)
        assert math.isclose(xa, -f / 2) and math.isclose(ha, res["M_a"]) and xa < 0
        xb, hb = cruce(f, -3 * f)
        assert math.isclose(xb, 1.5 * f) and math.isclose(hb, res["M_b"]) and xb > 0
    # Posiciones de la imagen en unidades de f'.
    assert aumento(sp.Rational(1, 3))[1] == sp.Rational(-1, 2) and aumento(3)[1] == sp.Rational(3, 2)
    # Expresión general M = f'/(f' + s).
    assert math.isclose(1 / (1 - 1 / 3), res["M_a"]) and math.isclose(1 / (1 - 3), res["M_b"])
