"""Verificación de fis2b-pau-madrid-2025-ord-1 (Eris: masa, gravedad y órbita elíptica)."""

import math

# Datos del enunciado (SI)
G = 6.67e-11
M_sol = 1.99e30
R = 2330e3 / 2
densidad = 2.5e3
r_a = 1.45e13
r_p = 5.24e12


def resolver() -> dict:
    masa = densidad * 4 / 3 * math.pi * R**3
    g = G * masa / R**2
    a = (r_a + r_p) / 2
    energia = -G * M_sol * masa / (2 * a)
    v_p = math.sqrt(2 * G * M_sol * (1 / r_p - 1 / (2 * a)))
    return {"masa": masa, "g": g, "energia": energia, "v_p": v_p}


def comprobar(res: dict) -> None:
    # g directamente con la densidad: g = (4/3) π G ρ R.
    assert math.isclose(res["g"], 4 / 3 * math.pi * G * densidad * R, rel_tol=1e-12)
    # Segunda vía para v_p: conservación del momento angular y de la energía entre perihelio y afelio.
    v_a = math.sqrt(2 * G * M_sol * r_p / (r_a * (r_a + r_p)))
    v_p = v_a * r_a / r_p
    assert math.isclose(res["v_p"], v_p, rel_tol=1e-12), "v_p no coincide con la vía del momento angular"
    # La energía en el afelio con esa velocidad es la misma.
    e_afelio = 0.5 * res["masa"] * v_a**2 - G * M_sol * res["masa"] / r_a
    assert math.isclose(e_afelio, res["energia"], rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    for clave, oficial, tol in (("masa", 1.66e22, 3e-3), ("g", 0.82, 1e-2), ("energia", -1.11e29, 4e-3), ("v_p", 6.1e3, 1e-2)):
        assert math.isclose(res[clave], oficial, rel_tol=tol), f"{clave} no coincide con la solución oficial"
