"""Verificación de fis2b-pau-madrid-2027-mod-2b (órbita elíptica de Plutón)."""

import math

# Datos del enunciado (SI)
G = 6.67e-11
M = 1.99e30
T = 248 * 365 * 24 * 3600
e = 0.244


def resolver() -> dict:
    a = (G * M * T**2 / (4 * math.pi**2)) ** (1 / 3)
    c = e * a
    r_p, r_a = a - c, a + c
    v_a = math.sqrt(2 * G * M * r_p / (r_a * (r_a + r_p)))
    v_p = v_a * r_a / r_p
    return {"r_a": r_a, "r_p": r_p, "v_a": v_a, "v_p": v_p}


def comprobar(res: dict) -> None:
    r_a, r_p, v_a, v_p = res["r_a"], res["r_p"], res["v_a"], res["v_p"]
    # Conservación de la energía mecánica por unidad de masa.
    assert math.isclose(0.5 * v_a**2 - G * M / r_a, 0.5 * v_p**2 - G * M / r_p, rel_tol=1e-10), \
        "la energía no se conserva entre afelio y perihelio"
    # Segunda vía: ecuación vis-viva, v² = GM (2/r − 1/a).
    a = (r_a + r_p) / 2
    assert math.isclose(v_a, math.sqrt(G * M * (2 / r_a - 1 / a)), rel_tol=1e-10), "v_a no cumple vis-viva"
    assert math.isclose(v_p, math.sqrt(G * M * (2 / r_p - 1 / a)), rel_tol=1e-10), "v_p no cumple vis-viva"
    # El periodo que corresponde a ese semieje es el del enunciado.
    assert math.isclose(2 * math.pi * math.sqrt(a**3 / (G * M)), T, rel_tol=1e-10)
    # Valores de la solución orientativa oficial (tres cifras).
    for clave, oficial in (("r_a", 7.34e12), ("r_p", 4.46e12), ("v_a", 3.69e3), ("v_p", 6.08e3)):
        assert math.isclose(res[clave], oficial, rel_tol=5e-3), f"{clave} no coincide con la solución oficial"
