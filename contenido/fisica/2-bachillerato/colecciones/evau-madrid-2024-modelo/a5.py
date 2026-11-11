"""Verificación de fis2b-evau-madrid-2024-mod-a5 (oro-198)."""

import math

# Datos del enunciado
DIA = 86400.0
fraccion, t_fraccion = 1 / 6, 7.0      # días
A_1dia = 10e3                           # Bq


def resolver() -> dict:
    lam_dia = -math.log(fraccion) / t_fraccion
    lam = lam_dia / DIA
    A0 = A_1dia * math.exp(lam_dia * 1.0)
    return {"constante": lam, "periodo": math.log(2) / lam_dia, "actividad": A0, "nucleos": A0 / lam}


def comprobar(res: dict) -> None:
    T = res["periodo"]
    # A la semana queda la sexta parte; al día, 10 kBq.
    assert math.isclose(0.5 ** (7 / T), 1 / 6, rel_tol=1e-12)
    assert math.isclose(res["actividad"] * 0.5 ** (1 / T), A_1dia, rel_tol=1e-12)
    assert math.isclose(7 / T, math.log2(6), rel_tol=1e-12)
    # Valores de la solución orientativa oficial (dos cifras).
    assert math.isclose(res["constante"], 3.0e-6, rel_tol=2e-2) and math.isclose(res["periodo"], 2.7, rel_tol=1e-2)
    assert math.isclose(res["actividad"], 13e3, rel_tol=1e-2) and math.isclose(res["nucleos"], 4.3e9, rel_tol=2e-2)
