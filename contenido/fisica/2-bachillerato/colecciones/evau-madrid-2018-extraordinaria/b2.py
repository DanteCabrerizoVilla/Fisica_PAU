"""Verificación de fis2b-evau-madrid-2018-ext-b2 (onda a partir de su foto en t = 0)."""

import math

A, T, k, fase = 0.2, 4.0, 4 * math.pi, math.pi / 3
w = 2 * math.pi / T
x0, t0 = 0.40, 8.0


def y(x, t):
    return A * math.sin(w * t - k * x + fase)


def resolver() -> dict:
    ph = w * t0 - k * x0 + fase
    return {"A": A, "f": 1 / T, "lam": 2 * math.pi / k, "v": w / k,
            "vy": A * w * math.cos(ph), "ay": -A * w**2 * math.sin(ph)}


def comprobar(res: dict) -> None:
    # En t = 0 reproduce la expresión dada.
    for x in (0, 0.1, 0.37):
        assert math.isclose(y(x, 0), 0.2 * math.sin(-4 * math.pi * x + math.pi / 3), abs_tol=1e-15)
    h = 1e-4
    vy = (y(x0, t0 + h) - y(x0, t0 - h)) / (2 * h)
    ay = (y(x0, t0 + h) - 2 * y(x0, t0) + y(x0, t0 - h)) / h**2
    assert math.isclose(vy, res["vy"], rel_tol=1e-6) and math.isclose(ay, res["ay"], rel_tol=1e-5)
