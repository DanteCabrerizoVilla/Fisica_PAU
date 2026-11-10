"""Verificación de fis2b-pau-madrid-2025-mod-4a (protón a 0,75 c)."""

import math

# Datos del enunciado
c = 3e8
e = 1.6e-19
E0_MeV = 938.2
beta = 0.75


def resolver() -> dict:
    E0 = E0_MeV * 1e6 * e
    gamma = 1 / math.sqrt(1 - beta**2)
    return {"masa": E0 / c**2, "Ec_MeV": (gamma - 1) * E0_MeV, "Ec_J": (gamma - 1) * E0}


def comprobar(res: dict) -> None:
    m0 = res["masa"]
    v = beta * c
    # Segunda vía: energía total con E² = (pc)² + (m0 c²)², p = gamma m0 v.
    gamma = 1 / math.sqrt(1 - beta**2)
    p = gamma * m0 * v
    total = math.sqrt((p * c) ** 2 + (m0 * c**2) ** 2)
    assert math.isclose(total - m0 * c**2, res["Ec_J"], rel_tol=1e-12)
    # La energía cinética clásica queda muy por debajo (264 MeV).
    clasica = 0.5 * m0 * v**2 / e / 1e6
    assert math.isclose(clasica, 264, rel_tol=5e-3) and clasica < res["Ec_MeV"]
    # Valores de la solución orientativa oficial (usa la masa redondeada).
    assert math.isclose(res["masa"], 1.67e-27, rel_tol=2e-3)
    assert math.isclose(res["Ec_MeV"], 480.8, rel_tol=2e-3) and math.isclose(res["Ec_J"], 7.69e-11, rel_tol=2e-3)
