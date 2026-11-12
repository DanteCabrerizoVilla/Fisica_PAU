"""Verificación de fis2b-evau-madrid-2023-mod-b2 (foco sonoro, dos niveles)."""

import math

import numpy as np

I0 = 1e-12
b1, b2, separacion = 60.0, 47.96, 10.0


def resolver() -> dict:
    I1, I2 = I0 * 10 ** (b1 / 10), I0 * 10 ** (b2 / 10)
    x = separacion / (math.sqrt(I1 / I2) - 1)
    return {"x": x, "P": I1 * 4 * math.pi * x**2}


def comprobar(res: dict) -> None:
    x, P = res["x"], res["P"]
    nivel = lambda r: 10 * math.log10(P / (4 * math.pi * r**2) / I0)
    # Con la potencia y la distancia obtenidas se recuperan los dos niveles del enunciado.
    assert math.isclose(nivel(x), b1, abs_tol=1e-9)
    assert math.isclose(nivel(x + separacion), b2, abs_tol=1e-9)
    # Segunda vía: la ecuación de segundo grado de la solución oficial.
    k = 10 ** ((b1 - b2) / 10)
    raices = np.roots([k - 1, -2 * separacion, -separacion**2])
    positivas = [r for r in raices if r > 0]
    assert len(positivas) == 1 and math.isclose(positivas[0], x, rel_tol=1e-9)
    assert math.isclose(min(raices), -2, abs_tol=2e-3)
    # Valores de la solución orientativa oficial.
    assert math.isclose(x, 10 / 3, rel_tol=1e-3)
    assert math.isclose(P, 1.39e-4, rel_tol=6e-3)
