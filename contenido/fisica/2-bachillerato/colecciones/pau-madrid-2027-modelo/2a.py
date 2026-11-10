"""Verificación de fis2b-pau-madrid-2027-mod-2a (planeta extrasolar G-876d)."""

import math

# Datos del enunciado (SI)
G = 6.67e-11
M_T = 5.97e24
R_T = 6.37e6
M_p = 6 * M_T
R_p = 1.73 * R_T
r = 3.14e6 * 1e3
M_e = 6.37e29


def resolver() -> dict:
    g = G * M_p / R_p**2
    v = math.sqrt(G * M_e / r)
    T = 2 * math.pi * r / v
    E = 0.5 * M_p * v**2 - G * M_e * M_p / r
    return {"g": g, "v": v, "T": T, "E": E}


def comprobar(res: dict) -> None:
    # Gravedad por proporcionalidad con la de la Tierra.
    g_T = G * M_T / R_T**2
    assert math.isclose(res["g"], g_T * 6 / 1.73**2, rel_tol=1e-12), "g no escala como M/R²"
    # Periodo por la tercera ley de Kepler.
    T_kepler = 2 * math.pi * math.sqrt(r**3 / (G * M_e))
    assert math.isclose(res["T"], T_kepler, rel_tol=1e-12), "el periodo no cumple la tercera ley"
    # Energía mecánica de la órbita circular: mitad de la potencial.
    assert math.isclose(res["E"], -G * M_e * M_p / (2 * r), rel_tol=1e-12), "Em distinta de Ep/2"
    # Valores de la solución orientativa oficial (tres cifras).
    for clave, oficial in (("g", 19.7), ("v", 1.16e5), ("T", 1.70e5), ("E", -2.42e35)):
        assert math.isclose(res[clave], oficial, rel_tol=5e-3), f"{clave} no coincide con la solución oficial"
