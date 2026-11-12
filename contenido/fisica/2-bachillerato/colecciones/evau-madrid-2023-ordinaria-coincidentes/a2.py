"""Verificación de fis2b-evau-madrid-2023-ordc-a2 (onda a partir de la oscilación de un punto)."""

import math

v = 20.0
A, w = 0.025, 10 * math.pi
x_dato = 0.5


def resolver() -> dict:
    longitud = 2 * math.pi * v / w
    k = 2 * math.pi / longitud
    return {"longitud": longitud, "fase": k * x_dato, "v_max": A * w, "a_max": A * w**2}


def comprobar(res: dict) -> None:
    k = 2 * math.pi / res["longitud"]
    y_cos = lambda x, t: A * math.cos(w * t - k * x + res["fase"])
    y_sen = lambda x, t: A * math.sin(w * t - k * x + 3 * math.pi / 4)
    for t in (0.0, 0.013, 0.07, 0.151):
        # En x = 0,5 m se recupera la ley del enunciado, con coseno y con seno.
        assert math.isclose(y_cos(x_dato, t), A * math.cos(w * t), abs_tol=1e-12)
        assert math.isclose(y_sen(x_dato, t), A * math.cos(w * t), abs_tol=1e-12)
        # Avanza hacia +x a 20 m/s.
        assert math.isclose(y_cos(1.0, t), y_cos(1.0 + v * 0.01, t + 0.01), abs_tol=1e-12)
    # Máximos de velocidad y aceleración, por muestreo de las derivadas numéricas.
    dt, n = 1e-6, 4000
    vs = [(y_cos(0.3, i * 0.2 / n + dt) - y_cos(0.3, i * 0.2 / n - dt)) / (2 * dt) for i in range(n)]
    acs = [(y_cos(0.3, i * 0.2 / n + dt) - 2 * y_cos(0.3, i * 0.2 / n) + y_cos(0.3, i * 0.2 / n - dt)) / dt**2 for i in range(n)]
    assert math.isclose(max(vs), res["v_max"], rel_tol=1e-5)
    assert math.isclose(max(acs), res["a_max"], rel_tol=1e-3)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["longitud"], 4) and math.isclose(res["fase"], math.pi / 4)
    assert math.isclose(res["v_max"], 0.79, rel_tol=1e-2) and math.isclose(res["a_max"], 24.67, rel_tol=1e-3)
