"""Verificación de fis2b-evau-madrid-2021-mod-b1 (planeta de 360 masas terrestres)."""

import math

masa, escape = 360.0, 6.0


def resolver() -> dict:
    radios = masa / escape**2
    return {"radios": radios, "gravedades": masa / radios**2}


def comprobar(res: dict) -> None:
    G, MT, RT = 6.67e-11, 5.97e24, 6.37e6
    MP, RP = masa * MT, res["radios"] * RT
    ve = lambda M, R: math.sqrt(2 * G * M / R)
    assert math.isclose(ve(MP, RP) / ve(MT, RT), escape, rel_tol=1e-12)
    assert math.isclose((G * MP / RP**2) / (G * MT / RT**2), res["gravedades"], rel_tol=1e-12)
    assert math.isclose(res["radios"], 10) and math.isclose(res["gravedades"], 3.6)
