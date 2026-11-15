"""Verificación de fis2b-evau-madrid-2020-mod-a2 (onda a partir de su foto en t = 0)."""

import math

v, lam, A = 1500.0, 20.0, 6e-3


def resolver() -> dict:
    k = 2 * math.pi / lam
    w = 2 * math.pi * v / lam
    # sen φ = −1/2 → −π/6 o 7π/6; en t = 0 la gráfica sube con x en x = 0
    candidatas = (-math.pi / 6, 7 * math.pi / 6)
    fase = next(f for f in candidatas if -A * k * math.cos(f) > 0)   # dy/dx en x = 0, t = 0
    return {"k": k, "w": w, "fase": fase}


def comprobar(res: dict) -> None:
    k, f = res["k"], res["fase"]
    y = lambda x: A * math.sin(f - k * x)
    # Puntos leídos en la gráfica: y(0) = −3 mm, cero en x = 5/3 m, máximo en x = 20/3 m.
    assert math.isclose(y(0), -3e-3, rel_tol=1e-12)
    assert abs(y(5 / 3)) < 1e-15 and math.isclose(y(20 / 3), A, rel_tol=1e-12)
    assert math.isclose(y(5), 5.196e-3, rel_tol=1e-3)
    assert math.isclose(res["w"], 150 * math.pi) and math.isclose(f, 7 * math.pi / 6)
