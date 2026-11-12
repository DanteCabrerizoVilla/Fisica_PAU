"""Verificación de fis2b-evau-madrid-2022-ext-a1 (Sentinel-1)."""

import math

G, M, R = 6.67e-11, 5.97e24, 6.37e6
m, h = 2300, 7e5


def resolver() -> dict:
    r = R + h
    return {"T": 2 * math.pi * math.sqrt(r**3 / (G * M)), "E": -G * M * m / (2 * r)}


def comprobar(res: dict) -> None:
    r = R + h
    # Segunda vía: velocidad orbital, y de ella periodo y energías por separado.
    v = math.sqrt(G * M / r)
    assert math.isclose(2 * math.pi * r / v, res["T"], rel_tol=1e-12)
    Ec, Ep = 0.5 * m * v**2, -G * M * m / r
    assert math.isclose(Ec + Ep, res["E"], rel_tol=1e-12)
    assert math.isclose(Ec, -Ep / 2, rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["T"], 5919.14, rel_tol=1e-5)
    assert math.isclose(res["E"], -6.48e10, rel_tol=1e-3)
