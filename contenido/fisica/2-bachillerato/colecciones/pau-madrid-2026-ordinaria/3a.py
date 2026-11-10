"""Verificación de fis2b-pau-madrid-2026-ord-3a (onda: perfil y velocidad de oscilación)."""

import math

# Lecturas de las gráficas (SI)
A = 0.04
longitud = 6.0
T = 4.0
fase = 0.0


def y(x: float, t: float) -> float:
    return A * math.sin(2 * math.pi / T * t - 2 * math.pi / longitud * x + fase)


def v_osc(x: float, t: float, h: float = 1e-6) -> float:
    return (y(x, t + h) - y(x, t - h)) / (2 * h)


def resolver() -> dict:
    return {"A": A, "k": 2 * math.pi / longitud, "fase": fase,
            "v_max": A * 2 * math.pi / T, "v": longitud / T}


def comprobar(res: dict) -> None:
    # Figura (a): perfil en t = 0.
    for x, valor in ((0, 0), (1.5, -0.04), (3, 0), (4.5, 0.04), (7.5, -0.04), (10.5, 0.04)):
        assert math.isclose(y(x, 0), valor, abs_tol=1e-9), f"el perfil no pasa por x = {x}"
    # Figura (b): velocidad en x = 0 (derivada numérica).
    for t, valor in ((0, res["v_max"]), (1, 0), (2, -res["v_max"]), (4, res["v_max"]), (8, res["v_max"])):
        assert math.isclose(v_osc(0, t), valor, abs_tol=1e-7), f"la velocidad no coincide en t = {t}"
    # Con fase π la velocidad inicial sería negativa.
    assert A * 2 * math.pi / T * math.cos(math.pi) < 0
    # La onda viaja hacia +x a la velocidad calculada.
    assert math.isclose(y(2 + res["v"] * 0.7, 0.7), y(2, 0), abs_tol=1e-12)
    # Valor de la solución orientativa oficial.
    assert math.isclose(res["v_max"], 6.28e-2, rel_tol=1e-3)
