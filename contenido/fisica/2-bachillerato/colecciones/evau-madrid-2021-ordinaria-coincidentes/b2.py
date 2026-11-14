"""Verificación de fis2b-evau-madrid-2021-ordc-b2 (número de fuentes y distancia al umbral)."""

import math

P, I0, b1 = 8e-6, 1e-12, 20.0


def resolver() -> dict:
    I1 = I0 * 10 ** (b1 / 10)
    n = I0 * 10 ** (2 * b1 / 10) / I1
    d1 = math.sqrt(P / (4 * math.pi * I1))
    d2 = math.sqrt(n * P / (4 * math.pi * I0))
    return {"n": n, "alejarse": d2 - d1}


def comprobar(res: dict) -> None:
    n = round(res["n"])
    I1 = I0 * 10 ** (b1 / 10)
    d1 = math.sqrt(P / (4 * math.pi * I1))
    nivel = lambda N, d: 10 * math.log10(N * P / (4 * math.pi * d**2) / I0)
    assert math.isclose(nivel(n, d1), 2 * b1, abs_tol=1e-9) and nivel(n - 1, d1) < 2 * b1
    assert math.isclose(nivel(n, d1 + res["alejarse"]), 0, abs_tol=1e-9)
    # Valores de la solución orientativa oficial.
    assert n == 100 and math.isclose(res["alejarse"], 7899.06, rel_tol=1e-5)
