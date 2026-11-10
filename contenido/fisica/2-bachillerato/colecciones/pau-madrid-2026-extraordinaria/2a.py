"""Verificación de fis2b-pau-madrid-2026-ext-2a (onda armónica a partir de dos gráficas)."""

import math

# Lecturas de las gráficas
T = 1.0          # s
longitud = 4.0   # m
A = 3.0          # m
# Puntos de las gráficas: (x, t, y)
PUNTOS = [
    (0, 0, -3), (1, 0, 0), (2, 0, 3), (3, 0, 0), (4, 0, -3), (6, 0, 3),      # perfil en t = 0
    (1, 0.25, -3), (1, 0.5, 0), (1, 0.75, 3), (1, 1.0, 0), (1, 1.25, -3),    # oscilación en x = 1 m
]


def onda(x: float, t: float, fase: float) -> float:
    return A * math.sin(2 * math.pi / T * t - 2 * math.pi / longitud * x + fase)


def resolver() -> dict:
    return {"T": T, "k": 2 * math.pi / longitud, "A": A, "longitud": longitud}


def comprobar(res: dict) -> None:
    fase = 3 * math.pi / 2
    for x, t, y in PUNTOS:
        assert math.isclose(onda(x, t, fase), y, abs_tol=1e-9), f"no pasa por (x={x}, t={t}, y={y})"
    # La otra fase compatible con y(1, 0) = 0 no reproduce las gráficas.
    assert not math.isclose(onda(0, 0, math.pi / 2), -3, abs_tol=1e-9)
    # Formas equivalentes citadas en la solución.
    for x, t in ((0.3, 0.1), (2.7, 0.83)):
        assert math.isclose(onda(x, t, fase), onda(x, t, -math.pi / 2), abs_tol=1e-9)
        coseno = A * math.cos(2 * math.pi * t - math.pi / 2 * x + math.pi)
        assert math.isclose(onda(x, t, fase), coseno, abs_tol=1e-9)
    # Se propaga hacia +x: el perfil se desplaza v·dt.
    v = longitud / T
    assert math.isclose(onda(2 + v * 0.1, 0.1, fase), onda(2, 0, fase), abs_tol=1e-9)
