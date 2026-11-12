"""Verificación de fis2b-evau-madrid-2023-ord-a3 (tres cargas, resultado literal).

Se trabaja con K = q = a = 1, de modo que los resultados son los coeficientes
que multiplican a K q²/a² (fuerza) y K q²/a (trabajo).
"""

import math

K = q = a = 1.0
OTRAS = [(-q, (-a, a)), (2 * q, (0.0, 0.0))]
P = (a, a)
carga = -q


def fuerza(p):
    fx = fy = 0.0
    for Q, (x, y) in OTRAS:
        dx, dy = p[0] - x, p[1] - y
        d = math.hypot(dx, dy)
        fx += K * Q * carga * dx / d**3
        fy += K * Q * carga * dy / d**3
    return fx, fy


def energia(p):
    return sum(K * Q * carga / math.dist(p, pos) for Q, pos in OTRAS)


def resolver() -> dict:
    fx, fy = fuerza(P)
    return {"F_x": fx, "F_y": fy, "W": -energia(P)}


def comprobar(res: dict) -> None:
    assert math.isclose(res["F_x"], 0.25 - math.sqrt(2) / 2, rel_tol=1e-12)
    assert math.isclose(res["F_y"], -math.sqrt(2) / 2, rel_tol=1e-12)
    assert math.isclose(res["W"], math.sqrt(2) - 0.5, rel_tol=1e-12)
    # La fuerza es menos el gradiente de la energía potencial.
    h = 1e-6
    fx = -(energia((a + h, a)) - energia((a - h, a))) / (2 * h)
    fy = -(energia((a, a + h)) - energia((a, a - h))) / (2 * h)
    assert math.isclose(fx, res["F_x"], rel_tol=1e-6) and math.isclose(fy, res["F_y"], rel_tol=1e-6)
    # Gauss: carga encerrada +q en S1 y 0 en S2 -> flujos 4πKq y 0.
    assert 2 * q - q == q and 2 * q - q - q == 0
