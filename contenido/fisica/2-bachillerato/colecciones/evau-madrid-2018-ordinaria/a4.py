"""Verificación de fis2b-evau-madrid-2018-ord-a4 (dos lentes de +10 y −10 D)."""

import math
import numpy as np

f1, f2, D, s1, y = 10.0, -10.0, 50.0, -15.0, 10.0


def resolver() -> dict:
    s1p = 1 / (1 / f1 + 1 / s1)
    s2 = s1p - D
    s2p = 1 / (1 / f2 + 1 / s2)
    return {"s1p": s1p, "y1": s1p / s1 * y, "s2p": s2p, "y2": s1p / s1 * s2p / s2 * y}


def comprobar(res: dict) -> None:
    # Matrices de transferencia (altura, ángulo): un rayo que sale del extremo del objeto con
    # cualquier ángulo pasa, tras el sistema, por la imagen final (prolongado).
    lente = lambda f: np.array([[1, 0], [-1 / f, 1]])
    viaje = lambda L: np.array([[1, L], [0, 1]])
    sistema = lente(f2) @ viaje(D) @ lente(f1) @ viaje(-s1)
    for ang in (-0.3, 0.05, 0.4):
        h, u = sistema @ np.array([y, ang])
        # retroceder desde la lente 2 hasta s2′ (negativo): altura = h + u·s2′
        assert math.isclose(h + u * res["s2p"], res["y2"], rel_tol=1e-9)
