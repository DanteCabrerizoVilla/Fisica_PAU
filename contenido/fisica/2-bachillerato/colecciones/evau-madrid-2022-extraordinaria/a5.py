"""Verificación de fis2b-evau-madrid-2022-ext-a5 (protón a 0,9 c)."""

import math

c, e = 3e8, 1.6e-19
beta, m = 0.9, 3.83e-27


def resolver() -> dict:
    m0 = m * math.sqrt(1 - beta**2)
    Ec = (m - m0) * c**2
    return {"m0": m0, "Ec": Ec / e, "Ec_J": Ec}


def comprobar(res: dict) -> None:
    gamma = 1 / math.sqrt(1 - beta**2)
    # Segunda vía: Ec = (γ − 1) m0 c².
    assert math.isclose((gamma - 1) * res["m0"] * c**2, res["Ec_J"], rel_tol=1e-12)
    # Tercera vía: E² = (pc)² + (m0c²)², con p = m·v.
    p = m * beta * c
    E = math.hypot(p * c, res["m0"] * c**2)
    assert math.isclose(E - res["m0"] * c**2, res["Ec_J"], rel_tol=1e-9)
    # La fórmula clásica se queda muy corta.
    assert 0.5 * res["m0"] * (beta * c) ** 2 < 0.35 * res["Ec_J"]
    # Valores de la solución orientativa oficial (usa m0 redondeada a 1,67e-27).
    assert math.isclose(res["m0"], 1.669e-27, rel_tol=1e-3)
    assert math.isclose(res["Ec"], 12.15e8, rel_tol=1e-3)
