"""Verificación de fis2b-pau-madrid-2025-mod-4b (uvas con torio-231)."""

import math

# Datos del enunciado
T_semi = 25.5 * 3600       # s
masa_uva = 1.50e-12        # g
masa_molar = 231.0         # g/mol
N_A = 6.02e23
t = 8 * 3600.0
actividad_medida = 1.19e6


def _uvas_sin_redondear() -> float:
    lam = math.log(2) / T_semi
    A0 = lam * masa_uva / masa_molar * N_A
    return actividad_medida / (A0 * math.exp(-lam * t))


def resolver() -> dict:
    lam = math.log(2) / T_semi
    A0 = lam * masa_uva / masa_molar * N_A
    # El número de uvas es entero: se redondea el cociente.
    return {"vida_media": 1 / lam, "actividad": A0, "uvas": round(_uvas_sin_redondear())}


def comprobar(res: dict) -> None:
    n = _uvas_sin_redondear()
    assert abs(n - res["uvas"]) < 0.3, f"el cociente ({n:.2f}) no está cerca de un entero"
    # Con 50 uvas, la actividad a las 8 horas es la medida (dentro del redondeo de los datos).
    restante = 0.5 ** (t / T_semi)
    assert math.isclose(res["uvas"] * res["actividad"] * restante, actividad_medida, rel_tol=5e-3)
    # Sin el decaimiento saldrían unas 40 uvas (error típico citado).
    assert round(actividad_medida / res["actividad"]) == 40
    # Vida media mayor que el periodo: tau = T / ln 2 = 36,8 h.
    assert math.isclose(res["vida_media"] / 3600, 36.8, rel_tol=2e-3)
    # Valores de la solución orientativa oficial (usa 25,52 h).
    assert math.isclose(res["vida_media"], 1.33e5, rel_tol=5e-3) and math.isclose(res["actividad"], 2.95e4, rel_tol=2e-3)
