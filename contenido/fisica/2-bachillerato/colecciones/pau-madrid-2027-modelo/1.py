"""Verificación de fis2b-pau-madrid-2027-mod-1 (lente delgada y gráfica M-s')."""

import math

# Punto de la gráfica (cm)
s_imagen = 40.0
M = -4.0


def resolver() -> dict:
    f = s_imagen / (1 - M)
    s = s_imagen / M
    return {"f": f, "s": s}


def comprobar(res: dict) -> None:
    f, s = res["f"], res["s"]
    # La ecuación de la lente debe cumplirse con esos valores.
    assert math.isclose(1 / s_imagen - 1 / s, 1 / f, rel_tol=1e-12), "no cumple la ecuación de la lente"
    # Otros puntos de la gráfica dan la misma focal.
    for sp, m in ((20.0, -1.5), (24.0, -2.0), (16.0, -1.0), (8.0, 0.0)):
        assert math.isclose(1 - sp / f, m, abs_tol=1e-9), f"el punto ({sp}, {m}) no está en la recta"
    # Objeto entre f' y 2f': imagen real, invertida y mayor.
    assert f < abs(s) < 2 * f and s_imagen > 0 and M < -1
    # Trazado: el rayo paralelo y el del centro se cortan en la imagen.
    y = 1.0
    y_por_foco = y - (y / f) * s_imagen          # sale de (0, y) y pasa por (f, 0)
    y_por_centro = (y / s) * s_imagen            # recta por el origen
    assert math.isclose(y_por_foco, y_por_centro) and math.isclose(y_por_foco, M * y)
