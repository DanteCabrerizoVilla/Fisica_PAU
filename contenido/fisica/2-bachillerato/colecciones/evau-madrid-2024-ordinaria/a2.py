"""Verificación de fis2b-evau-madrid-2024-ord-a2 (fase inicial de una onda en una cuerda)."""

import math

# Datos del enunciado (SI)
v = 200.0
longitud = 0.4


def resolver() -> dict:
    return {"k": 2 * math.pi / longitud, "f": v / longitud, "fase": math.pi / 3}


def comprobar(res: dict) -> None:
    w = 2 * math.pi * res["f"]
    k, fase = res["k"], res["fase"]
    A = 1.0

    def y(x, t, f0=fase):
        return A * math.sin(w * t - k * x + f0)

    def vy(x, t, f0=fase, h=1e-9):
        return (y(x, t + h, f0) - y(x, t - h, f0)) / (2 * h)

    # Condiciones del enunciado.
    assert y(0, 0) > 0
    assert math.isclose(vy(0, 0), 0.5 * A * w, rel_tol=1e-5)
    # La otra raíz del coseno no cumple el signo de la elongación.
    assert y(0, 0, -math.pi / 3) < 0
    # Equivalencia con la forma coseno y fase −π/6.
    for x, t in ((0.13, 2.1e-4), (0.31, 1.7e-3)):
        assert math.isclose(y(x, t), A * math.cos(w * t - k * x - math.pi / 6), abs_tol=1e-9)
    # Se propaga hacia +x a 200 m/s.
    assert math.isclose(y(0.1 + v * 1e-4, 1e-4), y(0.1, 0), abs_tol=1e-9)
