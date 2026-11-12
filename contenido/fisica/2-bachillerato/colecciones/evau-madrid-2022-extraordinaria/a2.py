"""Verificación de fis2b-evau-madrid-2022-ext-a2 (onda a partir de dos gráficas)."""

import math

A, T, longitud = 0.03, 1.0, 0.04      # SI
x_p, t_p = 0.03, 1.0


def resolver() -> dict:
    w, k = 2 * math.pi / T, 2 * math.pi / longitud
    v_osc = -A * w * math.sin(w * t_p - k * x_p + math.pi)
    return {"v": longitud / T, "v_osc": v_osc}


def comprobar(res: dict) -> None:
    w, k = 2 * math.pi / T, 2 * math.pi / longitud
    y = lambda x, t: A * math.cos(w * t - k * x + math.pi)
    # Puntos leídos de las dos gráficas del enunciado.
    for x_cm, y_cm in ((0, -3), (1, 0), (2, 3), (3, 0), (4, -3), (6, 3)):
        assert math.isclose(y(x_cm / 100, 0), y_cm / 100, abs_tol=1e-12)
    for t, y_cm in ((0, -3), (0.25, 0), (0.5, 3), (1, -3)):
        assert math.isclose(y(0, t), y_cm / 100, abs_tol=1e-12)
    # La versión con seno es la misma onda.
    for x, t in ((0.013, 0.4), (0.03, 1.0)):
        assert math.isclose(A * math.sin(w * t - k * x + 1.5 * math.pi), y(x, t), abs_tol=1e-12)
    # Velocidad de oscilación por derivada numérica; coincide con la máxima.
    dt = 1e-7
    assert math.isclose((y(x_p, t_p + dt) - y(x_p, t_p - dt)) / (2 * dt), res["v_osc"], rel_tol=1e-6)
    assert math.isclose(res["v_osc"], A * w, rel_tol=1e-12)
    # Avanza hacia +x.
    assert math.isclose(y(0.01, 0.2), y(0.01 + res["v"] * 0.1, 0.3), abs_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["v"], 0.04) and math.isclose(res["v_osc"], 0.1885, rel_tol=1e-3)
