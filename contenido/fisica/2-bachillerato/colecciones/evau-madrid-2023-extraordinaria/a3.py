"""Verificación de fis2b-evau-madrid-2023-ext-a3 (carga y posición a partir de V y E)."""

import math

# Datos del enunciado (SI)
K = 9e9
V = 54.0
E = (0.0, -180.0)
W = -270e-9


def resolver() -> dict:
    d = V / math.hypot(*E)
    q = V * d / K
    return {"q": q, "q2": -W / V}


def comprobar(res: dict) -> None:
    q = res["q"]
    posicion = (0.0, 0.3)
    # Con la carga en (0; 0,3) m se reproducen el potencial y el vector campo en el origen.
    dx, dy = 0 - posicion[0], 0 - posicion[1]
    d = math.hypot(dx, dy)
    assert math.isclose(K * q / d, V, rel_tol=1e-12)
    assert abs(K * q * dx / d**3 - E[0]) < 1e-12 and math.isclose(K * q * dy / d**3, E[1], rel_tol=1e-12)
    # En (0; −0,3) el campo saldría al revés.
    assert K * q * 0.3 / 0.3**3 > 0
    # Trabajo de la fuerza eléctrica: −q'·V = −270 nJ; cargas del mismo signo.
    assert math.isclose(-res["q2"] * V, W, rel_tol=1e-12) and res["q2"] * q > 0
    assert math.isclose(q, 1.8e-9, rel_tol=1e-12) and math.isclose(res["q2"], 5e-9, rel_tol=1e-12)
