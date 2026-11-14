"""Verificación de fis2b-evau-madrid-2021-ext-b2 (onda a partir de dos perfiles)."""

import math

A, k, fase = 0.1, 4 * math.pi, math.pi


def resolver() -> dict:
    w = (11 * math.pi - fase) / 2
    return {"w": w, "v": w / k, "a_max": A * w**2}


def comprobar(res: dict) -> None:
    w = res["w"]
    y = lambda x, t: A * math.cos(w * t - k * x + fase)
    for x in (0.0, 0.07, 0.31, 0.9):
        assert math.isclose(y(x, 0), A * math.cos(math.pi - 4 * math.pi * x), abs_tol=1e-12)
        assert math.isclose(y(x, 2), A * math.cos(11 * math.pi - 4 * math.pi * x), abs_tol=1e-12)
    # La ambigüedad: ω = π también reproduce las dos fotos.
    for x in (0.0, 0.07, 0.31):
        assert math.isclose(A * math.cos(math.pi * 2 - k * x + fase), A * math.cos(11 * math.pi - 4 * math.pi * x), abs_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(w, 5 * math.pi) and math.isclose(res["v"], 1.25) and math.isclose(res["a_max"], 24.674, rel_tol=1e-4)
