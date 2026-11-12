"""Verificación de fis2b-evau-madrid-2023-ord-a5 (radón en un acuífero)."""

import math

# Datos del enunciado
A0 = 14.0                  # Bq por litro
T_dias = 3.8
DIA = 86400.0
masa_aporte = 2e-16        # g por litro
M = 222.0
N_A = 6.02e23
semana, dias_restantes = 7.0, 3.0


def resolver() -> dict:
    lam = math.log(2) / (T_dias * DIA)
    sin_aporte = A0 * math.exp(-lam * semana * DIA)
    aporte = lam * masa_aporte / M * N_A * math.exp(-lam * dias_restantes * DIA)
    return {"A_sin": sin_aporte, "A_con": sin_aporte + aporte}


def comprobar(res: dict) -> None:
    # Segunda vía: seguir el número de núcleos día a día.
    lam_dia = math.log(2) / T_dias
    lam = lam_dia / DIA
    N = A0 / lam
    for dia in range(1, 8):
        N *= math.exp(-lam_dia)
        if dia == 4:
            N += masa_aporte / M * N_A
    assert math.isclose(lam * N, res["A_con"], rel_tol=1e-10), f"día a día: {lam * N}"
    assert math.isclose((res["A_con"] - res["A_sin"]) / res["A_sin"], 0.17, abs_tol=0.005)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["A_sin"], 3.90, rel_tol=2e-3) and math.isclose(res["A_con"], 4.56, rel_tol=3e-3)
