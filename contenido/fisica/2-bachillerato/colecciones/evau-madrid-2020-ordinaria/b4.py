"""Verificación de fis2b-evau-madrid-2020-ord-b4 (placa de vidrio entre dos aceites)."""

import math

import numpy as np

n1, n2, n3, e = 1.4, 1.5, 1.2, 4.0
inc = math.radians(30)


def resolver() -> dict:
    b = math.asin(n1 * math.sin(inc) / n2)
    return {"d": 2 * e * math.tan(b) * math.cos(inc), "angulo": math.degrees(math.asin(n3 / n1))}


def comprobar(res: dict) -> None:
    # Segunda vía: geometría vectorial. Rayo reflejado desde (0, 0); el otro sale en (2x, 0).
    b = math.asin(n1 * math.sin(inc) / n2)
    salida = np.array([2 * e * math.tan(b), 0.0])
    u = np.array([math.sin(inc), math.cos(inc)])            # dirección de los dos rayos que suben
    dist = abs(u[0] * salida[1] - u[1] * salida[0])          # |u × salida| en 2D
    assert math.isclose(dist, res["d"], rel_tol=1e-12)
    # Reflexión total en la cara inferior justo a partir del ángulo calculado.
    total = lambda grados: n1 * math.sin(math.radians(grados)) / n3 >= 1
    assert not total(res["angulo"] - 0.01) and total(res["angulo"] + 0.01)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["d"], 3.66, rel_tol=2e-3) and math.isclose(res["angulo"], 59, abs_tol=0.05)
