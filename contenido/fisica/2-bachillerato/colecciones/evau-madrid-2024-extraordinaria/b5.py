"""Verificación de fis2b-evau-madrid-2024-ext-b5 (recta V-f del efecto fotoeléctrico)."""

import math

# Datos del enunciado
e = 1.6e-19
pendiente = 4.16e-15      # V·s
ordenada = -2.16          # V


def resolver() -> dict:
    return {"f0": -ordenada / pendiente, "W": -ordenada, "h": pendiente * e}


def comprobar(res: dict) -> None:
    h, f0, W = res["h"], res["f0"], res["W"]
    # Coherencia interna: h·f0 = W0.
    assert math.isclose(h * f0 / e, W, rel_tol=1e-12)
    # Para una frecuencia cualquiera, Einstein reproduce la recta.
    f = 9.0e14
    assert math.isclose((h * f - W * e) / e, pendiente * f + ordenada, rel_tol=1e-12)
    # h cercana al valor aceptado.
    assert math.isclose(h, 6.63e-34, rel_tol=6e-3)
    # Valores de la solución orientativa oficial.
    assert math.isclose(f0, 5.2e14, rel_tol=3e-3) and math.isclose(h, 6.66e-34, rel_tol=2e-3)
