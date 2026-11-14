"""Verificación de fis2b-evau-madrid-2021-ext-a5 (electrón a 0,75 c y fotón de 15 MeV)."""

import math

e, m0, h, c = 1.6e-19, 9.1e-31, 6.63e-34, 3e8
beta, E_foton = 0.75, 15e6 * 1.6e-19


def resolver() -> dict:
    m = m0 / math.sqrt(1 - beta**2)
    return {"m": m, "Ec": (m - m0) * c**2, "l_foton": h * c / E_foton, "l_electron": h / (m * beta * c)}


def comprobar(res: dict) -> None:
    # Segunda vía: p a partir de E² = (pc)² + (m0c²)².
    E = res["Ec"] + m0 * c**2
    p = math.sqrt(E**2 - (m0 * c**2) ** 2) / c
    assert math.isclose(h / p, res["l_electron"], rel_tol=1e-9)
    # El fotón: p = E/c y λ = h/p.
    assert math.isclose(h / (E_foton / c), res["l_foton"], rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["m"], 1.38e-30, rel_tol=5e-3) and math.isclose(res["Ec"], 4.19e-14, rel_tol=1e-3)
    assert math.isclose(res["l_foton"], 8.29e-14, rel_tol=1e-3) and math.isclose(res["l_electron"], 2.14e-12, rel_tol=2e-3)
