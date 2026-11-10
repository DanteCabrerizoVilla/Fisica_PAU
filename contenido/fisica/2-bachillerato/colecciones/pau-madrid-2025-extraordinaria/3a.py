"""Verificación de fis2b-pau-madrid-2025-ext-3a (bloque unido a un muelle)."""

import math

# Datos del enunciado (SI)
A = 0.05
Ec_equilibrio = 0.02
m = 4.0
x = 0.02


def resolver() -> dict:
    k = 2 * Ec_equilibrio / A**2
    T = 2 * math.pi * math.sqrt(m / k)
    v = math.sqrt(k / m * (A**2 - x**2))
    return {"k": k, "T": T, "v": v}


def comprobar(res: dict) -> None:
    k, T = res["k"], res["T"]
    omega = 2 * math.pi / T
    # Segunda vía: ecuaciones del MAS, x = A cos(wt). Instante en que x = 2 cm y velocidad allí.
    t = math.acos(x / A) / omega
    assert math.isclose(abs(-A * omega * math.sin(omega * t)), res["v"], rel_tol=1e-12)
    # Velocidad máxima coherente con la energía cinética del enunciado.
    assert math.isclose(0.5 * m * (A * omega) ** 2, Ec_equilibrio, rel_tol=1e-12)
    # Tercera vía: integración numérica de m·a = −k·x desde el extremo hasta x = 2 cm.
    pos, vel, dt = A, 0.0, 1e-5
    while pos > x:
        vel += -k / m * pos * dt
        pos += vel * dt
    assert math.isclose(abs(vel), res["v"], rel_tol=1e-3), f"la integración da {vel}"
    # Valores de la solución orientativa oficial.
    assert math.isclose(k, 16, rel_tol=1e-9) and math.isclose(T, 3.14, rel_tol=1e-3)
    assert math.isclose(res["v"], 0.0917, rel_tol=1e-3)
