"""Verificación de fis2b-pau-madrid-2027-mod-4a (desintegración del cobalto-60)."""

import math

# Datos del enunciado
T_semi_dias = 1925.2
masa_molar = 59.94          # g/mol
A0 = 2.64e9                 # Bq
N_A = 6.02e23
DIA = 86400.0
t_dias = 365.0


def resolver() -> dict:
    lam = math.log(2) / (T_semi_dias * DIA)       # s⁻¹
    N0 = A0 / lam
    masa = N0 / N_A * masa_molar                  # g
    actividad = A0 * math.exp(-lam * t_dias * DIA)
    return {"constante": lam, "masa": masa, "actividad": actividad}


def comprobar(res: dict) -> None:
    # Actividad por otra vía: fracción 1/2 elevada al número de periodos transcurridos.
    por_periodos = A0 * 0.5 ** (t_dias / T_semi_dias)
    assert math.isclose(res["actividad"], por_periodos, rel_tol=1e-12), "la actividad no coincide"
    # Tras un periodo de semidesintegración debe quedar la mitad.
    assert math.isclose(math.exp(-res["constante"] * T_semi_dias * DIA), 0.5, rel_tol=1e-12)
    # La masa hallada reproduce la actividad inicial.
    N0 = res["masa"] / masa_molar * N_A
    assert math.isclose(res["constante"] * N0, A0, rel_tol=1e-12), "la masa no da la actividad inicial"
    # Valores de la solución orientativa oficial.
    for clave, oficial in (("constante", 4.17e-9), ("masa", 6.3e-5), ("actividad", 2.31e9)):
        assert math.isclose(res[clave], oficial, rel_tol=5e-3), f"{clave} no coincide con la solución oficial"
