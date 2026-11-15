"""Verificación de fis2b-evau-madrid-2018-mod-b5 (h y W a partir de dos potenciales de frenado)."""

import math
import numpy as np

e, c = 1.6e-19, 3e8
f1, V1, f2, V2 = 9e14, 0.6, c / 2.38e-7, 2.1


def resolver() -> dict:
    h = e * (V2 - V1) / (f2 - f1)
    return {"h": h, "W": h * f1 - e * V1}


def comprobar(res: dict) -> None:
    h, W = np.linalg.solve([[f1, -1], [f2, -1]], [e * V1, e * V2])
    assert math.isclose(h, res["h"], rel_tol=1e-10) and math.isclose(W, res["W"], rel_tol=1e-10)
    # Oficial: h = 6,66·10⁻³⁴ J s, W = 5,03·10⁻¹⁹ J.
    assert math.isclose(res["h"], 6.66e-34, rel_tol=1e-3)
