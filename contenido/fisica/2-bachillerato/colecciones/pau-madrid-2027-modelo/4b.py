"""Verificación de fis2b-pau-madrid-2027-mod-4b (protones relativistas)."""

import math

# Datos del enunciado (SI)
e = 1.6e-19
c = 3e8
m0 = 1.67e-27
Ec = 1.4e9 * e


def resolver() -> dict:
    m = m0 + Ec / c**2
    v = c * math.sqrt(1 - (m0 / m) ** 2)
    return {"masa": m, "velocidad": v}


def comprobar(res: dict) -> None:
    m, v = res["masa"], res["velocidad"]
    assert v < c, "la velocidad no puede superar la de la luz"
    # Con esa velocidad, la energía cinética relativista debe ser la del enunciado.
    gamma = 1 / math.sqrt(1 - (v / c) ** 2)
    assert math.isclose((gamma - 1) * m0 * c**2, Ec, rel_tol=1e-9), "no se recupera la energía cinética"
    assert math.isclose(gamma * m0, m, rel_tol=1e-9), "la masa relativista no es gamma·m0"
    # Relación energía-momento: E² = (pc)² + (m0 c²)².
    p = m * v
    assert math.isclose((m * c**2) ** 2, (p * c) ** 2 + (m0 * c**2) ** 2, rel_tol=1e-9)
    # La fórmula clásica daría una velocidad mayor que c (lo dice la solución).
    assert math.isclose(math.sqrt(2 * Ec / m0), 5.2e8, rel_tol=1e-2)
    # Valores de la solución orientativa oficial.
    assert math.isclose(m, 4.16e-27, rel_tol=5e-3) and math.isclose(v, 2.75e8, rel_tol=5e-3)
