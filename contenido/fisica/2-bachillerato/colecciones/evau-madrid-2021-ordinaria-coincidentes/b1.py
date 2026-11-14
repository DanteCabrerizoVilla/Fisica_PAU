"""Verificación de fis2b-evau-madrid-2021-ordc-b1 (51 Pegasi b)."""

import math

G, MS, MJ = 6.67e-11, 1.99e30, 1.90e27
TJ, TP = 12 * 365 * 86400, 4 * 86400


def resolver() -> dict:
    RJ = (G * MS * TJ**2 / (4 * math.pi**2)) ** (1 / 3)
    RP = RJ / 100
    M = 4 * math.pi**2 * RP**3 / (G * TP**2)
    return {"M": M, "E": -G * M * 51 * MJ / (2 * RP)}


def comprobar(res: dict) -> None:
    # Segunda vía, con cocientes: M*/MS = (RP/RJ)³ (TJ/TP)².
    assert math.isclose(res["M"], MS * (1 / 100) ** 3 * (TJ / TP) ** 2, rel_tol=1e-12)
    # Con esa masa, el periodo del exoplaneta sale 4 días.
    RP = (G * MS * TJ**2 / (4 * math.pi**2)) ** (1 / 3) / 100
    assert math.isclose(2 * math.pi * math.sqrt(RP**3 / (G * res["M"])), TP, rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["M"], 2.39e30, rel_tol=2e-3) and math.isclose(res["E"], -9.85e38, rel_tol=2e-3)
