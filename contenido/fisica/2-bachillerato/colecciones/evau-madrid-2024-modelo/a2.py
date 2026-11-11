"""Verificación de fis2b-evau-madrid-2024-mod-a2 (muelle y onda en una cuerda)."""

import math

# Datos del enunciado (SI)
k_muelle = 750.0
f = 3.0
E = 1.0
v = 5.0


def resolver() -> dict:
    w = 2 * math.pi * f
    return {"A": math.sqrt(2 * E / k_muelle), "m": k_muelle / w**2}


def comprobar(res: dict) -> None:
    A, m = res["A"], res["m"]
    w = 2 * math.pi * f
    # Energía por la velocidad máxima: (1/2) m (A w)² = E.
    assert math.isclose(0.5 * m * (A * w) ** 2, E, rel_tol=1e-12)
    k_onda = w / v

    def y(x, t):
        return A * math.sin(w * t - k_onda * x + math.pi)

    h = 1e-8
    assert abs(y(0, 0)) < 1e-15 and (y(0, h) - y(0, -h)) / (2 * h) < 0
    # Se propaga hacia +x a 5 m/s; longitud de onda v/f = 5/3 m.
    assert math.isclose(y(0.4 + v * 0.03, 0.03), y(0.4, 0), abs_tol=1e-12)
    assert math.isclose(y(0.2 + v / f, 0.01), y(0.2, 0.01), abs_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(A, 0.052, rel_tol=1e-2) and math.isclose(m, 2.11, rel_tol=2e-3)
