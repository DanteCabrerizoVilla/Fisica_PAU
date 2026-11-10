"""Verificación de fis2b-pau-madrid-2025-ord-3a (sonido de una ballena)."""

import math

# Datos del enunciado (SI)
f = 60.0
longitud = 25.0
t = 80e-3
D = 300.0
I_A = 3e-6
I_0 = 1e-12


def resolver() -> dict:
    h = longitud * f * t
    P = 4 * math.pi * h**2 * I_A
    d = math.hypot(D, h)
    I_B = P / (4 * math.pi * d**2)
    return {"h": h, "P": P, "nivel": 10 * math.log10(I_B / I_0)}


def comprobar(res: dict) -> None:
    h = res["h"]
    # Segunda vía: diferencia de niveles entre A y B, 20·log(d/h).
    nivel_A = 10 * math.log10(I_A / I_0)
    d = math.hypot(D, h)
    assert math.isclose(res["nivel"], nivel_A - 20 * math.log10(d / h), rel_tol=1e-12)
    assert math.isclose(nivel_A, 64.8, rel_tol=1e-3) and math.isclose(nivel_A - res["nivel"], 8.6, rel_tol=1e-2)
    # La velocidad obtenida es la del sonido en el agua (unos 1500 m/s).
    assert math.isclose(longitud * f, 1500, rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    for clave, oficial in (("h", 120), ("P", 0.543), ("nivel", 56.17)):
        assert math.isclose(res[clave], oficial, rel_tol=1e-3), f"{clave} no coincide con la solución oficial"
