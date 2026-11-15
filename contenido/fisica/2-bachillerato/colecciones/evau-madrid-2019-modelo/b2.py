"""Verificación de fis2b-evau-madrid-2019-mod-b2 (onda a partir de la oscilación del origen)."""

import math

A, w, fase, lam = 0.5, math.pi / 4, math.pi / 2, 0.1
y0, t0 = 0.5, 40.0


def z(y, t, k):
    return A * math.sin(w * t - k * y + fase)


def resolver() -> dict:
    k = 2 * math.pi / lam
    arg = w * t0 - k * y0 + fase
    return {"k": k, "v": round(A * w * math.cos(arg), 12), "a": -A * w**2 * math.sin(arg)}


def comprobar(res: dict) -> None:
    k, dt = res["k"], 1e-3
    # Derivadas numéricas en el tiempo.
    v = (z(y0, t0 + dt, k) - z(y0, t0 - dt, k)) / (2 * dt)
    a = (z(y0, t0 + dt, k) - 2 * z(y0, t0, k) + z(y0, t0 - dt, k)) / dt**2
    assert abs(v) < 1e-6 and math.isclose(a, res["a"], rel_tol=1e-5)
    # En y = 0 reproduce el movimiento dado.
    assert all(math.isclose(z(0, t, k), A * math.sin(w * t + fase), abs_tol=1e-15) for t in (0, 1.3, 7))
    # Oficial: v = 0, a = −π²/32 m/s².
    assert math.isclose(res["a"], -math.pi**2 / 32, rel_tol=1e-12)
