"""Verificación de fis2b-evau-madrid-2024-ext-a1 (satélite en órbita elíptica de 12 h)."""

import math

# Datos del enunciado (SI)
G = 6.67e-11
M_T = 5.97e24
R_T = 6.37e6
T = 12 * 3600.0
r_a = R_T + 39700e3


def resolver() -> dict:
    a = (G * M_T * T**2 / (4 * math.pi**2)) ** (1 / 3)
    r_p = 2 * a - r_a
    v_p = math.sqrt(2 * G * M_T * r_a / (r_p * (r_a + r_p)))
    return {"h_p": r_p - R_T, "cociente": r_a / r_p, "v_p": v_p, "v_circ": math.sqrt(G * M_T / r_p)}


def comprobar(res: dict) -> None:
    r_p = res["h_p"] + R_T
    a = (r_a + r_p) / 2
    # Vis-viva en el perigeo.
    assert math.isclose(res["v_p"], math.sqrt(G * M_T * (2 / r_p - 1 / a)), rel_tol=1e-12)
    # Energía igual en perigeo y apogeo con v_a = v_p / cociente.
    v_a = res["v_p"] / res["cociente"]
    assert math.isclose(0.5 * res["v_p"] ** 2 - G * M_T / r_p, 0.5 * v_a**2 - G * M_T / r_a, rel_tol=1e-10)
    assert res["v_p"] > res["v_circ"], "en el perigeo la velocidad supera a la circular"
    # Valores de la solución orientativa oficial (redondea a a tres cifras).
    for clave, oficial, tol in (("h_p", 7.6e5, 1e-2), ("cociente", 6.46, 2e-3), ("v_p", 9.84e3, 2e-3), ("v_circ", 7.47e3, 2e-3)):
        assert math.isclose(res[clave], oficial, rel_tol=tol), f"{clave} no coincide con la solución oficial"
