"""Verificación de fis2b-evau-madrid-2021-mod-a1 (el Sol alrededor del centro galáctico)."""

import math

G, r = 6.67e-11, 2.4e20
T = 203e6 * 365 * 86400


def resolver() -> dict:
    v = 2 * math.pi * r / T
    return {"v": v, "M": v**2 * r / G}


def comprobar(res: dict) -> None:
    # Segunda vía: tercera ley de Kepler.
    assert math.isclose(4 * math.pi**2 * r**3 / (G * T**2), res["M"], rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["v"], 235.6e3, rel_tol=1e-3) and math.isclose(res["M"], 1.99e41, rel_tol=5e-3)
