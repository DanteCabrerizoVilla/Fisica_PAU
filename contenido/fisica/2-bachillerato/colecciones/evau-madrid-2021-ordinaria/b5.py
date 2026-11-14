"""Verificación de fis2b-evau-madrid-2021-ord-b5 (vida media, actividad y décima parte)."""

import math

T_anios, N0 = 5730.0, 5e20
ANIO = 365 * 86400


def resolver() -> dict:
    tau = T_anios / math.log(2)
    lam = 1 / (tau * ANIO)
    return {"tau": tau, "constante": lam, "A0": lam * N0, "tiempo": tau * math.log(10)}


def comprobar(res: dict) -> None:
    # Segunda vía: en periodos, t = T½·log2(10).
    assert math.isclose(res["tiempo"], T_anios * math.log2(10), rel_tol=1e-12)
    assert math.isclose(math.exp(-res["tiempo"] / res["tau"]), 0.1, rel_tol=1e-12)
    # Desintegraciones en un segundo.
    assert math.isclose(N0 * -math.expm1(-res["constante"]), res["A0"], rel_tol=1e-6)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["tau"], 8266.64, rel_tol=1e-5) and math.isclose(res["constante"], 3.84e-12, rel_tol=2e-3)
    assert math.isclose(res["A0"], 1.92e9, rel_tol=2e-3) and math.isclose(res["tiempo"], 19000, rel_tol=2e-3)
