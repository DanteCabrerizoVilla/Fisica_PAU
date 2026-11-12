"""Verificación de fis2b-evau-madrid-2022-ext-b4 (aire, aceite y agua)."""

import math

n_aire, n_aceite, n_agua = 1.0, 1.44, 1.33


def resolver() -> dict:
    agua = math.asin(n_aire * math.sin(math.radians(40)) / n_agua)
    return {"agua": math.degrees(agua), "limite": math.degrees(math.asin(n_aire / n_agua))}


def paso(n1, n2, grados):
    """Refracción en una superficie; None si hay reflexión total."""
    s = n1 * math.sin(math.radians(grados)) / n2
    return None if s >= 1 else math.degrees(math.asin(s))


def comprobar(res: dict) -> None:
    # Segunda vía: superficie a superficie, pasando por el aceite.
    aceite = paso(n_aire, n_aceite, 40)
    assert math.isclose(aceite, 26.51, abs_tol=0.01)
    assert math.isclose(paso(n_aceite, n_agua, aceite), res["agua"], abs_tol=1e-9)
    # Hacia arriba: justo por debajo del límite sale; justo por encima, no.
    def sale(grados):
        en_aceite = paso(n_agua, n_aceite, grados)
        assert en_aceite is not None, "del agua al aceite nunca hay reflexión total"
        return paso(n_aceite, n_aire, en_aceite) is not None
    assert sale(res["limite"] - 0.01) and not sale(res["limite"] + 0.01)
    assert sale(10) and not sale(60)
    # El resultado no depende del índice del aceite.
    for n in (1.2, 1.44, 1.7):
        assert math.isclose(paso(n, n_agua, paso(n_aire, n, 40)), res["agua"], abs_tol=1e-9)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["agua"], 28.90, abs_tol=0.01) and math.isclose(res["limite"], 48.75, abs_tol=0.01)
