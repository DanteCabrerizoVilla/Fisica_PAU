"""Verificación de fis2b-evau-madrid-2021-mod-b3 (varilla sobre un alambre en U)."""

import math

import numpy as np

B, l, R, I = 0.5, 0.2, 2.0, 1.0


def resolver() -> dict:
    v = I * R / (B * l)
    F_mag = I * np.cross([0.0, l, 0.0], [0.0, 0.0, -B])      # corriente hacia +y en la varilla
    return {"v": v, "F": -F_mag[0]}


def comprobar(res: dict) -> None:
    # Flujo con normal +z (saliente): Φ = −B·l·x. Varilla hacia +x: fem = −dΦ/dt = +B l v (> 0, antihoraria).
    flujo = lambda t: -B * l * (0.5 + res["v"] * t)
    dt = 1e-6
    fem = -(flujo(dt) - flujo(-dt)) / (2 * dt)
    assert fem > 0 and math.isclose(fem / R, I, rel_tol=1e-9)
    # Balance de potencias.
    assert math.isclose(res["F"] * res["v"], I**2 * R, rel_tol=1e-12)
    assert math.isclose(res["v"], 20) and math.isclose(res["F"], 0.1)
