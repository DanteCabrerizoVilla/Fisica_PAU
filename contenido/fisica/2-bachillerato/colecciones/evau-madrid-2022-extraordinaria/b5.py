"""Verificación de fis2b-evau-madrid-2022-ext-b5 (americio-241)."""

import math

NA, M = 6.02e23, 241.0
m0_mg, tau_anios = 0.2, 432.0
ANIO = 365 * 24 * 3600
queda = 0.2


def resolver() -> dict:
    N0 = m0_mg * 1e-3 / M * NA
    return {
        "periodo": tau_anios * math.log(2),
        "actividad": N0 / (tau_anios * ANIO),
        "masa": queda * m0_mg,
        "tiempo": -tau_anios * math.log(queda),
    }


def comprobar(res: dict) -> None:
    lam = 1 / tau_anios                       # años⁻¹
    # Tras un periodo queda la mitad.
    assert math.isclose(math.exp(-lam * res["periodo"]), 0.5, rel_tol=1e-12)
    # Segunda vía para el tiempo: en periodos, t = T½ · log2(1/0,2).
    assert math.isclose(res["tiempo"], res["periodo"] * math.log2(1 / queda), rel_tol=1e-12)
    # A ese tiempo la actividad y la masa son el 20 % de las iniciales.
    assert math.isclose(math.exp(-lam * res["tiempo"]), queda, rel_tol=1e-12)
    N = res["masa"] * 1e-3 / M * NA
    assert math.isclose(N / (tau_anios * ANIO), queda * res["actividad"], rel_tol=1e-12)
    # Tercera vía para la actividad: desintegraciones en un segundo.
    N0 = m0_mg * 1e-3 / M * NA
    assert math.isclose(N0 * -math.expm1(-1 / (tau_anios * ANIO)), res["actividad"], rel_tol=1e-6)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["periodo"], 299.44, rel_tol=1e-4)
    assert math.isclose(res["actividad"], 3.66e7, rel_tol=3e-3)
    assert math.isclose(res["tiempo"], 695.28, rel_tol=1e-4)
