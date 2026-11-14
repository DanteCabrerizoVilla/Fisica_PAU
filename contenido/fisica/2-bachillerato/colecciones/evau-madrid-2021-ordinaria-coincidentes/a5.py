"""Verificación de fis2b-evau-madrid-2021-ordc-a5 (fotoeléctrico con 500 nm y De Broglie)."""

import math

e, me, h, c = 1.6e-19, 9.1e-31, 6.63e-34, 3e8
lam, W = 500e-9, 1.8 * 1.6e-19


def resolver() -> dict:
    Ec = h * c / lam - W
    v = math.sqrt(2 * Ec / me)
    return {"Ec": Ec, "Ec_eV": Ec / e, "corte": h * c / W, "broglie": h / (me * v)}


def comprobar(res: dict) -> None:
    # Segunda vía: λ_dB = h / sqrt(2 m Ec).
    assert math.isclose(h / math.sqrt(2 * me * res["Ec"]), res["broglie"], rel_tol=1e-12)
    # En el corte, la energía cinética es nula.
    assert math.isclose(h * c / res["corte"], W, rel_tol=1e-12) and lam < res["corte"]
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["Ec"], 1.10e-19, rel_tol=3e-3) and math.isclose(res["corte"], 6.91e-7, rel_tol=1e-3)
    assert math.isclose(res["broglie"], 1.48e-9, rel_tol=3e-3)
