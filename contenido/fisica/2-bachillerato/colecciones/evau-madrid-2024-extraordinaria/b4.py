"""Verificación de fis2b-evau-madrid-2024-ext-b4 (lente y pantalla, aumento −3)."""

import math

# Datos del enunciado (m, criterio DIN)
distancia = 4.0
M = -3.0


def resolver() -> dict:
    s = distancia / (M - 1)
    s_im = M * s
    return {"s": s, "f": 1 / (1 / s_im - 1 / s)}


def comprobar(res: dict) -> None:
    s, f = res["s"], res["f"]
    s_im = 1 / (1 / f + 1 / s)
    assert math.isclose(s_im - s, distancia, rel_tol=1e-12) and math.isclose(s_im / s, M, rel_tol=1e-12)
    assert f < abs(s) < 2 * f, "el objeto debe estar entre f' y 2f'"
    # Trazado: los tres rayos llegan a la misma altura en la pantalla.
    y = 1.0
    por_foco_imagen = y - y / f * s_im
    por_centro = y / s * s_im
    por_foco_objeto = y - (y / (s + f)) * s          # altura en la lente del rayo que pasa por F(−f, 0)
    assert math.isclose(por_foco_imagen, por_centro, rel_tol=1e-12)
    assert math.isclose(por_foco_objeto, por_centro, rel_tol=1e-12) and math.isclose(por_centro, M * y, rel_tol=1e-12)
    assert (round(s, 9), round(f, 9)) == (-1.0, 0.75)
