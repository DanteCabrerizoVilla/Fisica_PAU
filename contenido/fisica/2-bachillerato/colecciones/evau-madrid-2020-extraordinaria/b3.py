"""Verificación de fis2b-evau-madrid-2020-ext-b3 (espira circular: B = 3t² y espira que gira)."""

import math

S, t = math.pi * 0.06**2, 7e-3
B0, w = 8e-3, 60.0


def resolver() -> dict:
    return {
        "flujo_a": 3 * t**2 * S, "fem_a": 6 * t * S,
        "flujo_b": B0 * S * math.cos(w * t), "fem_b": B0 * S * w * math.sin(w * t),
    }


def comprobar(res: dict) -> None:
    dt = 1e-7
    fa = lambda s: 3 * s**2 * S
    fb = lambda s: B0 * S * math.cos(w * s)
    assert math.isclose((fa(t + dt) - fa(t - dt)) / (2 * dt), res["fem_a"], rel_tol=1e-6)
    assert math.isclose(-(fb(t + dt) - fb(t - dt)) / (2 * dt), res["fem_b"], rel_tol=1e-6)
    assert math.isclose(res["flujo_a"], 1.66e-6, rel_tol=2e-3) and math.isclose(res["fem_a"], 4.75e-4, rel_tol=1e-3)
    assert math.isclose(res["flujo_b"], 8.26e-5, rel_tol=1e-3) and math.isclose(res["fem_b"], 2.21e-3, rel_tol=2e-3)
