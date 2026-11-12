"""Verificación de fis2b-evau-madrid-2022-mod-a1 (la Tierra entre afelio y perihelio)."""

import math

import numpy as np

G, MS, MT = 6.67e-11, 1.99e30, 5.97e24
ra, rp = 1.52e11, 1.47e11
Em = -2.65e33


def resolver() -> dict:
    W = G * MS * MT * (1 / rp - 1 / ra)
    v = math.sqrt(2 * (Em / MT + G * MS / rp))
    return {"W": W, "v": v}


def comprobar(res: dict) -> None:
    # Segunda vía para el trabajo: integral de la fuerza radial del afelio al perihelio.
    r = np.linspace(ra, rp, 200001)
    F = -G * MS * MT / r**2                      # componente radial (hacia el Sol)
    W = float(np.sum(0.5 * (F[1:] + F[:-1]) * np.diff(r)))
    assert math.isclose(W, res["W"], rel_tol=1e-8)
    # Segunda vía para la velocidad: órbita de Kepler con esos extremos (vis-viva).
    a = (ra + rp) / 2
    v_kepler = math.sqrt(G * MS * (2 / rp - 1 / a))
    assert math.isclose(v_kepler, res["v"], rel_tol=2e-3), "la energía del enunciado debe encajar con las distancias"
    assert math.isclose(-G * MS * MT / (2 * a), Em, rel_tol=2e-3)
    # En el afelio va más despacio, y el trabajo es el aumento de energía cinética.
    v_afelio = math.sqrt(2 * (Em / MT + G * MS / ra))
    assert v_afelio < res["v"]
    assert math.isclose(0.5 * MT * (res["v"] ** 2 - v_afelio**2), res["W"], rel_tol=1e-9)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["W"], 1.77e32, rel_tol=2e-3) and math.isclose(res["v"], 3.03e4, rel_tol=1e-3)
