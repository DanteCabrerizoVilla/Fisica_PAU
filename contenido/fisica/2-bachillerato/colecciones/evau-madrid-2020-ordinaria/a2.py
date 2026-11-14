"""Verificación de fis2b-evau-madrid-2020-ord-a2 (onda escrita como sen(kx − ωt + φ))."""

import math

A, w, v = 0.03, 200 * math.pi, 400.0


def resolver() -> dict:
    k = w / v
    candidatas = [math.asin(0.5), math.pi - math.asin(0.5)]
    fase = next(f for f in candidatas if -A * w * math.cos(f) > 0)
    return {"k": k, "fase": fase, "a_max": A * w**2}


def comprobar(res: dict) -> None:
    y = lambda x, t: A * math.sin(res["k"] * x - w * t + res["fase"])
    assert math.isclose(y(0, 0), 0.015, rel_tol=1e-12)
    dt = 1e-8
    assert (y(0, dt) - y(0, -dt)) / (2 * dt) > 0
    assert math.isclose(res["fase"], 5 * math.pi / 6) and math.isclose(res["k"], math.pi / 2)
    assert math.isclose(res["a_max"], 1.18e4, rel_tol=5e-3)
