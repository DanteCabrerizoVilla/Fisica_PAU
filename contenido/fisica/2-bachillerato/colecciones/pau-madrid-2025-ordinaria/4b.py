"""Verificación de fis2b-pau-madrid-2025-ord-4b (datación con aluminio-26)."""

import math

# Datos del enunciado
T_semi_anios = 0.72e6
ANIO = 365 * 24 * 3600.0
proporcion_superficie = 0.1 / 100
proporcion_sedimento = 0.08 / 100
atomos_silicio = 8.3e22


def resolver() -> dict:
    lam = math.log(2) / (T_semi_anios * ANIO)
    actividad = lam * proporcion_superficie * atomos_silicio
    edad = -math.log(proporcion_sedimento / proporcion_superficie) / lam / ANIO
    return {"actividad": actividad, "edad": edad}


def comprobar(res: dict) -> None:
    # Tras el tiempo hallado queda el 80 % (por periodos de semidesintegración).
    assert math.isclose(0.5 ** (res["edad"] / T_semi_anios), 0.8, rel_tol=1e-12)
    # La actividad de la muestra enterrada habrá bajado en la misma proporción.
    lam = math.log(2) / (T_semi_anios * ANIO)
    assert math.isclose(lam * proporcion_sedimento * atomos_silicio, 0.8 * res["actividad"], rel_tol=1e-12)
    # Vía de la vida media, como en la solución oficial: t = tau · ln(N0/N).
    tau = T_semi_anios / math.log(2)
    assert math.isclose(res["edad"], tau * math.log(1.25), rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["actividad"], 2.53e6, rel_tol=2e-3) and math.isclose(res["edad"], 0.232e6, rel_tol=2e-3)
