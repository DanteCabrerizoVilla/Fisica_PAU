"""Verificación de fis2b-evau-madrid-2021-ext-b4 (índices a partir del ángulo límite y la diferencia)."""

import math

c, f, dif = 3e8, 6.04e14, 0.6
limite = math.radians(45.58)


def resolver() -> dict:
    nA = dif / (1 - math.sin(limite))
    nB = nA - dif
    return {"nA": nA, "nB": nB, "lA": c / (nA * f), "lB": c / (nB * f)}


def comprobar(res: dict) -> None:
    assert math.isclose(math.degrees(math.asin(res["nB"] / res["nA"])), 45.58, abs_tol=1e-9)
    assert math.isclose(res["nA"] * res["lA"], res["nB"] * res["lB"], rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["nA"], 2.10, rel_tol=1e-3) and math.isclose(res["nB"], 1.5, rel_tol=1e-3)
    assert math.isclose(res["lA"], 236.52e-9, rel_tol=1e-3) and math.isclose(res["lB"], 331.13e-9, rel_tol=1e-3)
