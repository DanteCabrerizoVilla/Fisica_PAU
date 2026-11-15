"""Verificación de fis2b-evau-madrid-2019-ext-b5 (datación con carbono-14)."""

import math

t, queda, m, M, NA = 3200.0, 0.68, 8e-6, 14.0, 6.02e23
anio = 365 * 86400


def resolver() -> dict:
    lam = -math.log(queda) / t
    return {"tau": 1 / lam, "T": math.log(2) / lam, "A": lam / anio * m / M * NA}


def comprobar(res: dict) -> None:
    assert math.isclose(0.5 ** (t / res["T"]), queda, rel_tol=1e-12)
    assert math.isclose(math.exp(-t / res["tau"]), queda, rel_tol=1e-12)
