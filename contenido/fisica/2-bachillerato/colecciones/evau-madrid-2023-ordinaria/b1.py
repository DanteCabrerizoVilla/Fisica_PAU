"""Verificación de fis2b-evau-madrid-2023-ord-b1 (satélite y punto de equilibrio Tierra-Luna)."""

import math

# Datos del enunciado (SI)
G = 6.67e-11
M_T, M_L = 5.97e24, 7.35e22
R_T = 6.37e6
d = 3.84e8
r = R_T + 1600e3


def resolver() -> dict:
    v = math.sqrt(G * M_T / r)
    k = math.sqrt(M_T / M_L)
    return {"v": v, "T": 2 * math.pi * r / v, "x": d * k / (1 + k)}


def comprobar(res: dict) -> None:
    x = res["x"]
    g_tierra = lambda p: G * M_T / p**2
    g_luna = lambda p: G * M_L / (d - p) ** 2
    assert math.isclose(g_tierra(x), g_luna(x), rel_tol=1e-12)
    assert g_tierra(x - 1e6) > g_luna(x - 1e6) and g_tierra(x + 1e6) < g_luna(x + 1e6)
    # Periodo por la tercera ley de Kepler.
    assert math.isclose(res["T"], 2 * math.pi * math.sqrt(r**3 / (G * M_T)), rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    for clave, oficial in (("v", 7.07e3), ("T", 7083), ("x", 3.46e8)):
        assert math.isclose(res[clave], oficial, rel_tol=2e-3), f"{clave} no coincide con la solución oficial"
