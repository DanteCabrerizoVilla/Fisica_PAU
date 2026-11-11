"""Verificación de fis2b-evau-madrid-2023-ext-b5 (corriente fotoeléctrica y energía recibida)."""

import math

# Datos del enunciado (SI)
c = 3e8
e = 1.6e-19
h = 6.63e-34
longitud = 400e-9
corriente = 15e-9
V_frenado = 1.0
t = 3600.0


def resolver() -> dict:
    E_foton = h * c / longitud
    return {"W": (E_foton - e * V_frenado) / e, "E": corriente / e * E_foton * t}


def comprobar(res: dict) -> None:
    # Segunda vía: carga total en una hora -> número de fotones -> energía en eV -> julios.
    fotones = corriente * t / e
    energia_eV = fotones * (h * c / longitud / e)
    assert math.isclose(energia_eV * e, res["E"], rel_tol=1e-12)
    assert math.isclose(res["E"] / t, 4.7e-8, rel_tol=1e-2)
    # El fotón de 400 nm tiene 3,11 eV: 2,11 de extracción y 1 de energía cinética.
    assert math.isclose(res["W"] + V_frenado, h * c / longitud / e, rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["W"], 2.11, rel_tol=2e-3) and math.isclose(res["E"], 1.68e-4, rel_tol=2e-3)
