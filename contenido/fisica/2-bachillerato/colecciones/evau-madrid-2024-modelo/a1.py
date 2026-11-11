"""Verificación de fis2b-evau-madrid-2024-mod-a1 (sonda Parker)."""

import math

# Datos del enunciado (SI)
G = 6.67e-11
M_S = 1.99e30
r_a = 1.1e8 * 1e3
r_p = 7.6e6 * 1e3


def resolver() -> dict:
    a = (r_a + r_p) / 2
    T = 2 * math.pi * math.sqrt(a**3 / (G * M_S))
    v_p = math.sqrt(2 * G * M_S * r_a / (r_p * (r_a + r_p)))
    return {"a": a, "T": T, "v_a": v_p * r_p / r_a, "v_p": v_p}


def comprobar(res: dict) -> None:
    a = res["a"]
    # Vis-viva en los dos puntos.
    assert math.isclose(res["v_p"], math.sqrt(G * M_S * (2 / r_p - 1 / a)), rel_tol=1e-12)
    assert math.isclose(res["v_a"], math.sqrt(G * M_S * (2 / r_a - 1 / a)), rel_tol=1e-12)
    # Energía mecánica por kg igual a −GM/(2a).
    assert math.isclose(0.5 * res["v_a"] ** 2 - G * M_S / r_a, -G * M_S / (2 * a), rel_tol=1e-10)
    # Valores de la solución orientativa oficial (redondea a a 5,9e10).
    for clave, oficial, tol in (("a", 5.9e10, 5e-3), ("T", 7.82e6, 6e-3), ("v_p", 1.81e5, 3e-3), ("v_a", 1.25e4, 3e-3)):
        assert math.isclose(res[clave], oficial, rel_tol=tol), f"{clave} no coincide con la solución oficial"
