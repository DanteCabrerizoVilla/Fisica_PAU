"""Verificación de fis2b-evau-madrid-2023-mod-a2 (onda hacia −x con y = 0 y velocidad negativa)."""

import math

v, longitud = 2.0, 0.5
vy0 = -0.4 * math.pi      # m/s


def resolver() -> dict:
    f = v / longitud
    w = 2 * math.pi * f
    return {"A": abs(vy0) / w, "f": f}


def comprobar(res: dict) -> None:
    A, f = res["A"], res["f"]
    w, k, fase = 2 * math.pi * f, 2 * math.pi / longitud, math.pi
    y = lambda x, t: A * math.sin(w * t + k * x + fase)
    # Derivada numérica de la elongación: velocidad de oscilación.
    dt = 1e-8
    vy = (y(0, dt) - y(0, -dt)) / (2 * dt)
    assert abs(y(0, 0)) < 1e-12 and math.isclose(vy, vy0, rel_tol=1e-6)
    # Puntos separados una longitud de onda oscilan en fase.
    for t in (0.03, 0.11):
        assert math.isclose(y(0.2, t), y(0.2 + longitud, t), abs_tol=1e-12)
    # Viaja hacia las x negativas: el perfil se repite desplazado −v·Δt.
    assert math.isclose(y(0.3, 0.0), y(0.3 - v * 0.05, 0.05), abs_tol=1e-12)
    # La otra fase posible (0) daría velocidad positiva.
    assert A * w * math.cos(0) > 0
    # Valores de la solución orientativa oficial: 5 cm y 4 Hz.
    assert math.isclose(A, 0.05, rel_tol=1e-12) and math.isclose(f, 4, rel_tol=1e-12)
