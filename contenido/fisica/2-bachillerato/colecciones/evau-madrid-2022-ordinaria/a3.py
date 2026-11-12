"""Verificación de fis2b-evau-madrid-2022-ord-a3 (varilla sobre raíles)."""

import math

import numpy as np

L, R = 0.2, 0.5
v = np.array([2.0, 0.0, 0.0])
B = np.array([0.0, 0.0, -0.4])


def resolver() -> dict:
    fem = abs(B[2]) * L * v[0]
    I = fem / R
    F = I * np.cross([0.0, L, 0.0], B)          # corriente hacia +y en la varilla
    return {"fem": fem, "I": I, "F": F[0]}


def comprobar(res: dict) -> None:
    # Segunda vía para la fem: fuerza de Lorentz sobre las cargas de la varilla, ε = |v × B|·L.
    campo_equivalente = np.cross(v, B)
    assert math.isclose(np.linalg.norm(campo_equivalente) * L, res["fem"], rel_tol=1e-12)
    # v × B apunta hacia +y: empuja las cargas positivas hacia arriba, corriente antihoraria.
    assert campo_equivalente[1] > 0
    # Tercera vía: derivada numérica del flujo con la superficie orientada según +z.
    flujo = lambda t: B[2] * L * (1.0 + v[0] * t)
    dt = 1e-6
    fem_con_signo = -(flujo(dt) - flujo(-dt)) / (2 * dt)
    assert math.isclose(fem_con_signo, res["fem"], rel_tol=1e-6), "positiva = antihoraria vista desde +z"
    # Balance de potencia: la que frena a la varilla es la que disipa la resistencia.
    assert res["F"] < 0
    assert math.isclose(-res["F"] * v[0], res["I"] ** 2 * R, rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["I"], 0.32) and math.isclose(res["F"], -2.56e-2)
