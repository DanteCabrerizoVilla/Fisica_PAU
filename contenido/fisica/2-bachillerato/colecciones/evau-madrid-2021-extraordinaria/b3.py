"""Verificación de fis2b-evau-madrid-2021-ext-b3 (espectrómetro con oxígeno-18)."""

import math

import numpy as np

m, q = 2.7e-26, 1.6e-19
E, B1, B2 = np.array([0, 4e5, 0.0]), np.array([0, 0, 2.0]), np.array([0, 0, 5.0])


def resolver() -> dict:
    v = np.linalg.norm(E) / np.linalg.norm(B1)
    return {"v": v, "r": m * v / (q * np.linalg.norm(B2))}


def comprobar(res: dict) -> None:
    v = np.array([res["v"], 0, 0])
    # En el selector la fuerza total se anula.
    assert np.linalg.norm(q * (E + np.cross(v, B1))) < 1e-25
    # Segunda vía: integrar media vuelta en B2 y medir el diámetro.
    pos, vel, dt = np.zeros(3), v.copy(), 1e-11
    ymin = 0.0
    for _ in range(int(math.pi * m / (q * 5) / dt)):
        a = q * np.cross(vel, B2) / m
        vm = vel + 0.5 * dt * a
        pos = pos + dt * vm
        vel = vel + dt * q * np.cross(vm, B2) / m
        ymin = min(ymin, pos[1])
    assert math.isclose(-ymin / 2, res["r"], rel_tol=1e-3), "se curva hacia −y con diámetro 2r"
    # Valores de la solución orientativa oficial (que trunca a 0,67 cm).
    assert math.isclose(res["v"], 2e5) and math.isclose(res["r"], 0.675e-2, rel_tol=1e-9)
