"""Verificación de fis2b-pau-madrid-2025-ord-2a (electrón y positrón)."""

import math

from scipy.integrate import solve_ivp

# Datos del enunciado (SI)
K = 9e9
e = 1.6e-19
m_e = 9.1e-31
CARGAS = [(-e, (0.0, 6e-9)), (e, (0.0, -6e-9))]
P = (8e-9, 0.0)
v0 = 1.5e5
d0 = 12e-9


def campo(p):
    ex = ey = 0.0
    for q, (x, y) in CARGAS:
        dx, dy = p[0] - x, p[1] - y
        d = math.hypot(dx, dy)
        ex += K * q * dx / d**3
        ey += K * q * dy / d**3
    return ex, ey


def resolver() -> dict:
    ex, ey = campo(P)
    if abs(ex) < 1e-9 * abs(ey):          # se anula por simetría
        ex = 0.0
    energia = 0.5 * m_e * v0**2 - K * e**2 / d0
    return {"E_x": ex, "E_y": ey, "d_max": -K * e**2 / energia}


def comprobar(res: dict) -> None:
    # Segunda vía: integrar el movimiento del positrón (se aleja a lo largo del eje y)
    # hasta que se detiene, y leer la separación.
    def f(_, estado):
        r, v = estado
        return [v, -K * e**2 / (m_e * r**2)]

    def parado(_, estado):
        return estado[1]

    parado.terminal = True
    parado.direction = -1
    sol = solve_ivp(f, (0, 1e-11), [d0, v0], events=parado, rtol=1e-11, atol=1e-20, max_step=1e-15)
    assert sol.t_events[0].size == 1, "el positrón no llega a detenerse"
    assert math.isclose(sol.y[0, -1], res["d_max"], rel_tol=1e-6), f"la integración da {sol.y[0, -1]}"
    # La energía total es negativa: el sistema está ligado.
    assert 0.5 * m_e * v0**2 < K * e**2 / d0
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["E_y"], 1.73e7, rel_tol=3e-3) and math.isclose(res["d_max"], 2.57e-8, rel_tol=3e-3)
