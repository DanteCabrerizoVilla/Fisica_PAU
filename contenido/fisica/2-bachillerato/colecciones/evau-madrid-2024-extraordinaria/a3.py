"""Verificación de fis2b-evau-madrid-2024-ext-a3 (dos cargas positivas y un electrón)."""

import math

# Datos del enunciado (SI)
K = 9e9
e = 1.6e-19
CARGAS = [(2e-9, (0.0, 0.0)), (4e-9, (6.0, 0.0))]
P = (2.0, 2.0)


def campo(p):
    ex = ey = 0.0
    for q, (x, y) in CARGAS:
        dx, dy = p[0] - x, p[1] - y
        d = math.hypot(dx, dy)
        ex += K * q * dx / d**3
        ey += K * q * dy / d**3
    return ex, ey


def potencial(p):
    return sum(K * q / math.dist(p, pos) for q, pos in CARGAS)


def resolver() -> dict:
    ex, ey = campo(P)
    x = 6 / (1 + math.sqrt(2))
    W = -e * (0 - potencial((x, 0.0)))
    return {"E_x": ex, "E_y": ey, "x": x, "W": W}


def comprobar(res: dict) -> None:
    # En el punto hallado el campo es nulo.
    ex, _ = campo((res["x"], 0.0))
    assert abs(ex) < 1e-12, f"el campo no se anula: {ex}"
    # Trabajo como integral de la fuerza sobre el electrón viniendo por el eje y (x fijo) desde muy lejos.
    # Se integra en la variable u = 1/y para llegar al infinito.
    n = 200000
    trabajo = 0.0
    y_min = 1e-9                     # el punto final está sobre el eje: y -> 0
    for i in range(n):
        # tramo de y = 1/u, con u de 0 a 1/paso; se usa cambio y = tan(theta)
        th1 = math.pi / 2 * (1 - i / n)
        th2 = math.pi / 2 * (1 - (i + 1) / n)
        y1, y2 = math.tan(min(th1, math.pi / 2 - 1e-9)), max(math.tan(th2), y_min)
        ym = 0.5 * (y1 + y2)
        fy = -e * campo((res["x"], ym))[1]
        trabajo += fy * (y2 - y1)
    assert math.isclose(trabajo, res["W"], rel_tol=2e-3), f"la integral da {trabajo}"
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["E_x"], -0.02, rel_tol=6e-2) and math.isclose(res["E_y"], 2.40, rel_tol=2e-3)
    assert math.isclose(res["x"], 2.49, rel_tol=2e-3) and math.isclose(res["W"], 2.80e-18, rel_tol=2e-3)
