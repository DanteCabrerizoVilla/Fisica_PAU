"""Verificación de fis2b-evau-madrid-2021-ext-b5 (platino-190 en el patrón del kilogramo)."""

import math

NA, M = 6.02e23, 189.96
T_anios, t_anios = 6.5e11, 1e9
ANIO = 365 * 24 * 3600


def resolver() -> dict:
    m0 = 1.0 * 0.9 * 0.012e-2                     # kg
    N0 = m0 * 1e3 / M * NA
    lam = math.log(2) / (T_anios * ANIO)
    return {"A": lam * N0, "m": m0 * math.exp(-math.log(2) * t_anios / T_anios)}


def comprobar(res: dict) -> None:
    m0 = 0.9 * 0.012e-2
    # Segunda vía: en periodos, m = m0 · 2^(−t/T).
    assert math.isclose(res["m"], m0 * 2 ** (-t_anios / T_anios), rel_tol=1e-12)
    assert 0.998 < res["m"] / m0 < 1
    # Valores de la solución orientativa oficial (que trunca la masa a 1,07e-4).
    assert math.isclose(res["A"], 11.57, rel_tol=1e-3) and math.isclose(res["m"], 107.885e-6, rel_tol=1e-5)
