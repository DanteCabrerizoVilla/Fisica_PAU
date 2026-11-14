"""Verificación de fis2b-evau-madrid-2020-ext-b1 (Mars Reconnaissance Orbiter)."""

import math

G, M, R, h, m = 6.67e-11, 6.42e23, 3.39e6, 2.9e5, 1031


def resolver() -> dict:
    r = R + h
    v = math.sqrt(G * M / r)
    return {"T": 2 * math.pi * r / v, "v": v, "E": G * M * m / (2 * r)}


def comprobar(res: dict) -> None:
    r = R + h
    assert math.isclose(res["T"], 2 * math.pi * math.sqrt(r**3 / (G * M)), rel_tol=1e-12)
    assert math.isclose(res["E"], -(0.5 * m * res["v"] ** 2 - G * M * m / r), rel_tol=1e-12)
    assert math.isclose(res["T"], 6.78e3, rel_tol=1e-3) and math.isclose(res["E"], 6.0e9, rel_tol=1e-3)
