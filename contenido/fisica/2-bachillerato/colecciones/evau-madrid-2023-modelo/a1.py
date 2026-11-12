"""Verificación de fis2b-evau-madrid-2023-mod-a1 (satélite a 15 000 km)."""

import math

G, M, R = 6.67e-11, 5.97e24, 6.37e6
m, h = 400, 1.5e7


def resolver() -> dict:
    r = R + h
    v = math.sqrt(G * M / r)
    E_orbita = 0.5 * m * v**2 - G * M * m / r
    E_suelo = -G * M * m / R
    return {"dE": E_orbita - E_suelo, "T": 2 * math.pi * r / v, "E_escape": -E_orbita}


def comprobar(res: dict) -> None:
    r = R + h
    # Segunda vía para el periodo: tercera ley de Kepler.
    assert math.isclose(res["T"], 2 * math.pi * math.sqrt(r**3 / (G * M)), rel_tol=1e-12)
    # Segunda vía para las energías: expresiones cerradas.
    assert math.isclose(res["E_escape"], G * M * m / (2 * r), rel_tol=1e-12)
    assert math.isclose(res["dE"], G * M * m * (1 / R - 1 / (2 * r)), rel_tol=1e-12)
    # Poner en órbita y después escapar equivale a escapar desde el suelo.
    assert math.isclose(res["dE"] + res["E_escape"], G * M * m / R, rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["dE"], 2.127e10, rel_tol=2e-3)
    assert math.isclose(res["T"], 31105.45, rel_tol=1e-4)
    assert math.isclose(res["E_escape"], 3.73e9, rel_tol=2e-3)
