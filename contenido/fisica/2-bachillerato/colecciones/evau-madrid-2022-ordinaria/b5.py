"""Verificación de fis2b-evau-madrid-2022-ord-b5 (electrón relativista con la energía de un fotón)."""

import math

e, h, c, m0 = 1.6e-19, 6.63e-34, 3e8, 9.1e-31
longitud = 5e-12


def resolver() -> dict:
    Ec = h * c / longitud
    gamma = 1 + Ec / (m0 * c**2)
    return {"Ec": Ec / e, "Ec_J": Ec, "v": c * math.sqrt(1 - 1 / gamma**2)}


def comprobar(res: dict) -> None:
    v, Ec = res["v"], res["Ec_J"]
    # Con esa velocidad, la energía cinética relativista es la del fotón.
    gamma = 1 / math.sqrt(1 - (v / c) ** 2)
    assert math.isclose((gamma - 1) * m0 * c**2, Ec, rel_tol=1e-9)
    # Segunda vía: E² = (pc)² + (m0c²)², y v = pc²/E.
    E = Ec + m0 * c**2
    p = math.sqrt(E**2 - (m0 * c**2) ** 2) / c
    assert math.isclose(p * c**2 / E, v, rel_tol=1e-9)
    assert v < c
    # La fórmula clásica sobreestima la velocidad en torno a un 33 %.
    assert math.isclose(math.sqrt(2 * Ec / m0) / v, 1.33, rel_tol=1e-2)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["Ec"], 2.49e5, rel_tol=2e-3) and math.isclose(v, 2.22e8, rel_tol=2e-3)
