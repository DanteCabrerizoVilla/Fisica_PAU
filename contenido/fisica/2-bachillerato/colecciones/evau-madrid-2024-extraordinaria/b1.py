"""Verificación de fis2b-evau-madrid-2024-ext-b1 (dos planetas en torno a una estrella)."""

import math

# Datos del enunciado (SI)
G = 6.67e-11
ANIO = 365 * 86400.0
r1 = 1.2e11
T1 = 3 * ANIO
r_p, r_a = 1.0e11, 1.8e11
E_m = -3.8e30


def resolver() -> dict:
    M = 4 * math.pi**2 * r1**3 / (G * T1**2)
    a2 = (r_p + r_a) / 2
    T2 = 2 * math.pi * math.sqrt(a2**3 / (G * M))
    v1 = 2 * math.pi * r1 / T1
    return {"M": M, "T2": T2, "v1": v1, "m": -2 * E_m / v1**2}


def comprobar(res: dict) -> None:
    M, m = res["M"], res["m"]
    # Kepler comparando planetas: T2 = T1 (a2/r1)^1.5 = 3,78 años.
    assert math.isclose(res["T2"] / ANIO, 3 * (1.4 / 1.2) ** 1.5, rel_tol=1e-12)
    # Velocidad orbital por la dinámica.
    assert math.isclose(res["v1"], math.sqrt(G * M / r1), rel_tol=1e-12)
    # Masa por la otra expresión de la energía mecánica.
    assert math.isclose(m, -2 * r1 * E_m / (G * M), rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    for clave, oficial, tol in (("M", 1.14e29, 3e-3), ("T2", 1.19e8, 3e-3), ("v1", 7.97e3, 2e-3), ("m", 1.2e23, 5e-3)):
        assert math.isclose(res[clave], oficial, rel_tol=tol), f"{clave} no coincide con la solución oficial"
