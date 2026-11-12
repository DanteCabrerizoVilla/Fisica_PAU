"""Verificación de fis2b-evau-madrid-2022-ord-b4 (lámina de vidrio sobre un líquido)."""

import math

n_aire = 1.0
fraccion = 0.70
limite = 30.0


def resolver() -> dict:
    return {"n_vidrio": n_aire / fraccion, "n_liquido": n_aire / math.sin(math.radians(limite))}


def paso(n1, n2, grados):
    s = n1 * math.sin(math.radians(grados)) / n2
    return None if s > 1 else math.degrees(math.asin(min(s, 1.0)))


def comprobar(res: dict) -> None:
    nv, nl = res["n_vidrio"], res["n_liquido"]

    def sale(grados):
        en_vidrio = paso(nl, nv, grados)
        return en_vidrio is not None and paso(nv, n_aire, en_vidrio) is not None

    # Segunda vía: superficie a superficie. Por debajo de 30° sale; por encima, no.
    assert sale(29.9) and not sale(30.1) and sale(5) and not sale(40)
    # A 30,1° el rayo sí entra en el vidrio: la reflexión total es en la cara superior.
    assert paso(nl, nv, 30.1) is not None
    # El ángulo en el vidrio en el límite coincide con el ángulo límite vidrio-aire.
    assert math.isclose(paso(nl, nv, 29.999999), math.degrees(math.asin(1 / nv)), abs_tol=1e-4)
    # Longitud de onda: con la misma frecuencia, λ = c/(n f).
    c, f = 3e8, 5e14
    assert math.isclose((c / (nv * f)) / (c / (n_aire * f)), fraccion, rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(nv, 1.43, rel_tol=1e-2) and math.isclose(nl, 2.0, rel_tol=1e-12)
