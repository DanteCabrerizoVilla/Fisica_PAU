"""Verificación del problema de muestra 1: satélite en órbita circular."""

import math

# Datos del enunciado (SI)
G = 6.67e-11
M_T = 5.97e24
R_T = 6.37e6
m = 1200
h = 600e3


def resolver() -> dict:
    r = R_T + h
    v = math.sqrt(G * M_T / r)
    T = 2 * math.pi * r / v
    E_m = 0.5 * m * v**2 - G * M_T * m / r
    return {"v": v, "T": T, "E_escape": -E_m}


def comprobar(res: dict) -> None:
    r = R_T + h
    # Periodo por la tercera ley de Kepler.
    T_kepler = math.sqrt(4 * math.pi**2 * r**3 / (G * M_T))
    assert math.isclose(res["T"], T_kepler, rel_tol=1e-9), "el periodo no cumple la tercera ley de Kepler"
    # Energía de escape por otra vía: cinética con velocidad de escape menos la que ya tiene.
    v_escape = math.sqrt(2 * G * M_T / r)
    por_velocidades = 0.5 * m * (v_escape**2 - res["v"] ** 2)
    assert math.isclose(res["E_escape"], por_velocidades, rel_tol=1e-9), "la energía de escape no coincide"
