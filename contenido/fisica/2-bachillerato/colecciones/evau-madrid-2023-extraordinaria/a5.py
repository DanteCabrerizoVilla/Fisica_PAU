"""Verificación de fis2b-evau-madrid-2023-ext-a5 (derrame de flúor-18)."""

import math

# Datos del enunciado
tau = 109.7 * 60       # s
A0, A = 18.5e6, 37e3   # Bq
M_F = 18.0
N_A = 6.02e23


def resolver() -> dict:
    N0 = A0 * tau
    return {"masa": N0 / N_A * M_F, "tiempo": tau * math.log(A0 / A)}


def comprobar(res: dict) -> None:
    # Con el periodo de semidesintegración T = tau·ln 2 se obtiene el mismo tiempo.
    T = tau * math.log(2)
    assert math.isclose(A0 * 0.5 ** (res["tiempo"] / T), A, rel_tol=1e-10)
    assert math.isclose(T / 60, 76.0, rel_tol=2e-3), "el periodo del F-18 debe salir de unos 76 minutos"
    # La masa hallada reproduce la actividad inicial.
    assert math.isclose(res["masa"] / M_F * N_A / tau, A0, rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["masa"], 3.65e-12, rel_tol=4e-3) and math.isclose(res["tiempo"], 4.09e4, rel_tol=2e-3)
