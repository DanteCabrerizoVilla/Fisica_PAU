"""Verificación de fis2b-evau-madrid-2020-mod-a5 (fotoeléctrico con luz de 400 nm)."""

import math

h, c, e, me = 6.63e-34, 3e8, 1.6e-19, 9.1e-31
lam, W, I = 400e-9, 2.5 * e, 5e-9


def resolver() -> dict:
    Ef = h * c / lam
    Ec = Ef - W
    n = I / Ef
    return {"Ec": Ec, "lamdB": h / math.sqrt(2 * me * Ec), "n": n, "Ie": n * Ec}


def comprobar(res: dict) -> None:
    v = math.sqrt(2 * res["Ec"] / me)
    assert math.isclose(h / (me * v), res["lamdB"], rel_tol=1e-12)
    assert math.isclose(res["Ie"] / I, res["Ec"] / (h * c / lam), rel_tol=1e-12)
    # Oficial: Ec = 9,725·10⁻²⁰ J; λ = 1,583·10⁻⁹ m (el cociente correcto es 1,576·10⁻⁹);
    # n = 1,005·10¹⁰; Ie = 9,78·10⁻¹⁰ W/m².
    assert math.isclose(res["Ec"], 9.725e-20, rel_tol=1e-9) and math.isclose(res["lamdB"], 1.576e-9, rel_tol=1e-3)
    assert math.isclose(res["n"], 1.005e10, rel_tol=1e-3) and math.isclose(res["Ie"], 9.78e-10, rel_tol=1e-3)
