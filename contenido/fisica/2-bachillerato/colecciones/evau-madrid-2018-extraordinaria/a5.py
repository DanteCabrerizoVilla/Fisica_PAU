"""Verificación de fis2b-evau-madrid-2018-ext-a5 (carbono-14)."""

import math

T, m0, m, M, NA = 5730.0, 2e-3, 0.5e-3, 14.0, 6.02e23
anio = 365 * 86400


def resolver() -> dict:
    lam = math.log(2) / (T * anio)
    return {"t": T * math.log2(m0 / m), "A0": lam * m0 / M * NA}


def comprobar(res: dict) -> None:
    lam_anio = math.log(2) / T
    assert math.isclose(m0 * math.exp(-lam_anio * res["t"]), m, rel_tol=1e-12)
