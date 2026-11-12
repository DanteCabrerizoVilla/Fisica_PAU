"""Verificación de fis2b-evau-madrid-2023-ord-b5 (constante de Planck con dos potenciales de frenado)."""

import math

import numpy as np

# Datos del enunciado
c = 3e8
e = 1.6e-19
l1, V1 = 379e-9, 2.5
l2, V2 = 544e-9, 1.5
I_max = 10.0          # pA, leído de la gráfica para 379 nm


def resolver() -> dict:
    h = e * (V1 - V2) / (c * (1 / l1 - 1 / l2))
    return {"h": h, "V": V1, "I": I_max / 2}


def comprobar(res: dict) -> None:
    # Segunda vía: resolver el sistema de dos ecuaciones con incógnitas h y W0.
    #   h·c/λ − W0 = e·V
    M = np.array([[c / l1, -1.0], [c / l2, -1.0]])
    h, W0 = np.linalg.solve(M, np.array([e * V1, e * V2]))
    assert math.isclose(h, res["h"], rel_tol=1e-9)
    assert W0 > 0, "el trabajo de extracción debe ser positivo"
    # Con ese h y ese W0 se recuperan los dos potenciales de frenado.
    assert math.isclose((h * c / l1 - W0) / e, V1, rel_tol=1e-9)
    assert math.isclose((h * c / l2 - W0) / e, V2, rel_tol=1e-9)
    # Tercera vía: pendiente de la recta V_f frente a la frecuencia, que vale h/e.
    pendiente = (V1 - V2) / (c / l1 - c / l2)
    assert math.isclose(pendiente * e, res["h"], rel_tol=1e-9)
    # El potencial de frenado no depende de la intensidad; la corriente es proporcional a ella.
    assert res["V"] == V1 and math.isclose(res["I"], 0.5 * I_max)
    # Cerca del valor aceptado y del de la solución orientativa oficial.
    assert math.isclose(res["h"], 6.626e-34, rel_tol=0.01)
    assert math.isclose(res["h"], 6.66e-34, rel_tol=2e-3)
    # El trabajo de extracción que se usa en el enlace a la simulación.
    assert math.isclose(W0 / e, 0.797, abs_tol=0.002)
