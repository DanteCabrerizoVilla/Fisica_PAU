"""Verificación de fis2b-evau-madrid-2023-ord-a2 (fase con condiciones fuera del origen)."""

import math

# Datos del enunciado (SI)
T = 4e-3
A = 3e-3
longitud = 0.25


def resolver() -> dict:
    return {"w": 2 * math.pi / T, "v": longitud / T}


def comprobar(res: dict) -> None:
    w, k = res["w"], 2 * math.pi / longitud

    def y(x, t, fase=5 * math.pi / 6):
        return A * math.sin(w * t - k * x + fase)

    h = 1e-9
    # Condiciones del enunciado en x = 0,5 m, t = 2 ms.
    assert math.isclose(y(0.5, 2e-3), -1.5e-3, rel_tol=1e-9)
    assert y(0.5, 2e-3 + h) - y(0.5, 2e-3 - h) > 0
    # La otra fase cumple la elongación pero no la velocidad.
    assert math.isclose(y(0.5, 2e-3, math.pi / 6), -1.5e-3, rel_tol=1e-9)
    assert y(0.5, 2e-3 + h, math.pi / 6) - y(0.5, 2e-3 - h, math.pi / 6) < 0
    # Forma coseno con fase π/3 y propagación hacia +x.
    assert math.isclose(y(0.13, 7e-4), A * math.cos(w * 7e-4 - k * 0.13 + math.pi / 3), abs_tol=1e-12)
    assert math.isclose(y(0.2 + res["v"] * 1e-3, 1e-3), y(0.2, 0), abs_tol=1e-12)
