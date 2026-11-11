"""Verificación de fis2b-evau-madrid-2024-mod-b3 (solenoide con corriente variable)."""

import math

# Datos del enunciado (SI)
MU0 = 4 * math.pi * 1e-7
n = 250.0
a = 0.03
R = 5.0
VERTICES = [(0.0, 0.0), (5.0, 10.0), (10.0, 10.0), (11.0, 0.0)]     # gráfica I(t)


def corriente(t: float) -> float:
    for (t1, i1), (t2, i2) in zip(VERTICES, VERTICES[1:]):
        if t1 <= t <= t2:
            return i1 + (i2 - i1) * (t - t1) / (t2 - t1)
    return 0.0


def flujo(t: float) -> float:
    return MU0 * n * corriente(t) * a**2


def inducida(t: float, h: float = 1e-4) -> float:
    return abs((flujo(t + h) - flujo(t - h)) / (2 * h)) / R


def resolver() -> dict:
    return {"B3": MU0 * n * corriente(3), "B8": MU0 * n * corriente(8), "I3": inducida(3), "I8": inducida(8)}


def comprobar(res: dict) -> None:
    assert corriente(3) == 6 and corriente(8) == 10
    # Expresión directa con la pendiente de 2 A/s (la oficial imprime 1,11e-7; la operación da 1,13e-7).
    directa = MU0 * n * a**2 * 2 / R
    assert math.isclose(res["I3"], directa, rel_tol=1e-6) and math.isclose(directa, 1.131e-7, rel_tol=1e-3)
    # En la bajada (t = 10,5 s) la corriente inducida es cinco veces mayor que en la subida.
    assert math.isclose(inducida(10.5), 5 * res["I3"], rel_tol=1e-6)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["B3"], 1.88e-3, rel_tol=4e-3), "B(3 s) no coincide con la solución oficial"
    assert math.isclose(res["B8"], 3.14e-3, rel_tol=4e-3), "B(8 s) no coincide con la solución oficial"
