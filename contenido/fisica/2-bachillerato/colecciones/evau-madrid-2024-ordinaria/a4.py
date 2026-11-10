"""Verificación de fis2b-evau-madrid-2024-ord-a4 (lente con imagen derecha y menor)."""

import math

# Datos del enunciado (m, criterio DIN)
s = -0.20
y, y_im = 4e-3, 2e-3


def resolver() -> dict:
    s_im = y_im / y * s
    return {"P": 1 / s_im - 1 / s}


def comprobar(res: dict) -> None:
    f = 1 / res["P"]
    assert f < 0, "la lente debe ser divergente"
    # Trazado: prolongación del rayo paralelo (recta por F' y (0, y)) y rayo central.
    # y1(x) = y (1 − x/f)  [pasa por (f, 0) y (0, y)] ;  y2(x) = y x / s
    x = 1 / (1 / s + 1 / f)
    assert math.isclose(y * (1 - x / f), y * x / s, rel_tol=1e-12)
    assert math.isclose(x, -0.10, rel_tol=1e-12) and math.isclose(y * x / s, y_im, rel_tol=1e-12)
    assert math.isclose(res["P"], -5.0, rel_tol=1e-12)
