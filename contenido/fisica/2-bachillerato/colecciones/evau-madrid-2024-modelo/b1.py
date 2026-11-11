"""Verificación de fis2b-evau-madrid-2024-mod-b1 (caída libre y escape de un planeta)."""

import math

from scipy.integrate import solve_ivp

# Datos del enunciado (SI)
G = 6.67e-11
R = 1800e3
h, t = 2.0, 1.5
v0 = 3.0e3


def resolver() -> dict:
    g = 2 * h / t**2
    M = g * R**2 / G
    v_e = math.sqrt(2 * G * M / R)
    return {"g": g, "M": M, "v_escape": v_e, "v_lejos": math.sqrt(v0**2 - v_e**2)}


def comprobar(res: dict) -> None:
    M = res["M"]
    assert v0 > res["v_escape"]
    # Segunda vía: integrar el ascenso radial hasta muy lejos y leer la velocidad.
    def f(_, estado):
        r, v = estado
        return [v, -G * M / r**2]

    sol = solve_ivp(f, (0, 5e9), [R, v0], rtol=1e-11, atol=1e-6)
    r_final, v_final = sol.y[0, -1], sol.y[1, -1]
    # Corrección por la energía potencial que aún queda a esa distancia.
    v_inf = math.sqrt(v_final**2 - 2 * G * M / r_final)
    assert r_final > 1e3 * R and math.isclose(v_inf, res["v_lejos"], rel_tol=1e-6), f"integración: {v_inf}"
    # Valores de la solución orientativa oficial.
    for clave, oficial in (("g", 1.78), ("M", 8.65e22), ("v_escape", 2.53e3), ("v_lejos", 1.61e3)):
        assert math.isclose(res[clave], oficial, rel_tol=3e-3), f"{clave} no coincide con la solución oficial"
