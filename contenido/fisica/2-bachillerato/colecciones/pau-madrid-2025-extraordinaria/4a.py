"""Verificación de fis2b-pau-madrid-2025-ext-4a (espectrómetro de masas)."""

import math

import numpy as np

# Datos del enunciado (SI)
N_A = 6.02e23
e = 1.6e-19
q = 2 * e
m = 40e-3 / N_A
v = np.array([2.4e5, 0.0, 0.0])
B1 = np.array([0.0, 1.0e-3, 0.0])
B2 = np.array([0.0, 1.5, 0.0])


def resolver() -> dict:
    E = -np.cross(v, B1)                        # anula la fuerza de Lorentz: E + v × B = 0
    radio = m * np.linalg.norm(v) / (q * np.linalg.norm(B2))
    return {"E": float(np.linalg.norm(E)), "radio": float(radio)}


def comprobar(res: dict) -> None:
    E = -np.cross(v, B1)
    assert np.allclose(E, [0, 0, -240]), f"el campo debe ser −240 k, sale {E}"
    assert np.allclose(q * (E + np.cross(v, B1)), 0), "la fuerza neta en el selector no es nula"
    # Segunda vía para el radio: integrar el movimiento en B2 media vuelta y medir el diámetro.
    pos = np.zeros(3)
    vel = v.copy()
    periodo = 2 * math.pi * m / (q * 1.5)
    n = 20000
    dt = periodo / 2 / n
    for _ in range(n):                          # rotación exacta de la velocidad en cada paso
        a = q / m * np.cross(vel, B2)
        vel_medio = vel + 0.5 * dt * a
        a = q / m * np.cross(vel_medio, B2)
        pos = pos + dt * vel_medio
        vel = vel + dt * a
        vel *= np.linalg.norm(v) / np.linalg.norm(vel)
    assert math.isclose(abs(pos[2]), 2 * res["radio"], rel_tol=1e-3), f"diámetro medido {pos[2]}"
    assert pos[2] > 0, "el ion positivo debe curvarse hacia +z"
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["E"], 240, rel_tol=1e-9) and math.isclose(res["radio"], 3.33e-2, rel_tol=4e-3)
