"""Verificación de fis2b-evau-madrid-2019-mod-a2 (explosión en una mina)."""

import math

I1, r1, r2, I0 = 100.0, 20.0, 1000.0, 1e-12


def resolver() -> dict:
    P = I1 * 4 * math.pi * r1**2
    return {"P": P, "beta": 10 * math.log10(P / (4 * math.pi * r2**2) / I0)}


def comprobar(res: dict) -> None:
    # Por niveles: la distancia se multiplica por 50, el nivel baja 20·log(50) dB.
    beta1 = 10 * math.log10(I1 / I0)
    assert math.isclose(res["beta"], beta1 - 20 * math.log10(r2 / r1), rel_tol=1e-12)
    # Oficial: P = 5,03·10⁵ W, β = 106,02 dB.
    assert math.isclose(res["P"], 5.03e5, rel_tol=1e-3) and math.isclose(res["beta"], 106.02, rel_tol=1e-4)
