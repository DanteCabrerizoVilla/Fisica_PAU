"""Verificación de fis2b-evau-madrid-2021-ordc-a1 (perdigón en órbita)."""

import math

G, M, m, r = 6.67e-11, 6.0, 3.5e-4, 2.5


def resolver() -> dict:
    return {"T": 2 * math.pi * math.sqrt(r**3 / (G * M)), "E": G * M * m / (2 * r)}


def comprobar(res: dict) -> None:
    v = math.sqrt(G * M / r)
    assert math.isclose(2 * math.pi * r / v, res["T"], rel_tol=1e-12)
    assert math.isclose(-(0.5 * m * v**2 - G * M * m / r), res["E"], rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["T"], 1.24e6, rel_tol=2e-3) and math.isclose(res["E"], 2.8e-14, rel_tol=1e-3)
