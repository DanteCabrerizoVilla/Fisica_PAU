"""Verificación de fis2b-evau-madrid-2021-mod-a2 (potencia de una onda en una cuerda)."""

import math

A, w, k = 0.01, 20 * math.pi, 5 * math.pi
mu = 2e-3 / 1e-2          # 2 g/cm en kg/m


def resolver() -> dict:
    v = w / k
    P = 0.5 * mu * w**2 * A**2 * v
    return {"longitud": 2 * math.pi / k, "T": 2 * math.pi / w, "P": P, "E": 10 * P}


def comprobar(res: dict) -> None:
    # Segunda vía: energía media por unidad de longitud (½ μ ω² A²) que avanza a velocidad v.
    densidad = 0.5 * mu * w**2 * A**2
    assert math.isclose(densidad * res["longitud"] / res["T"], res["P"], rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["P"], 0.158, rel_tol=2e-3) and math.isclose(res["E"], 1.58, rel_tol=2e-3)
