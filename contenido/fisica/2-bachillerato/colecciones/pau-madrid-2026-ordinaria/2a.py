"""Verificación de fis2b-pau-madrid-2026-ord-2a (órbita a partir de la energía mecánica)."""

import math

# Datos del enunciado (SI)
G = 6.67e-11
M_T = 5.97e24
m = 1500.0
E_m = -4.51e10
DIA = 86400.0


def resolver() -> dict:
    r = -G * M_T * m / (2 * E_m)
    v = math.sqrt(G * M_T / r)
    T = 2 * math.pi * r / v
    return {"r": r, "v": v, "vueltas": DIA / T, "v_escape": math.sqrt(2 * G * M_T / r)}


def comprobar(res: dict) -> None:
    r, v = res["r"], res["v"]
    # Con ese radio y esa velocidad se recupera la energía del enunciado.
    assert math.isclose(0.5 * m * v**2 - G * M_T * m / r, E_m, rel_tol=1e-12), "no se recupera la energía"
    # En órbita circular Ec = -Em, luego v = sqrt(-2 Em / m).
    assert math.isclose(v, math.sqrt(-2 * E_m / m), rel_tol=1e-12)
    # Periodo por la tercera ley de Kepler.
    T = 2 * math.pi * math.sqrt(r**3 / (G * M_T))
    assert math.isclose(res["vueltas"], DIA / T, rel_tol=1e-12)
    assert math.isclose(res["v_escape"], math.sqrt(2) * v, rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    for clave, oficial in (("r", 6.62e6), ("v", 7754.6), ("vueltas", 16.10), ("v_escape", 1.1e4)):
        assert math.isclose(res[clave], oficial, rel_tol=5e-3), f"{clave} no coincide con la solución oficial"
