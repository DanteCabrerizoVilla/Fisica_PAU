"""Verificación de fis2b-pau-madrid-2025-ord-4a (fotones UV absorbidos por el ozono)."""

import math

# Datos del enunciado (SI)
e = 1.6e-19
h = 6.63e-34
c = 3e8
longitud = 260e-9
flujo = 2.6e14
t = 30 * 60


def resolver() -> dict:
    E_foton = h * c / longitud
    potencia = flujo * E_foton
    return {"energia": E_foton / e, "potencia": potencia, "recibida": potencia * t}


def comprobar(res: dict) -> None:
    # Segunda vía: contar los fotones que llegan en media hora y sumar su energía en eV.
    fotones = flujo * t
    assert math.isclose(fotones * res["energia"] * e, res["recibida"], rel_tol=1e-12)
    # hc en eV·nm (1243 con los datos del enunciado) entre la longitud de onda en nm.
    assert math.isclose(res["energia"], (h * c / e * 1e9) / 260, rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    for clave, oficial in (("energia", 4.78), ("potencia", 1.99e-4), ("recibida", 0.358)):
        assert math.isclose(res[clave], oficial, rel_tol=2e-3), f"{clave} no coincide con la solución oficial"
