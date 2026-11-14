"""Verificación de fis2b-evau-madrid-2021-ordc-b3 (solenoide y espira interior)."""

import math

MU0 = 4e-7 * math.pi
L, N, R, flujo = 0.5, 1000, 0.05, 50e-3
r, dt = 0.02, 5e-3


def resolver() -> dict:
    B = flujo / (N * math.pi * R**2)
    I = B * L / (MU0 * N)
    return {"I": I, "fem": B * math.pi * r**2 / dt}


def comprobar(res: dict) -> None:
    # Con la corriente obtenida se recupera el flujo del enunciado.
    B = MU0 * N / L * res["I"]
    assert math.isclose(N * B * math.pi * R**2, flujo, rel_tol=1e-12)
    # Segunda vía: derivada numérica del flujo en la espira con I(t) lineal.
    flujo_e = lambda t: MU0 * N / L * res["I"] * (1 - t / dt) * math.pi * r**2
    assert math.isclose(-(flujo_e(0.003) - flujo_e(0.002)) / 0.001, res["fem"], rel_tol=1e-9)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["I"], 2.53, rel_tol=2e-3) and math.isclose(res["fem"], 1.59e-3, rel_tol=1e-2)
