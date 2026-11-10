"""Verificación de fis2b-pau-madrid-2026-ext-3a (carga y distancia a partir de V y E)."""

import math

# Datos del enunciado (SI)
K = 9e9
V = 9e2
E = 1.8e4
q2 = -10e-9
pos2 = (0.0, 0.05)
punto = (0.05, 0.0)


def campo(cargas, p):
    ex = ey = 0.0
    for q, (x, y) in cargas:
        dx, dy = p[0] - x, p[1] - y
        d = math.hypot(dx, dy)
        ex += K * q * dx / d**3
        ey += K * q * dy / d**3
    return ex, ey


def resolver() -> dict:
    d1 = V / E
    q1 = V * d1 / K
    ex, ey = campo([(q1, (0.0, 0.0)), (q2, pos2)], punto)
    return {"q1": q1, "d1": d1, "E_x": ex, "E_y": ey}


def comprobar(res: dict) -> None:
    # Con la carga y la distancia halladas se recuperan los dos datos.
    assert math.isclose(K * res["q1"] / res["d1"], V, rel_tol=1e-12)
    assert math.isclose(K * res["q1"] / res["d1"] ** 2, E, rel_tol=1e-12)
    # El punto del apartado b es el punto P.
    assert math.isclose(res["d1"], punto[0], rel_tol=1e-12)
    # Los dos campos tienen el mismo módulo y forman 135°.
    e2 = K * abs(q2) / (0.05**2 + 0.05**2)
    assert math.isclose(e2, E, rel_tol=1e-12)
    modulo = math.hypot(res["E_x"], res["E_y"])
    assert math.isclose(modulo, math.sqrt(2 * E**2 + 2 * E * E * math.cos(math.radians(135))), rel_tol=1e-9)
    # Valores de la solución orientativa oficial.
    for clave, oficial in (("q1", 5e-9), ("d1", 5e-2), ("E_x", 0.53e4), ("E_y", 1.27e4)):
        assert math.isclose(res[clave], oficial, rel_tol=6e-3), f"{clave} no coincide con la solución oficial"
