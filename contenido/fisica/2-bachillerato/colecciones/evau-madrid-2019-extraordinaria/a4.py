"""Verificación de fis2b-evau-madrid-2019-ext-a4 (lente de 10 cm, imagen a 14 cm)."""

import math

f, sp, y = 10.0, 14.0, 1.0


def resolver() -> dict:
    s = 1 / (1 / sp - 1 / f)
    return {"s": s, "yp": sp / s * y}


def comprobar(res: dict) -> None:
    s = res["s"]
    # Trazado: el rayo paralelo sale de la lente a altura y y pasa por F′ → y1(x) = y(1 − x/f).
    # El rayo central pasa por el objeto (s, y) y por el centro (0, 0) → y2(x) = (y/s)·x.
    xi = 1 / (1 / f + 1 / s)                     # donde se cortan
    assert math.isclose(y * (1 - xi / f), (y / s) * xi, rel_tol=1e-12)
    assert math.isclose(xi, sp, rel_tol=1e-12)
    assert math.isclose(res["yp"], (y / s) * xi, rel_tol=1e-12)
