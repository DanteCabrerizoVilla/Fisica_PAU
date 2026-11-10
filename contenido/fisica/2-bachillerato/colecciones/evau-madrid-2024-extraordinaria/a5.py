"""Verificación de fis2b-evau-madrid-2024-ext-a5 (tecnecio-99)."""

import math

# Datos del enunciado
T_semi = 6 * 3600.0
A0 = 5e8
A_final = 1e4
masa_molar = 98.9
N_A = 6.02e23


def resolver() -> dict:
    lam = math.log(2) / T_semi
    masa = A0 / lam / N_A * masa_molar
    return {"masa": masa, "tiempo": math.log(A0 / A_final) / lam}


def comprobar(res: dict) -> None:
    # Por periodos de semidesintegración: n = log2(A0/A).
    n = math.log2(A0 / A_final)
    assert math.isclose(res["tiempo"], n * T_semi, rel_tol=1e-12) and 15 < n < 16
    assert math.isclose(A0 * 0.5 ** (res["tiempo"] / T_semi), A_final, rel_tol=1e-9)
    # La masa hallada reproduce la actividad inicial.
    assert math.isclose(math.log(2) / T_semi * res["masa"] / masa_molar * N_A, A0, rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["masa"], 2.56e-9, rel_tol=2e-3) and math.isclose(res["tiempo"], 3.37e5, rel_tol=2e-3)
