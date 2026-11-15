"""Verificación de fis2b-evau-madrid-2019-ext-b2 (fase de una onda en coseno)."""

import math

A, w, k = 0.05, 8 * math.pi, 4 * math.pi
x0, t0 = 3.0, 5.0


def resolver() -> dict:
    fase = (math.pi - (w * t0 - k * x0)) % (2 * math.pi)
    return {"fase": fase, "t": 8 / (w / k)}


def comprobar(res: dict) -> None:
    y = lambda t: A * math.cos(w * t - k * x0 + res["fase"])
    dt = 1e-5
    v = (y(t0 + dt) - y(t0 - dt)) / (2 * dt)
    a = (y(t0 + dt) - 2 * y(t0) + y(t0 - dt)) / dt**2
    assert abs(v) < 1e-6 and a > 0
    assert math.isclose(res["fase"], math.pi, rel_tol=1e-9)
