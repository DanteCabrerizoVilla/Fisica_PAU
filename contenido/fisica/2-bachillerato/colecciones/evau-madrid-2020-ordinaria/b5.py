"""Verificación de fis2b-evau-madrid-2020-ord-b5 (fotoeléctrico a partir de la gráfica)."""

import math

e, me, h = 1.6e-19, 9.1e-31, 6.63e-34
f0, Ec_grafica = 5e14, 2.0 * 1.6e-19


def resolver() -> dict:
    v = math.sqrt(2 * Ec_grafica / me)
    return {"W": h * f0 / e, "broglie": h / (me * v)}


def comprobar(res: dict) -> None:
    # La recta de la gráfica: 0 eV en 5e14 y 3 eV en 12,5e14 → pendiente h_graf/e.
    h_graf = 3.0 * e / (12.5e14 - 5e14)
    assert math.isclose(h_graf, 6.4e-34, rel_tol=1e-9)
    assert math.isclose(h_graf * (10e14 - f0) / e, 2.0, rel_tol=1e-9)
    # Con la h del enunciado la longitud de onda cambia un 2 %.
    alt = h / math.sqrt(2 * me * h * (10e14 - f0))
    assert math.isclose(alt, 8.54e-10, rel_tol=2e-3) and abs(alt / res["broglie"] - 1) < 0.02
    assert math.isclose(res["W"], 2.07, abs_tol=0.005) and math.isclose(res["broglie"], 8.69e-10, rel_tol=1e-3)
