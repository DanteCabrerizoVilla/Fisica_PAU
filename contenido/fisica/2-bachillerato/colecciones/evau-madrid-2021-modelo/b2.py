"""Verificación de fis2b-evau-madrid-2021-mod-b2 (umbrales de audición y de dolor)."""

import math

I0 = 1e-12
audicion_100, dolor_10k = 40.0, 120.0
P_trueno, d_sirena = 4.0, 5.0


def resolver() -> dict:
    Ia = I0 * 10 ** (audicion_100 / 10)
    Id = I0 * 10 ** (dolor_10k / 10)
    return {"d": math.sqrt(P_trueno / (4 * math.pi * Ia)), "P": Id * 4 * math.pi * d_sirena**2}


def comprobar(res: dict) -> None:
    nivel = lambda P, d: 10 * math.log10(P / (4 * math.pi * d**2) / I0)
    assert math.isclose(nivel(P_trueno, res["d"]), audicion_100, abs_tol=1e-9)
    assert math.isclose(nivel(res["P"], d_sirena), dolor_10k, abs_tol=1e-9)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["d"], 5642, rel_tol=1e-4) and math.isclose(res["P"], 314, rel_tol=2e-3)
