"""Verificación de fis2b-evau-madrid-2021-ordc-b4 (foco en el fondo de una piscina)."""

import math

h, l_agua, l_aire = 3.0, 680e-9, 904.4e-9


def resolver() -> dict:
    n = l_aire / l_agua
    return {"n": n, "r": h * math.tan(math.asin(1 / n))}


def comprobar(res: dict) -> None:
    n = res["n"]
    # Segunda vía: un rayo que llega al borde del disco incide justo con el ángulo límite.
    sen = res["r"] / math.hypot(res["r"], h)
    assert math.isclose(n * sen, 1, rel_tol=1e-12)
    # Un poco más allá del borde, reflexión total; un poco más cerca, sale.
    sale = lambda x: n * x / math.hypot(x, h) < 1
    assert sale(res["r"] * 0.99) and not sale(res["r"] * 1.01)
    # Valores de la solución orientativa oficial.
    assert math.isclose(n, 1.33, rel_tol=1e-4) and math.isclose(res["r"], 3.42, rel_tol=1e-3)
