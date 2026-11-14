"""Verificación de fis2b-evau-madrid-2021-mod-b5 (tecnecio-99)."""

import math

NA, M, T = 6.02e23, 99.0, 6 * 3600
A = 10e6 * 70


def resolver() -> dict:
    lam = math.log(2) / T
    return {"constante": lam, "masa": A / lam / NA * M}


def comprobar(res: dict) -> None:
    N = res["masa"] / M * NA
    # Desintegraciones en un segundo.
    assert math.isclose(N * -math.expm1(-res["constante"]), A, rel_tol=1e-4)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["constante"], 3.21e-5, rel_tol=1e-3) and math.isclose(res["masa"], 3.59e-9, rel_tol=2e-3)
