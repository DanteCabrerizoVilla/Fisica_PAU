"""Verificación de fis2b-pau-madrid-2025-mod-3b (espejo convexo)."""

import math

# Datos del enunciado (cm, criterio DIN)
s = -12.0
M = 0.25


def resolver() -> dict:
    s_im = -M * s
    f = 1 / (1 / s_im + 1 / s)
    return {"s_im": s_im, "R": 2 * f}


def comprobar(res: dict) -> None:
    s_im, R = res["s_im"], res["R"]
    f = R / 2
    assert s_im > 0 and R > 0, "imagen virtual detrás del espejo y espejo convexo"
    # Segunda vía: intersección de las prolongaciones de los dos rayos del trazado.
    y = 1.0
    # Rayo paralelo: reflejado sobre la recta que pasa por (0, y) y el foco (f, 0).
    # Rayo hacia C: recta que pasa por (s, y) y el centro (R, 0).
    # y1(x) = y (1 − x/f) ; y2(x) = y (R − x)/(R − s)
    x = (1 - R / (R - s)) / (1 / f - 1 / (R - s))
    altura = y * (1 - x / f)
    assert math.isclose(x, s_im, rel_tol=1e-12), f"las prolongaciones se cortan en x = {x}"
    assert math.isclose(altura, M * y, rel_tol=1e-12)
    # Tercera vía: reflexión exacta de un rayo paraxial en la esfera de radio R centrada en (R, 0).
    h = 1e-4                                   # altura de incidencia muy pequeña
    # Rayo desde (s, 0) hacia el punto del espejo a altura h.
    xm = R - math.sqrt(R**2 - h**2)
    d = (xm - s, h)
    n = (xm - R, h)                            # normal (radial)
    nn = math.hypot(*n)
    n = (n[0] / nn, n[1] / nn)
    pe = d[0] * n[0] + d[1] * n[1]
    r = (d[0] - 2 * pe * n[0], d[1] - 2 * pe * n[1])
    x_corte = xm - h * r[0] / r[1]             # donde la prolongación corta al eje
    assert math.isclose(x_corte, s_im, rel_tol=1e-4), f"trazado exacto: {x_corte}"
    assert (round(s_im, 9), round(R, 9)) == (3.0, 8.0)
