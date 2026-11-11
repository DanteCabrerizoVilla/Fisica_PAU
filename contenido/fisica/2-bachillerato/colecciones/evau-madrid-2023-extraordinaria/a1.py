"""Verificación de fis2b-evau-madrid-2023-ext-a1 (satélite UPM-Sat2)."""

import math

# Datos del enunciado (SI)
G = 6.67e-11
M_T = 5.97e24
R_T = 6.37e6
T = 5710.0
m = 50.0


def resolver() -> dict:
    r = (G * M_T * T**2 / (4 * math.pi**2)) ** (1 / 3)
    dE = -G * M_T * m / (2 * r) + G * M_T * m / R_T
    v = 2 * math.pi * r / T
    return {"h": r - R_T, "dE": dE, "v": v, "a": v**2 / r}


def comprobar(res: dict) -> None:
    r = res["h"] + R_T
    # Velocidad por la dinámica y aceleración igual a la gravedad a esa altura.
    assert math.isclose(res["v"], math.sqrt(G * M_T / r), rel_tol=1e-10)
    assert math.isclose(res["a"], G * M_T / r**2, rel_tol=1e-10)
    # Energía: cinética en órbita más el aumento de potencial.
    por_partes = 0.5 * m * res["v"] ** 2 + G * M_T * m * (1 / R_T - 1 / r)
    assert math.isclose(res["dE"], por_partes, rel_tol=1e-10)
    # Valores de la solución orientativa oficial.
    for clave, oficial in (("h", 5.32e5), ("dE", 1.68e9), ("v", 7595.4), ("a", 8.35)):
        assert math.isclose(res[clave], oficial, rel_tol=3e-3), f"{clave} no coincide con la solución oficial"
