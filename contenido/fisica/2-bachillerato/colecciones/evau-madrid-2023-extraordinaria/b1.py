"""Verificación de fis2b-evau-madrid-2023-ext-b1 (fuerza de un planeta y su satélite sobre una nave)."""

import math

# Datos del enunciado (SI)
G = 6.67e-11
M, M_sat = 4e23, 2e20
m = 8000.0
alfa = math.radians(53.13)
F = (9.5, -66.4)


def resolver() -> dict:
    R_sat = math.sqrt(G * M_sat * m * math.sin(alfa) / F[0])
    F_planeta = -F[1] - F[0] / math.tan(alfa)
    return {"R_sat": R_sat, "R_pla": math.sqrt(G * M * m / F_planeta)}


def comprobar(res: dict) -> None:
    # Reconstruir la fuerza total a partir de las posiciones halladas.
    planeta = (0.0, -res["R_pla"])
    satelite = (res["R_sat"] * math.sin(alfa), -res["R_sat"] * math.cos(alfa))
    fx = fy = 0.0
    for masa, (x, y) in ((M, planeta), (M_sat, satelite)):
        d = math.hypot(x, y)
        fx += G * masa * m * x / d**3
        fy += G * masa * m * y / d**3
    assert math.isclose(fx, F[0], rel_tol=1e-9) and math.isclose(fy, F[1], rel_tol=1e-9), (fx, fy)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["R_sat"], 3.00e6, rel_tol=2e-3) and math.isclose(res["R_pla"], 6.00e7, rel_tol=2e-3)
