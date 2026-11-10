"""Verificación de fis2b-pau-madrid-2027-mod-3a (dos cargas: campo, potencial, trabajo)."""

import math

# Datos del enunciado (SI)
K = 9e9
CARGAS = [(-2e-9, (-5.0, 0.0)), (2e-9, (5.0, 0.0))]
A = (5.0, 4.0)
B = (0.0, 4.0)
q_prueba = 3e-9


def campo(punto):
    ex = ey = 0.0
    for q, (x, y) in CARGAS:
        dx, dy = punto[0] - x, punto[1] - y
        d = math.hypot(dx, dy)
        ex += K * q * dx / d**3
        ey += K * q * dy / d**3
    return ex, ey


def potencial(punto):
    return sum(K * q / math.hypot(punto[0] - x, punto[1] - y) for q, (x, y) in CARGAS)


def resolver() -> dict:
    ex, ey = campo(A)
    return {"E_x": ex, "E_y": ey, "V_A": potencial(A), "W": q_prueba * (potencial(A) - potencial(B))}


def comprobar(res: dict) -> None:
    assert abs(potencial(B)) < 1e-12, "el potencial en B debería ser nulo"
    # El campo es menos el gradiente del potencial (derivada numérica).
    h = 1e-5
    ex = -(potencial((A[0] + h, A[1])) - potencial((A[0] - h, A[1]))) / (2 * h)
    ey = -(potencial((A[0], A[1] + h)) - potencial((A[0], A[1] - h))) / (2 * h)
    assert math.isclose(ex, res["E_x"], rel_tol=1e-6) and math.isclose(ey, res["E_y"], rel_tol=1e-6), \
        "el campo no coincide con el gradiente del potencial"
    # Trabajo como integral de la fuerza a lo largo del segmento recto de A a B.
    n = 20000
    trabajo = 0.0
    for i in range(n):
        x = A[0] + (B[0] - A[0]) * (i + 0.5) / n
        trabajo += q_prueba * campo((x, 4.0))[0] * (B[0] - A[0]) / n
    assert math.isclose(trabajo, res["W"], rel_tol=1e-6), "el trabajo no coincide con la integral de la fuerza"
    # Valores de la solución orientativa oficial.
    for clave, oficial in (("E_x", -0.144), ("E_y", 1.067), ("V_A", 2.83), ("W", 8.49e-9)):
        assert math.isclose(res[clave], oficial, rel_tol=5e-3), f"{clave} no coincide con la solución oficial"
