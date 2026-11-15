"""Verificación de fis2b-evau-madrid-2018-ord-a3 (espira con varilla móvil)."""

import math

B0, a, b, t = 0.3, 1.0, 0.5, 2.0
xa = lambda s: a + 3 * s
xb = lambda s: a + 0.5 * 2 * s**2


def resolver() -> dict:
    return {"flujo_a": B0 * b * xa(t), "fem_a": B0 * b * 3, "flujo_b": B0 * b * xb(t), "fem_b": B0 * b * 2 * t}


def comprobar(res: dict) -> None:
    h = 1e-6
    for x, fem in ((xa, res["fem_a"]), (xb, res["fem_b"])):
        assert math.isclose(B0 * b * (x(t + h) - x(t - h)) / (2 * h), fem, rel_tol=1e-6)
