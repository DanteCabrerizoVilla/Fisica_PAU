"""Verificación de fis2b-evau-madrid-2021-ord-b2 (onda electromagnética en un medio)."""

import math

w, k, c = 3.43e15, 1.52e7, 3e8


def resolver() -> dict:
    v = w / k
    return {"f": w / (2 * math.pi), "longitud": 2 * math.pi / k, "v": v, "n": c / v}


def comprobar(res: dict) -> None:
    assert math.isclose(res["longitud"] * res["f"], res["v"], rel_tol=1e-12)
    # La longitud de onda en el vacío es n veces la del medio.
    assert math.isclose(c / res["f"], res["n"] * res["longitud"], rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["f"], 5.46e14, rel_tol=1e-3) and math.isclose(res["longitud"], 4.13e-7, rel_tol=1e-3)
    assert math.isclose(res["v"], 2.26e8, rel_tol=2e-3) and math.isclose(res["n"], 1.33, rel_tol=2e-3)
