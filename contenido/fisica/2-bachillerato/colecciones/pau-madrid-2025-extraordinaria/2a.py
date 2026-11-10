"""Verificación de fis2b-pau-madrid-2025-ext-2a (radio y masa de la Tierra con T y v de escape)."""

import math

# Datos del enunciado (SI)
G = 6.67e-11
T = 1.59 * 3600
v_e = 10.7e3


def resolver() -> dict:
    r = v_e * T / (2 * math.sqrt(2) * math.pi)
    M = v_e**2 * r / (2 * G)
    return {"r": r, "M": M}


def comprobar(res: dict) -> None:
    r, M = res["r"], res["M"]
    # Con esos valores se recuperan los dos datos del enunciado.
    assert math.isclose(2 * math.pi * math.sqrt(r**3 / (G * M)), T, rel_tol=1e-12), "no se recupera el periodo"
    assert math.isclose(math.sqrt(2 * G * M / r), v_e, rel_tol=1e-12), "no se recupera la velocidad de escape"
    # Vía alternativa: velocidad orbital = v_e / raíz de 2.
    assert math.isclose(r, (v_e / math.sqrt(2)) * T / (2 * math.pi), rel_tol=1e-12)
    # La masa obtenida es cercana a la real.
    assert math.isclose(M, 5.97e24, rel_tol=2e-2)
    # Valores de la solución orientativa oficial.
    assert math.isclose(r, 6.89e6, rel_tol=2e-3) and math.isclose(M, 5.92e24, rel_tol=2e-3)
