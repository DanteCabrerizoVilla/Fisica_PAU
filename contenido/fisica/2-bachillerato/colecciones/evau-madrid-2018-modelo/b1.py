"""Verificación de fis2b-evau-madrid-2018-mod-b1 (estrella y planeta)."""

import math
import numpy as np

G, M, T, d = 6.67e-11, 1.3e30, 210 * 86400, 4.6e8
mP = 5e-6 * M


def resolver() -> dict:
    R = (G * M * T**2 / (4 * math.pi**2)) ** (1 / 3)
    g = G * M / (R - d) ** 2 - G * mP / d**2       # módulo, hacia la estrella
    return {"R": R, "g": g}


def comprobar(res: dict) -> None:
    R = res["R"]
    masas = [(M, np.array([0.0, 0])), (mP, np.array([R, 0]))]
    p = np.array([R - d, 0])
    g = sum(G * m * (c - p) / np.linalg.norm(c - p) ** 3 for m, c in masas)
    assert g[0] < 0 and math.isclose(-g[0], res["g"], rel_tol=1e-12)
    # Oficial: R = 89,7·10⁶ km, g = −8,83·10⁻³ u N/kg.
    assert math.isclose(R, 89.7e9, rel_tol=2e-3) and math.isclose(res["g"], 8.83e-3, rel_tol=1e-3)
