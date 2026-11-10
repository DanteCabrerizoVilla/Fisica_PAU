"""Verificación de fis2b-pau-madrid-2026-ext-1 (de órbita elíptica a circular)."""

import math

# Datos del enunciado (SI)
G = 6.67e-11
M_T = 5.97e24
m = 50.0
t_medio = 55759.5
r_cir = 8.2e4 * 1e3
v_p = 6.0e3


def resolver() -> dict:
    T = 2 * t_medio
    a = (G * M_T * T**2 / (4 * math.pi**2)) ** (1 / 3)
    r_p = 2 * a - r_cir
    E_elip = 0.5 * m * v_p**2 - G * M_T * m / r_p
    E_circ = -G * M_T * m / (2 * r_cir)
    return {"T": T, "a": a, "r_p": r_p, "E_elip": E_elip, "E_circ": E_circ}


def comprobar(res: dict) -> None:
    # La energía de una órbita elíptica solo depende del semieje: -GMm/(2a).
    # Debe coincidir con la calculada con la velocidad en el perigeo que da el enunciado.
    por_semieje = -G * M_T * m / (2 * res["a"])
    assert math.isclose(res["E_elip"], por_semieje, rel_tol=5e-3), \
        f"los datos no son coherentes: {res['E_elip']:.4g} frente a {por_semieje:.4g}"
    # La velocidad en el perigeo que predice vis-viva es la del enunciado.
    v_teorica = math.sqrt(G * M_T * (2 / res["r_p"] - 1 / res["a"]))
    assert math.isclose(v_teorica, v_p, rel_tol=5e-3), f"v_p teórica {v_teorica:.4g}"
    assert res["E_circ"] > res["E_elip"], "la órbita circular exterior debe tener más energía"
    # Valores de la solución orientativa oficial.
    for clave, oficial in (("T", 1.12e5), ("a", 5.01e7), ("r_p", 1.81e7), ("E_elip", -1.99e8), ("E_circ", -1.21e8)):
        assert math.isclose(res[clave], oficial, rel_tol=6e-3), f"{clave} no coincide con la solución oficial"
