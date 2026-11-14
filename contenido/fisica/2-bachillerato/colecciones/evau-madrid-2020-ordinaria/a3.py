"""Verificación de fis2b-evau-madrid-2020-ord-a3 (barra sobre rieles en U)."""

import math

import numpy as np

B, L, v, a = 1e-3, 0.30, 100.0, 5.0


def resolver() -> dict:
    return {"fem_a": B * L * v, "pendiente": B * L * a}


def comprobar(res: dict) -> None:
    dt = 1e-6
    flujo_a = lambda t: B * L * (0.1 + v * t)
    flujo_b = lambda t: B * L * (0.1 + 0.5 * a * t**2)
    assert math.isclose((flujo_a(1 + dt) - flujo_a(1 - dt)) / (2 * dt), res["fem_a"], rel_tol=1e-6)
    for t in (0.5, 2.0, 7.0):
        assert math.isclose((flujo_b(t + dt) - flujo_b(t - dt)) / (2 * dt), res["pendiente"] * t, rel_tol=1e-6)
    # Con el campo eléctrico equivalente v × B: módulo v·B a lo largo de la barra.
    E = np.cross([v, 0, 0], [0, 0, B])
    assert math.isclose(np.linalg.norm(E) * L, res["fem_a"], rel_tol=1e-12)
    assert math.isclose(res["fem_a"], 0.03) and math.isclose(res["pendiente"], 1.5e-3)
