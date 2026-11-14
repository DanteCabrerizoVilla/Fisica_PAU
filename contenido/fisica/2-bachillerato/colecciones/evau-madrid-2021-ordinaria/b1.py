"""Verificación de fis2b-evau-madrid-2021-ord-b1 (sonda en torno a Saturno)."""

import math

G, M, m = 6.67e-11, 5.68e26, 3500
T = 36 * 3600


def resolver() -> dict:
    r = (G * M * T**2 / (4 * math.pi**2)) ** (1 / 3)
    E = -G * M * m / (2 * r)
    return {"v": 2 * math.pi * r / T, "E": E, "E_escape": -E}


def comprobar(res: dict) -> None:
    v = res["v"]
    r = G * M / v**2                     # segunda vía: radio desde la velocidad
    assert math.isclose(2 * math.pi * r / v, T, rel_tol=1e-12)
    assert math.isclose(0.5 * m * v**2 - G * M * m / r, res["E"], rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(v, 12246.62, rel_tol=1e-5) and math.isclose(res["E"], -2.62e11, rel_tol=2e-3)
