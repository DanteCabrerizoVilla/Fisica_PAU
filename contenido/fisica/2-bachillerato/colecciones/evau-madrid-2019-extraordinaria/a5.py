"""Verificación de fis2b-evau-madrid-2019-ext-a5 (h y W a partir de dos medidas)."""

import math
import numpy as np

e, me, c = 1.6e-19, 9.1e-31, 3e8
l1, Ec1, l2, Ec2 = 589e-9, 0.577 * e, 179.76e-9, 5.38 * e


def resolver() -> dict:
    h = (Ec2 - Ec1) / (c * (1 / l2 - 1 / l1))
    W = h * c / l1 - Ec1
    return {"h": h, "W": W, "lam": h / math.sqrt(2 * me * Ec2)}


def comprobar(res: dict) -> None:
    # Sistema lineal en (h, W): h·c/λ − W = Ec.
    A = np.array([[c / l1, -1], [c / l2, -1]])
    h, W = np.linalg.solve(A, [Ec1, Ec2])
    assert math.isclose(h, res["h"], rel_tol=1e-10) and math.isclose(W, res["W"], rel_tol=1e-10)
    v = math.sqrt(2 * Ec2 / me)
    assert math.isclose(res["h"] / (me * v), res["lam"], rel_tol=1e-12)
