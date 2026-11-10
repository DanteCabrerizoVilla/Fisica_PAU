"""Verificación de fis2b-pau-madrid-2025-mod-2a (tres cargas en triángulo equilátero)."""

import math
from itertools import combinations

# Datos del enunciado (SI)
K = 9e9
CARGAS = [
    (4e-9, (0.0, 0.0)),
    (-2e-9, (0.02, 0.02 * math.sqrt(3))),
    (-4e-9, (0.04, 0.0)),
]


def energia(cargas) -> float:
    return sum(K * q1 * q2 / math.dist(p1, p2) for (q1, p1), (q2, p2) in combinations(cargas, 2))


def resolver() -> dict:
    q3, p3 = CARGAS[2]
    fx = fy = 0.0
    for q, p in CARGAS[:2]:
        dx, dy = p3[0] - p[0], p3[1] - p[1]
        d = math.hypot(dx, dy)
        fx += K * q * q3 * dx / d**3
        fy += K * q * q3 * dy / d**3
    return {"F_x": fx, "F_y": fy, "energia": energia(CARGAS)}


def comprobar(res: dict) -> None:
    # El triángulo es equilátero de 4 cm de lado.
    for (_, p1), (_, p2) in combinations(CARGAS, 2):
        assert math.isclose(math.dist(p1, p2), 0.04, rel_tol=1e-12)
    # Segunda vía para la fuerza: menos el gradiente de la energía al desplazar Q3.
    h = 1e-7
    q3, (x3, y3) = CARGAS[2]

    def con_q3_en(x, y):
        return energia(CARGAS[:2] + [(q3, (x, y))])

    fx = -(con_q3_en(x3 + h, y3) - con_q3_en(x3 - h, y3)) / (2 * h)
    fy = -(con_q3_en(x3, y3 + h) - con_q3_en(x3, y3 - h)) / (2 * h)
    assert math.isclose(fx, res["F_x"], rel_tol=1e-5) and math.isclose(fy, res["F_y"], rel_tol=1e-5)
    # Valores de la solución orientativa oficial.
    for clave, oficial in (("F_x", -6.75e-5), ("F_y", -3.90e-5), ("energia", -3.6e-6)):
        assert math.isclose(res[clave], oficial, rel_tol=2e-3), f"{clave} no coincide con la solución oficial"
