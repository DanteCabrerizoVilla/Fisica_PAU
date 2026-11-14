"""Verificación de fis2b-evau-madrid-2021-ordc-a2 (onda con aceleración máxima en el origen)."""

import math

v, A, w = 2.0, 0.02, math.pi / 2


def resolver() -> dict:
    k = w / v
    return {"v": A * w * math.cos(w * 10 - k * 3 - math.pi / 2)}


def comprobar(res: dict) -> None:
    k = w / v
    y = lambda x, t: A * math.sin(w * t - k * x - math.pi / 2)
    dt = 1e-4
    acel = lambda x, t: (y(x, t + dt) - 2 * y(x, t) + y(x, t - dt)) / dt**2
    # En el origen, en t = 0, la aceleración es la máxima posible y positiva.
    assert math.isclose(acel(0, 0), A * w**2, rel_tol=1e-6)
    # Derivada numérica de la elongación en (3 m, 10 s).
    assert math.isclose((y(3, 10 + 1e-7) - y(3, 10 - 1e-7)) / 2e-7, res["v"], rel_tol=1e-6)
    # Viaja hacia +x a 2 m/s.
    assert math.isclose(y(1.0, 2.0), y(1.0 + v * 0.5, 2.5), abs_tol=1e-12)
    # Valor de la solución orientativa oficial.
    assert math.isclose(res["v"], 0.022, rel_tol=1e-2)
