"""Verificación de fis2b-evau-madrid-2024-mod-a4 (espejo cóncavo)."""

import math

# Datos del enunciado (cm, criterio DIN)
R = -60.0
s = -80.0
y = 5.0


def resolver() -> dict:
    f = R / 2
    s_im = 1 / (1 / f - 1 / s)
    return {"s_im": s_im, "y_im": -s_im / s * y}


def comprobar(res: dict) -> None:
    f = R / 2
    # Trazado: rayo paralelo reflejado (recta por (0, y) y el foco) y rayo por C (recta por (s, y) y (R, 0)).
    # y1(x) = y (1 − x/f) ; y2(x) = y (x − R)/(s − R)
    x = (1 + R / (s - R)) / (1 / f + 1 / (s - R))
    assert math.isclose(x, res["s_im"], rel_tol=1e-12), f"los rayos se cortan en x = {x}"
    assert math.isclose(y * (1 - x / f), res["y_im"], rel_tol=1e-12)
    # Imagen real (delante del espejo), entre C y F, invertida y menor.
    assert R < res["s_im"] < f and -y < res["y_im"] < 0
    assert (round(res["s_im"], 9), round(res["y_im"], 9)) == (-48.0, -3.0)
