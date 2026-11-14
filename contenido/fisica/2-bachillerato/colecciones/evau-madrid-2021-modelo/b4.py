"""Verificación de fis2b-evau-madrid-2021-mod-b4 (prisma de 45° con emergencia rasante)."""

import math

import numpy as np

c, f, apice = 3e8, 4.6e14, math.radians(45)


def resolver() -> dict:
    n = 1 / math.sin(apice)
    return {"n": n, "l_aire": c / f, "l_prisma": c / (f * n)}


def comprobar(res: dict) -> None:
    # Segunda vía con vectores: caras AB y AC forman 45° en A.
    nAB = np.array([-math.cos(apice / 2), math.sin(apice / 2)])     # normales exteriores
    nAC = np.array([math.cos(apice / 2), math.sin(apice / 2)])
    rayo = -nAB                                                     # entra perpendicular
    inc = math.degrees(math.acos(np.dot(rayo, nAC)))
    assert math.isclose(inc, 45, abs_tol=1e-9)
    assert math.isclose(res["n"] * math.sin(math.radians(inc)), 1, rel_tol=1e-12)
    assert math.isclose(res["n"], math.sqrt(2))
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["l_aire"], 652e-9, rel_tol=1e-3) and math.isclose(res["l_prisma"], 461e-9, rel_tol=1e-3)
