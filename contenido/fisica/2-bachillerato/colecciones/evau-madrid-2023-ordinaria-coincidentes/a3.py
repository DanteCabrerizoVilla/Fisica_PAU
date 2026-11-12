"""Verificación de fis2b-evau-madrid-2023-ordc-a3 (espira cuadrada que gira)."""

import math

T, B, flujo_max = 0.5, 0.4, 1.6e-2


def resolver() -> dict:
    w = 2 * math.pi / T
    return {"lado": math.sqrt(flujo_max / B), "fem_max": flujo_max * w,
            "fem_1s": round(flujo_max * w * math.sin(w * 1.0), 12)}   # sen(4π) = 0 salvo redondeo


def comprobar(res: dict) -> None:
    w = 2 * math.pi / T
    S = res["lado"] ** 2
    flujo = lambda t: B * S * math.cos(w * t)
    # Flujo máximo en t = 0 y de valor el del enunciado.
    assert math.isclose(flujo(0), flujo_max, rel_tol=1e-12)
    assert all(flujo(i * T / 1000) <= flujo(0) + 1e-15 for i in range(1000))
    # Segunda vía: la fem como derivada numérica del flujo.
    dt = 1e-7
    fem = lambda t: -(flujo(t + dt) - flujo(t - dt)) / (2 * dt)
    assert abs(fem(1.0)) < 1e-6
    maximo = max(abs(fem(i * T / 2000)) for i in range(2000))
    assert math.isclose(maximo, res["fem_max"], rel_tol=1e-5)
    # Un cuarto de periodo después del máximo de flujo, la fem es máxima.
    assert math.isclose(fem(T / 4), res["fem_max"], rel_tol=1e-6)
    assert abs(res["fem_1s"]) < 1e-12
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["lado"], 0.20, rel_tol=1e-9) and math.isclose(res["fem_max"], 0.2, rel_tol=1e-2)
