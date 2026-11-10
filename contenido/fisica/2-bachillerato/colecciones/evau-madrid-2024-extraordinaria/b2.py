"""Verificación de fis2b-evau-madrid-2024-ext-b2 (onda hacia −x a partir de su perfil)."""

import math

# Lecturas de la gráfica y dato del enunciado
A = 3.0            # cm
longitud = 1.5     # m
T = 0.5            # s


def y(x: float, t: float) -> float:
    return A * math.sin(2 * math.pi / T * t + 2 * math.pi / longitud * x + math.pi / 2)


def resolver() -> dict:
    return {"longitud": longitud, "v": longitud / T}


def comprobar(res: dict) -> None:
    # Perfil en t = 0.
    for x, valor in ((0, 3), (0.375, 0), (0.75, -3), (1.125, 0), (1.5, 3), (2.0, -1.5)):
        assert math.isclose(y(x, 0), valor, abs_tol=1e-9), f"el perfil no pasa por x = {x}"
    # El punto x = 0 vuelve a +A a los 0,5 s y no antes.
    assert math.isclose(y(0, 0.5), 3, abs_tol=1e-9) and y(0, 0.25) < 0
    # Se propaga hacia −x: el perfil se desplaza −v·dt.
    v = res["v"]
    assert math.isclose(y(1.0 - v * 0.07, 0.07), y(1.0, 0), abs_tol=1e-9)
    # Forma con coseno.
    assert math.isclose(y(0.4, 0.13), A * math.cos(4 * math.pi * 0.13 + 4 * math.pi / 3 * 0.4), abs_tol=1e-9)
