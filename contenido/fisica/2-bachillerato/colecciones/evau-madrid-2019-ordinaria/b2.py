"""Verificación de fis2b-evau-madrid-2019-ord-b2 (onda a partir de dos instantes)."""

import math

f, lam, x0 = 0.25, 2.0, 0.5
w, k = 2 * math.pi * f, 2 * math.pi / lam


def resolver() -> dict:
    fase = math.pi - (w * 2 - k * x0)            # argumento = π en t = 2 s
    A = -0.2 / math.sin(w * 3 - k * x0 + fase)   # condición en t = 3 s
    return {"A": A, "fase": fase, "vmax": A * w, "dfase": k * 0.75}


def comprobar(res: dict) -> None:
    A, fase = res["A"], res["fase"]
    y = lambda x, t: A * math.sin(w * t - k * x + fase)
    dt = 1e-6
    assert abs(y(x0, 2)) < 1e-12 and (y(x0, 2 + dt) - y(x0, 2 - dt)) < 0
    assert math.isclose(y(x0, 3), -0.2, rel_tol=1e-12)
    assert A > 0 and math.isclose(fase, math.pi / 2)
