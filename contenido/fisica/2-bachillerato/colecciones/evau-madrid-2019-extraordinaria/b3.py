"""Verificación de fis2b-evau-madrid-2019-ext-b3 (positrón en un campo de 5 μT)."""

import math
import numpy as np

e, m, B, R = 1.6e-19, 9.1e-31, 5e-6, 0.50


def resolver() -> dict:
    v = e * B * R / m
    return {"dV": 0.5 * m * v**2 / e, "w": e * B / m}


def comprobar(res: dict) -> None:
    # Integración numérica del movimiento (Boris) con la velocidad que da ΔV: radio y periodo.
    v0 = math.sqrt(2 * e * res["dV"] / m)
    pos, vel = np.zeros(3), np.array([v0, 0, 0])
    Bv = np.array([0, 0, B])
    Tgiro = 2 * math.pi / res["w"]
    n = 20000
    dt = Tgiro / n
    ys = []
    for _ in range(n):
        tvec = (e / m) * Bv * dt / 2
        vp = vel + np.cross(vel, tvec)
        vel = vel + np.cross(vp, 2 * tvec / (1 + tvec @ tvec))
        pos = pos + vel * dt
        ys.append(pos[1])
    assert math.isclose((max(ys) - min(ys)) / 2, R, rel_tol=1e-4)
    assert np.linalg.norm(pos) < 1e-3 * R, "vuelve al punto de partida tras un periodo"
