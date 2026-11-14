"""Verificación de fis2b-evau-madrid-2020-ord-b1 (gravedad y escape)."""

import math

G, M, R = 6.67e-11, 1.95e25, 5.5e6


def resolver() -> dict:
    g = G * M / R**2
    return {"g": g, "v": math.sqrt(2 * G * M / R)}


def comprobar(res: dict) -> None:
    assert math.isclose(res["v"], math.sqrt(2 * res["g"] * R), rel_tol=1e-12)
    assert math.isclose(res["g"], 43, rel_tol=1e-3) and math.isclose(res["v"], 21.75e3, rel_tol=1e-3)
