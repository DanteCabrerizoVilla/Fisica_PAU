"""Verificación de fis2b-evau-madrid-2024-ord-b3 (dos cargas positivas iguales)."""

import math

# Datos del enunciado (SI)
K = 9e9
CARGAS = [(9e-9, (-6e-3, 0.0)), (9e-9, (6e-3, 0.0))]
P = (0.0, 3e-3)


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
    ex0, ey0 = campo((0.0, 0.0))
    exp_, eyp = campo(P)
    return {"V_O": potencial((0.0, 0.0)), "E_O": math.hypot(ex0, ey0), "V_P": potencial(P), "E_P": eyp}


def comprobar(res: dict) -> None:
    assert res["E_O"] == 0, "el campo en el origen debe anularse exactamente"
    assert abs(campo(P)[0]) < 1e-6, "la componente horizontal en (0, 3) mm debe anularse"
    # El campo es menos el gradiente del potencial (derivada numérica en y).
    h = 1e-9
    ey = -(potencial((0.0, P[1] + h)) - potencial((0.0, P[1] - h))) / (2 * h)
    assert math.isclose(ey, res["E_P"], rel_tol=1e-5)
    # Valores de la solución orientativa oficial.
    for clave, oficial in (("V_O", 2.70e4), ("V_P", 2.41e4), ("E_P", 1.61e6)):
        assert math.isclose(res[clave], oficial, rel_tol=3e-3), f"{clave} no coincide con la solución oficial"
