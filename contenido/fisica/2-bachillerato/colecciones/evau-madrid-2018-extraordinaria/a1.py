"""Verificación de fis2b-evau-madrid-2018-ext-a1 (objeto de 50 kg en Mercurio)."""

import math

G, M, R, m = 6.67e-11, 3.30e23, 2.44e6, 50.0


def resolver() -> dict:
    return {"m": m, "P": m * G * M / R**2, "h": (math.sqrt(3) - 1) * R}


def comprobar(res: dict) -> None:
    P_h = m * G * M / (R + res["h"]) ** 2
    assert math.isclose(P_h, res["P"] / 3, rel_tol=1e-12)
