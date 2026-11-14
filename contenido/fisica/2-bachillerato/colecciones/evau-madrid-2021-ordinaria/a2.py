"""Verificación de fis2b-evau-madrid-2021-ord-a2 (fuegos artificiales)."""

import math

P, t, vs, I0 = 0.02, 1.5, 340.0, 1e-12


def resolver() -> dict:
    d = vs * t
    I = P / (4 * math.pi * d**2)
    return {"d": d, "I": I, "nivel": 10 * math.log10(10 * I / I0)}


def comprobar(res: dict) -> None:
    # Diez fuentes suman exactamente 10 dB al nivel de una.
    uno = 10 * math.log10(res["I"] / I0)
    assert math.isclose(res["nivel"], uno + 10, abs_tol=1e-9)
    # Segunda vía: potencia total sobre la esfera.
    assert math.isclose(10 * P / (4 * math.pi * res["d"] ** 2), 10 * res["I"], rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert res["d"] == 510 and math.isclose(res["I"], 6.12e-9, rel_tol=2e-3)
    assert math.isclose(res["nivel"], 47.87, abs_tol=0.01)
