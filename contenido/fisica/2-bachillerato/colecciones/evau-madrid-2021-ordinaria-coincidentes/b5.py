"""Verificación de fis2b-evau-madrid-2021-ordc-b5 (radio-226)."""

import math

NA, M, e = 6.02e23, 226.0, 1.6e-19
T, masa, t, E_alfa = 1590.0, 1e-3, 10.0, 3e6 * 1.6e-19


def resolver() -> dict:
    lam = math.log(2) / T
    N0 = masa / M * NA
    return {"tau": 1 / lam, "reduccion": 100 * (1 - math.exp(-1)),
            "E": N0 * -math.expm1(-lam * t) * E_alfa}


def comprobar(res: dict) -> None:
    lam = 1 / res["tau"]
    assert math.isclose(math.exp(-lam * res["tau"]), math.exp(-1))
    # Segunda vía: integrar la actividad (en desintegraciones/año) durante 10 años.
    N0 = masa / M * NA
    n = 10000
    total = sum(lam * N0 * math.exp(-lam * (i + 0.5) * t / n) * t / n for i in range(n))
    assert math.isclose(total * E_alfa, res["E"], rel_tol=1e-8)
    # Valores de la solución orientativa oficial (su 5760 J viene de redondear ΔN a 1,2e16).
    assert math.isclose(res["tau"], 2293.58, rel_tol=1e-3) and math.isclose(res["reduccion"], 63, abs_tol=0.5)
    assert math.isclose(res["E"], 5760, rel_tol=0.04)
