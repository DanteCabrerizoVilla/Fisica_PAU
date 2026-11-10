"""Verificación de fis2b-pau-madrid-2025-ext-2b (dos masas iguales: campo y trabajo)."""

import math

# Datos del enunciado (SI)
G = 6.67e-11
MASAS = [(3.0, (0.0, 0.0)), (3.0, (6.0, 0.0))]
A = (3.0, 3.0)
B = (0.0, 3.0)
m = 1.0


def campo(p):
    gx = gy = 0.0
    for masa, (x, y) in MASAS:
        dx, dy = x - p[0], y - p[1]
        d = math.hypot(dx, dy)
        gx += G * masa * dx / d**3
        gy += G * masa * dy / d**3
    return gx, gy


def potencial(p):
    return -sum(G * masa / math.hypot(p[0] - x, p[1] - y) for masa, (x, y) in MASAS)


def resolver() -> dict:
    gx, gy = campo(A)
    if abs(gx) < 1e-9 * abs(gy):      # se anula por simetría; se descarta el ruido de redondeo
        gx = 0.0
    return {"g_x": gx, "g_y": gy, "W": m * (potencial(A) - potencial(B))}


def comprobar(res: dict) -> None:
    assert abs(res["g_x"]) < 1e-25, "por simetría la componente x debe anularse"
    # Trabajo como integral de la fuerza a lo largo del segmento recto de A a B.
    n = 20000
    trabajo = 0.0
    for i in range(n):
        x = A[0] + (B[0] - A[0]) * (i + 0.5) / n
        trabajo += m * campo((x, 3.0))[0] * (B[0] - A[0]) / n
    assert math.isclose(trabajo, res["W"], rel_tol=1e-6), f"la integral da {trabajo}"
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["g_y"], -1.57e-11, rel_tol=3e-3)
    assert math.isclose(res["W"], 2.20e-12, rel_tol=3e-3)
