"""Verificación de fis2b-evau-madrid-2018-ext-a4 (dos lentes divergentes)."""

import math
import numpy as np

f, D, s1, y = -20.0, 5.0, -60.0, 2.0


def resolver() -> dict:
    s1p = 1 / (1 / f + 1 / s1)
    s2 = s1p - D
    s2p = 1 / (1 / f + 1 / s2)
    return {"s1p": s1p, "s2p": s2p, "yp": s1p / s1 * s2p / s2 * y}


def comprobar(res: dict) -> None:
    lente = lambda fo: np.array([[1, 0], [-1 / fo, 1]])
    viaje = lambda L: np.array([[1, L], [0, 1]])
    sistema = lente(f) @ viaje(D) @ lente(f) @ viaje(-s1)
    for ang in (-0.2, 0.0, 0.15):
        h, u = sistema @ np.array([y, ang])
        assert math.isclose(h + u * res["s2p"], res["yp"], rel_tol=1e-9)
