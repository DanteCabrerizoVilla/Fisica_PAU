"""Verificación de fis2b-evau-madrid-2024-mod-a3 (carga traída del infinito y carga de equilibrio)."""

import math

# Datos del enunciado (SI)
K = 9e9
FIJAS = [(2e-9, (0.0, 0.0)), (2e-9, (4.0, 0.0))]
P = (2.0, 2.0)
W = 1.27e-7
q3 = -10e-9


def campo(cargas, p):
    ex = ey = 0.0
    for q, (x, y) in cargas:
        dx, dy = p[0] - x, p[1] - y
        d = math.hypot(dx, dy)
        ex += K * q * dx / d**3
        ey += K * q * dy / d**3
    return ex, ey


def potencial(cargas, p):
    return sum(K * q / math.dist(p, pos) for q, pos in cargas)


def resolver() -> dict:
    Q = -W / potencial(FIJAS, P)
    _, ey = campo(FIJAS, P)
    d = math.sqrt(K * abs(q3) / ey)
    return {"Q": Q, "y": P[1] - d}


def comprobar(res: dict) -> None:
    # Con q3 en (2, y) el campo total en P se anula y, por tanto, la fuerza sobre Q.
    ex, ey = campo(FIJAS + [(q3, (2.0, res["y"]))], P)
    assert abs(ex) < 1e-12 and abs(ey) < 1e-9, f"campo residual ({ex}, {ey})"
    # Colocada encima, a la misma distancia, el campo no se anula (se duplica).
    _, ey_mal = campo(FIJAS + [(q3, (2.0, 2 * P[1] - res["y"]))], P)
    assert ey_mal > 6
    # Q negativa y trabajo del campo positivo.
    assert res["Q"] < 0 and math.isclose(-res["Q"] * potencial(FIJAS, P), W, rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["Q"], -9.98e-9, rel_tol=2e-3) and math.isclose(res["y"], -3.32, rel_tol=2e-3)
