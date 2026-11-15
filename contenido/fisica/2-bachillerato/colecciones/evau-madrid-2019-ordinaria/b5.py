"""Verificación de fis2b-evau-madrid-2019-ord-b5 (plutonio-238)."""

import math

T_anios, m0, m, M, NA = 87.7, 10e-3, 2e-3, 238.0, 6.02e23
anio = 365 * 86400


def resolver() -> dict:
    lam = math.log(2) / (T_anios * anio)
    A0 = lam * m0 / M * NA
    return {"t": T_anios * math.log(m0 / m) / math.log(2), "A0": A0, "A": A0 * m / m0}


def comprobar(res: dict) -> None:
    assert math.isclose(m0 * 0.5 ** (res["t"] / T_anios), m, rel_tol=1e-12)
    lam = math.log(2) / (T_anios * anio)
    assert math.isclose(res["A0"] * math.exp(-lam * res["t"] * anio), res["A"], rel_tol=1e-12)
