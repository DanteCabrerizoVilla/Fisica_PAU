"""Verificación de fis2b-evau-madrid-2018-ext-b5 (segunda medida y frecuencia umbral)."""

import math

h, c, e = 6.63e-34, 3e8, 1.6e-19
lam1, Ec1, Ec2 = 700e-9, 0.45 * e, 1.49 * e


def resolver() -> dict:
    W = h * c / lam1 - Ec1
    return {"f2": (W + Ec2) / h, "f0": W / h}


def comprobar(res: dict) -> None:
    # La diferencia de energías cinéticas es h·(f2 − f1).
    f1 = c / lam1
    assert math.isclose(h * (res["f2"] - f1), Ec2 - Ec1, rel_tol=1e-12)
    assert res["f0"] < f1 < res["f2"]
