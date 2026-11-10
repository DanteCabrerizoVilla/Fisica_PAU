"""Verificación de fis2b-pau-madrid-2025-ext-1 (protones relativistas y neutrones lentos)."""

import math

# Datos del enunciado (SI)
c = 3.0e8
e = 1.6e-19
m_p0 = 1.67e-27
m_n = 1.67e-27
h = 6.63e-34
Ec_p = 2e9 * e
Ec_n = 25e-3 * e


def resolver() -> dict:
    masa = m_p0 + Ec_p / c**2
    v = math.sqrt(2 * Ec_n / m_n)
    return {"masa": masa, "velocidad": v, "longitud": h / (m_n * v)}


def comprobar(res: dict) -> None:
    # Protón: con gamma = m/m0 se recupera la energía cinética.
    gamma = res["masa"] / m_p0
    assert math.isclose((gamma - 1) * m_p0 * c**2, Ec_p, rel_tol=1e-12)
    assert gamma > 3, "el protón debe ser claramente relativista"
    # Neutrón: longitud de onda directamente con la energía, lambda = h / sqrt(2 m Ec).
    assert math.isclose(res["longitud"], h / math.sqrt(2 * m_n * Ec_n), rel_tol=1e-12)
    # El neutrón no es relativista: la corrección es despreciable.
    assert res["velocidad"] / c < 1e-4
    # Valores de la solución orientativa oficial.
    for clave, oficial in (("masa", 5.23e-27), ("velocidad", 2.19e3), ("longitud", 1.81e-10)):
        assert math.isclose(res[clave], oficial, rel_tol=3e-3), f"{clave} no coincide con la solución oficial"
