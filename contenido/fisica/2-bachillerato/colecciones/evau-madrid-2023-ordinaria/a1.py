"""Verificación de fis2b-evau-madrid-2023-ord-a1 (satélite OneWeb)."""

import math

# Datos del enunciado (SI)
G = 6.67e-11
M_T = 5.97e24
R_T = 6.37e6
m = 150.0
r = R_T + 1200e3


def resolver() -> dict:
    Ep = -G * M_T * m / r
    v = math.sqrt(G * M_T / r)
    Ec = 0.5 * m * v**2
    return {"Ep": Ep, "Ec": Ec, "dE": Ec + Ep + G * M_T * m / R_T}


def comprobar(res: dict) -> None:
    assert math.isclose(res["Ec"], -res["Ep"] / 2, rel_tol=1e-12)
    # Por partes: cinética en órbita más aumento de energía potencial.
    por_partes = res["Ec"] + G * M_T * m * (1 / R_T - 1 / r)
    assert math.isclose(res["dE"], por_partes, rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    for clave, oficial in (("Ep", -7.89e9), ("Ec", 3.95e9), ("dE", 5.44e9)):
        assert math.isclose(res[clave], oficial, rel_tol=3e-3), f"{clave} no coincide con la solución oficial"
