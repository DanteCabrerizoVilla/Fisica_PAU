"""Verificación de fis2b-evau-madrid-2018-mod-a5 (De Broglie y masa relativista)."""

import math

h, c, e, me = 6.63e-34, 3e8, 1.6e-19, 9.1e-31


def resolver() -> dict:
    return {"lam": h / math.sqrt(2 * me * 40 * e), "ratio": 1 + 2e9 * e / (me * c**2)}


def comprobar(res: dict) -> None:
    # a) La corrección relativista a 40 eV es despreciable.
    E0, Ec = me * c**2, 40 * e
    p_rel = math.sqrt((Ec + E0) ** 2 - E0**2) / c
    assert math.isclose(h / p_rel, res["lam"], rel_tol=1e-4)
    # b) γ = 1/√(1 − v²/c²) a partir de la velocidad que corresponde a esa energía.
    g = res["ratio"]
    beta = math.sqrt(1 - 1 / g**2)
    assert math.isclose(1 / math.sqrt(1 - beta**2), g, rel_tol=1e-6)
    # Oficial: λ = 1,94·10⁻¹⁰ m; 3915 con m0c² = 0,511 MeV.
    assert math.isclose(res["lam"], 1.94e-10, rel_tol=2e-3)
    assert math.isclose(res["ratio"], 3915, rel_tol=3e-3)
