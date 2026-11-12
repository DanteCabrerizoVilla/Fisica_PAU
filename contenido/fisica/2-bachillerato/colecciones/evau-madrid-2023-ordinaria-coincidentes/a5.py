"""Verificación de fis2b-evau-madrid-2023-ordc-a5 (fotoeléctrico en magnesio y De Broglie)."""

import math

c, e, h, m = 3e8, 1.6e-19, 6.63e-34, 9.1e-31
umbral = 339e-9
f1 = 1.0e15
broglie = 0.87e-9


def resolver() -> dict:
    W = h * c / umbral
    v = h / (m * broglie)
    return {"Ec": (h * f1 - W) / e, "f": (W + 0.5 * m * v**2) / h}


def comprobar(res: dict) -> None:
    W = h * c / umbral
    # Segunda vía para a): con frecuencias, Ec = h (f − f0).
    f0 = c / umbral
    assert f1 > f0, "debe haber emisión"
    assert math.isclose(h * (f1 - f0) / e, res["Ec"], rel_tol=1e-9)
    # Segunda vía para b): Ec = p²/(2m) con p = h/λ, y de ahí la frecuencia.
    p = h / broglie
    Ec2 = p**2 / (2 * m)
    assert math.isclose(f0 + Ec2 / h, res["f"], rel_tol=1e-9)
    # Camino inverso: con esa frecuencia, la longitud de onda de De Broglie es la del enunciado.
    Ec = h * res["f"] - W
    assert math.isclose(h / math.sqrt(2 * m * Ec), broglie, rel_tol=1e-9)
    # El electrón no es relativista.
    assert h / (m * broglie) < 0.01 * c
    # Valores de la solución orientativa oficial (que trunca a 0,47 eV).
    assert math.isclose(res["Ec"], 0.47, abs_tol=0.01)
    assert math.isclose(res["f"], 1.37e15, rel_tol=5e-3)
