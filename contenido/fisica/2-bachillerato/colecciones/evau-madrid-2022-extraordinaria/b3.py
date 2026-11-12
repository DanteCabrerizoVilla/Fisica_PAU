"""Verificación de fis2b-evau-madrid-2022-ext-b3 (espira en campo variable)."""

import math

a, t0 = 0.2, 2.0
K = 2e-3
B_lineal = lambda t: K * t
B_armonico = lambda t: 3e-3 * math.cos(3 * math.pi * t)


def resolver() -> dict:
    S = a**2
    return {
        "flujo_a": B_lineal(t0) * S,
        "fem_a": -K * S,
        "flujo_b": B_armonico(t0) * S,
        "fem_b": round(3e-3 * S * 3 * math.pi * math.sin(3 * math.pi * t0), 12),   # sen(6π) = 0 salvo redondeo
    }


def comprobar(res: dict) -> None:
    S, dt = a**2, 1e-6
    # Segunda vía: la fem como derivada numérica del flujo.
    fem = lambda B, t: -(B(t + dt) - B(t - dt)) * S / (2 * dt)
    assert math.isclose(fem(B_lineal, t0), res["fem_a"], rel_tol=1e-6)
    assert abs(fem(B_armonico, t0)) < 1e-9
    # En el caso lineal la fem no depende del instante.
    assert math.isclose(fem(B_lineal, 0.3), fem(B_lineal, 7.1), rel_tol=1e-6)
    # En el armónico, t = 2 s es un máximo del flujo y la fem máxima es Φmáx·ω.
    assert all(B_armonico(t0) >= B_armonico(t0 + d) for d in (-0.05, -0.01, 0.01, 0.05))
    assert math.isclose(fem(B_armonico, t0 + 1 / 6), 1.2e-4 * 3 * math.pi, rel_tol=1e-6)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["flujo_a"], 1.6e-4) and math.isclose(res["fem_a"], -8e-5)
    assert math.isclose(res["flujo_b"], 1.2e-4) and res["fem_b"] == 0
