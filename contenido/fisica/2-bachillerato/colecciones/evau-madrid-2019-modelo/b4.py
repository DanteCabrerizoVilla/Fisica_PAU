"""Verificación de fis2b-evau-madrid-2019-mod-b4 (pez y ángulo crítico)."""

import math

n, c, lam0 = 1.33, 3e8, 525e-9


def resolver() -> dict:
    return {"thc": math.degrees(math.asin(1 / n)), "f": c / lam0, "lam": lam0 / n}


def comprobar(res: dict) -> None:
    # La luz rasante desde el aire (90°) entra con el ángulo crítico.
    assert math.isclose(math.degrees(math.asin(math.sin(math.radians(90)) / n)), res["thc"], rel_tol=1e-12)
    # A 60° dentro del agua no hay refracción posible.
    assert n * math.sin(math.radians(60)) > 1
    assert math.isclose(res["f"] * res["lam"], c / n, rel_tol=1e-12)
    # Oficial: 48,8°; 5,714·10¹⁴ Hz; 395 nm.
    assert math.isclose(res["f"], 5.714e14, rel_tol=1e-3) and math.isclose(res["lam"], 3.95e-7, rel_tol=1e-3)
