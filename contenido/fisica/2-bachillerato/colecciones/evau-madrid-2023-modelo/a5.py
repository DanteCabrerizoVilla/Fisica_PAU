"""Verificación de fis2b-evau-madrid-2023-mod-a5 (positrón acelerado con 3 MV)."""

import math

c, e, m0 = 3e8, 1.6e-19, 9.1e-31
dV = 3e6


def resolver() -> dict:
    Ec = e * dV
    E = m0 * c**2 + Ec
    m = E / c**2
    return {"Ec": Ec, "E": E, "m": m, "v": c * math.sqrt(1 - (m0 / m) ** 2)}


def comprobar(res: dict) -> None:
    # Segunda vía: con la velocidad obtenida, recalcular γ y la energía cinética.
    gamma = 1 / math.sqrt(1 - (res["v"] / c) ** 2)
    assert math.isclose((gamma - 1) * m0 * c**2, res["Ec"], rel_tol=1e-9)
    assert math.isclose(gamma * m0, res["m"], rel_tol=1e-9)
    # Tercera vía: relación energía-momento, E² = (pc)² + (m0c²)².
    p = res["m"] * res["v"]
    assert math.isclose(math.hypot(p * c, m0 * c**2), res["E"], rel_tol=1e-9)
    assert res["v"] < c
    # La fórmula clásica daría una velocidad imposible.
    assert math.sqrt(2 * res["Ec"] / m0) > c
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["E"], 5.62e-13, rel_tol=1e-3)
    assert math.isclose(res["m"], 6.24e-30, rel_tol=1e-3)
    assert math.isclose(res["v"] / c, 0.9893, rel_tol=1e-4)
