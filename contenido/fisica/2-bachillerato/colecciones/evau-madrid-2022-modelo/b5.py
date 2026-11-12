"""Verificación de fis2b-evau-madrid-2022-mod-b5 (datación con carbono-14)."""

import math

NA, MC = 6.02e23, 12.0
masa, proporcion = 25.0, 1.3e-12
T_anios = 5730.0
ANIO = 365 * 86400
A_actual = 5.2


def resolver() -> dict:
    N0 = masa / MC * NA * proporcion
    lam = math.log(2) / (T_anios * ANIO)
    A0 = lam * N0
    return {"actividad": A0, "tiempo": T_anios / math.log(2) * math.log(A0 / A_actual)}


def comprobar(res: dict) -> None:
    lam = math.log(2) / T_anios                       # años⁻¹
    # A ese tiempo, la actividad ha bajado a 5,2 Bq.
    assert math.isclose(res["actividad"] * math.exp(-lam * res["tiempo"]), A_actual, rel_tol=1e-12)
    # Segunda vía: en periodos, t = T½ · log2(A0/A).
    assert math.isclose(res["tiempo"], T_anios * math.log2(res["actividad"] / A_actual), rel_tol=1e-12)
    assert 0 < res["tiempo"] < T_anios
    # Tercera vía para la actividad: desintegraciones en un segundo.
    N0 = masa / MC * NA * proporcion
    assert math.isclose(N0 * -math.expm1(-math.log(2) / (T_anios * ANIO)), res["actividad"], rel_tol=1e-6)
    # Con año de 365,25 días el resultado apenas cambia.
    A0_bis = math.log(2) / (T_anios * 365.25 * 86400) * N0
    assert math.isclose(T_anios * math.log2(A0_bis / A_actual), res["tiempo"], rel_tol=5e-3)
    # Solución orientativa oficial: 6,28 Bq y 1562 años, con redondeos intermedios.
    assert math.isclose(res["actividad"], 6.28, rel_tol=5e-3)
    assert math.isclose(res["tiempo"], 1562, rel_tol=0.03)
