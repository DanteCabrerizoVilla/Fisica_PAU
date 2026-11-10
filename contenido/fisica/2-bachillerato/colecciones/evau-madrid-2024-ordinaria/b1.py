"""Verificación de fis2b-evau-madrid-2024-ord-b1 (¿órbita circular o elíptica?)."""

import math

# Datos del enunciado (SI)
G = 6.67e-11
M_T = 5.97e24
R_T = 6.37e6
m = 200.0
r = R_T + 630e3
v = 9.92e3


def resolver() -> dict:
    return {"v_circ": math.sqrt(G * M_T / r), "L": m * r * v, "a": G * M_T / r**2}


def comprobar(res: dict) -> None:
    v_escape = math.sqrt(2) * res["v_circ"]
    assert res["v_circ"] < v < v_escape, "debe ser más rápida que la circular y no llegar al escape"
    # Órbita ligada: energía mecánica negativa; el punto es el perigeo (r menor que el semieje).
    energia = 0.5 * v**2 - G * M_T / r
    a_semieje = -G * M_T / (2 * energia)
    assert energia < 0 and r < a_semieje
    # v²/r no es la aceleración aquí (error típico citado: 14,1 m/s²).
    assert math.isclose(v**2 / r, 14.1, rel_tol=5e-3) and v**2 / r > res["a"]
    # Valores de la solución orientativa oficial.
    for clave, oficial in (("v_circ", 7.54e3), ("L", 1.39e13), ("a", 8.13)):
        assert math.isclose(res[clave], oficial, rel_tol=2e-3), f"{clave} no coincide con la solución oficial"
