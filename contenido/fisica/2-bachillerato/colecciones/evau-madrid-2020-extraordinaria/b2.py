"""Verificación de fis2b-evau-madrid-2020-ext-b2 (fase a partir de un punto en un instante)."""

import math

f, lam, vmax = 1000.0, 1.5, 100.0
t0, y0 = 600e-6, 0.01


def resolver() -> dict:
    w = 2 * math.pi * f
    A = vmax / w
    arg = math.asin(y0 / A)                  # la solución con coseno positivo
    return {"v": lam * f, "A": A, "fase": arg - w * t0}


def comprobar(res: dict) -> None:
    w, k, A = 2 * math.pi * f, 2 * math.pi / lam, res["A"]
    y = lambda x, t: A * math.sin(w * t - k * x + res["fase"])
    assert math.isclose(y(0, t0), y0, rel_tol=1e-12)
    dt = 1e-9
    assert (y(0, t0 + dt) - y(0, t0 - dt)) / (2 * dt) > 0
    # La otra fase posible da la misma elongación con velocidad negativa.
    otra = math.pi - math.asin(y0 / A) - w * t0
    assert math.isclose(A * math.sin(w * t0 + otra), y0, rel_tol=1e-9) and math.cos(w * t0 + otra) < 0
    assert math.isclose(res["fase"], -3.09, abs_tol=0.005) and math.isclose(A, 0.0159, rel_tol=1e-3)
