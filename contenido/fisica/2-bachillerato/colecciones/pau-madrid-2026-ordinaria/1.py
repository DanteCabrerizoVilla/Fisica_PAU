"""Verificación de fis2b-pau-madrid-2026-ord-1 (campo uniforme a partir del potencial)."""

import math

# Datos del enunciado (SI)
q = 10e-9
m = 6e-10
x_final = 5.0


def V(x: float) -> float:
    return -3 * x


def resolver() -> dict:
    h = 1e-6
    E = -(V(x_final + h) - V(x_final - h)) / (2 * h)      # derivada numérica
    a = q * E / m
    v = math.sqrt(2 * q * (V(0) - V(x_final)) / m)
    return {"E": E, "a": a, "v": v}


def comprobar(res: dict) -> None:
    # Cinemática con aceleración constante.
    assert math.isclose(res["v"], math.sqrt(2 * res["a"] * x_final), rel_tol=1e-6), "v² distinto de 2·a·x"
    # Integración paso a paso del movimiento (Euler semiimplícito).
    x = v = 0.0
    dt = 1e-5
    while x < x_final:
        v += res["a"] * dt
        x += v * dt
    assert math.isclose(v, res["v"], rel_tol=1e-3), f"la integración da v = {v}"
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["E"], 3, rel_tol=1e-6) and math.isclose(res["a"], 50, rel_tol=1e-6)
    assert math.isclose(res["v"], 22.36, rel_tol=1e-3)
