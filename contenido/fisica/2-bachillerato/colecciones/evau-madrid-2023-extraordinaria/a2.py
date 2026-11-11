"""Verificación de fis2b-evau-madrid-2023-ext-a2 (onda hacia −x en una cuerda)."""

import math

# Datos del enunciado (SI)
v = 400.0
a_max = 2e4
separacion_ceros = 0.4
y0 = 1e-3


def resolver() -> dict:
    longitud = 2 * separacion_ceros
    f = v / longitud
    A = a_max / (2 * math.pi * f) ** 2
    # Elongación con la ecuación de onda completa (hacia −x, velocidad inicial positiva).
    w, k = 2 * math.pi * f, 2 * math.pi / longitud
    fase = math.asin(y0 / A)                       # coseno positivo: velocidad positiva
    y = A * math.sin(w * 2.0 + k * 1.2 + fase)
    return {"f": f, "A": A, "y": y}


def comprobar(res: dict) -> None:
    A, f = res["A"], res["f"]
    w, k = 2 * math.pi * f, 2 * math.pi / 0.8
    fase = math.asin(y0 / A)
    assert math.isclose(fase, 0.52, abs_tol=0.01)

    def y(x, t):
        return A * math.sin(w * t + k * x + fase)

    h = 1e-9
    assert math.isclose(y(0, 0), y0, rel_tol=1e-12) and (y(0, h) - y(0, -h)) > 0
    # Ceros consecutivos separados 0,4 m en un instante cualquiera.
    x_cero = (-fase) / k
    assert abs(y(x_cero, 0)) < 1e-12 and abs(y(x_cero + 0.4, 0)) < 1e-12
    # Viaja hacia −x a 400 m/s.
    assert math.isclose(y(0.3 - v * 1e-4, 1e-4), y(0.3, 0), abs_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(A, 2.0e-3, rel_tol=2e-2) and math.isclose(res["y"], -1e-3, rel_tol=1e-6)
