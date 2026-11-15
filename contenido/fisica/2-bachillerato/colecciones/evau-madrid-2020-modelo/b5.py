"""Verificación de fis2b-evau-madrid-2020-mod-b5 (isótopo con vida media de 6 h)."""

import math

tau, m0, M, NA, t = 6 * 3600, 1e-3, 98.90, 6.02e23, 24 * 3600


def resolver() -> dict:
    lam = 1 / tau
    m = m0 * math.exp(-lam * t)
    return {"T": tau * math.log(2), "m": m, "A": lam * m / M * NA}


def comprobar(res: dict) -> None:
    # Por periodos de semidesintegración: m = m0 · (1/2)^(t/T).
    assert math.isclose(m0 * 0.5 ** (t / res["T"]), res["m"], rel_tol=1e-12)
    # Actividad como derivada numérica del número de núcleos.
    N = lambda s: m0 * math.exp(-s / tau) / M * NA
    dt = 1.0
    assert math.isclose(-(N(t + dt) - N(t - dt)) / (2 * dt), res["A"], rel_tol=1e-8)
    # Oficial: T = 1,5·10⁴ s, m = 1,83·10⁻⁵ g, A = 5,16·10¹² Bq.
    assert math.isclose(res["m"], 1.83e-5, rel_tol=1e-3) and math.isclose(res["A"], 5.16e12, rel_tol=1e-3)
