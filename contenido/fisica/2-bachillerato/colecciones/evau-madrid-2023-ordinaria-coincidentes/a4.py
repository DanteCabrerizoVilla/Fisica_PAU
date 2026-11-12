"""Verificación de fis2b-evau-madrid-2023-ordc-a4 (lente: imagen virtual y después real)."""

import math

sA, y, yA = -3.0, 2.0, 3.0
sB = -18.0


def resolver() -> dict:
    spA = (yA / y) * sA
    f = 1 / (1 / spA - 1 / sA)
    spB = 1 / (1 / f + 1 / sB)
    return {"f": f, "M": spB / sB}


def cruce(f, s, altura):
    """Segunda vía: cortar dos rayos principales (paralelo y central) trazados como rectas."""
    # Rayo 1: sale de la lente a la altura del objeto y pasa por F' (f, 0).
    m1, b1 = -altura / f, altura
    # Rayo 2: pasa por el centro de la lente.
    m2, b2 = altura / s, 0.0
    x = (b2 - b1) / (m1 - m2)
    return x, m1 * x + b1


def comprobar(res: dict) -> None:
    f = res["f"]
    xA, hA = cruce(f, sA, y)
    assert math.isclose(xA, -4.5, rel_tol=1e-9) and math.isclose(hA, yA, rel_tol=1e-9)
    assert xA < 0, "en A la imagen es virtual: se cortan las prolongaciones, a la izquierda"
    xB, hB = cruce(f, sB, y)
    assert math.isclose(xB, 18, rel_tol=1e-9) and math.isclose(hB / y, res["M"], rel_tol=1e-9)
    assert xB > 0 and hB < 0, "en B la imagen es real e invertida"
    # El objeto a 2f da la imagen a 2f con aumento −1.
    assert math.isclose(-sB, 2 * f)
    # Valores de la solución orientativa oficial.
    assert math.isclose(f, 9) and math.isclose(res["M"], -1)
