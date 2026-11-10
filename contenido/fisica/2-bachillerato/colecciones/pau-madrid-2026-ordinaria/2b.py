"""Verificación de fis2b-pau-madrid-2026-ord-2b (campo gravitatorio de dos masas)."""

import math

# Datos del enunciado (SI)
G = 6.67e-11
MASAS = [(2.0, (0.0, 0.0)), (4.0, (4.0, 0.0))]


def campo(p):
    gx = gy = 0.0
    for m, (x, y) in MASAS:
        dx, dy = x - p[0], y - p[1]          # hacia la masa
        d = math.hypot(dx, dy)
        gx += G * m * dx / d**3
        gy += G * m * dy / d**3
    return gx, gy


def resolver() -> dict:
    x = 4 / (1 + math.sqrt(2))
    gx, gy = campo((0.0, 2.0))
    return {"x": x, "g_x": gx, "g_y": gy}


def comprobar(res: dict) -> None:
    # En el punto hallado el campo total es nulo.
    gx, gy = campo((res["x"], 0.0))
    assert abs(gx) < 1e-22 and gy == 0, f"el campo no se anula: {gx}"
    # Búsqueda numérica del cero por bisección entre las dos masas.
    a, b = 0.01, 3.99
    for _ in range(80):
        c = (a + b) / 2
        if campo((a, 0.0))[0] * campo((c, 0.0))[0] <= 0:
            b = c
        else:
            a = c
    assert math.isclose(a, res["x"], rel_tol=1e-9), f"la bisección da {a}"
    # Es raíz de x² + 8x − 16 = 0.
    assert abs(res["x"] ** 2 + 8 * res["x"] - 16) < 1e-12
    # En la otra raíz los módulos coinciden pero el campo no se anula.
    assert abs(campo((-4 - 4 * math.sqrt(2), 0.0))[0]) > 1e-13
    # Valores de la solución orientativa oficial.
    for clave, oficial in (("x", 1.66), ("g_x", 1.19e-11), ("g_y", -3.94e-11)):
        assert math.isclose(res[clave], oficial, rel_tol=5e-3), f"{clave} no coincide con la solución oficial"
