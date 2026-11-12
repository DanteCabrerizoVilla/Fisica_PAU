"""Verificación de fis2b-evau-madrid-2022-mod-b4 (dos rayos de distinto índice en un vidrio)."""

import math

import numpy as np

c = 3e8
incidencia, espesor = math.radians(40), 20.0     # cm
n1, n2 = 1.61, 1.67
f = 4.21e14


def avance(n):
    return espesor * math.tan(math.asin(math.sin(incidencia) / n))


def resolver() -> dict:
    return {"separacion": avance(n1) - avance(n2), "longitud": c / (n1 * f)}


def punto_salida(n):
    """Segunda vía: trazado vectorial. Devuelve la abscisa del punto de salida (cm)."""
    d = np.array([math.sin(incidencia), -math.cos(incidencia)])     # rayo incidente, bajando
    normal = np.array([0.0, 1.0])                                   # contra el rayo
    cos_i = -np.dot(d, normal)
    k = 1 - (1 / n) ** 2 * (1 - cos_i**2)
    dentro = (1 / n) * d + ((1 / n) * cos_i - math.sqrt(k)) * normal
    return espesor * dentro[0] / -dentro[1]


def comprobar(res: dict) -> None:
    assert math.isclose(punto_salida(n1) - punto_salida(n2), res["separacion"], rel_tol=1e-12)
    # El de mayor índice se desvía más hacia la normal y avanza menos.
    assert punto_salida(n2) < punto_salida(n1)
    # La frecuencia es la misma dentro y fuera: n·λ_vidrio = λ_vacío.
    assert math.isclose(n1 * res["longitud"], c / f, rel_tol=1e-12)
    # Distancia perpendicular entre los rayos emergentes, que salen paralelos a 40°.
    assert math.isclose(res["separacion"] * math.cos(incidencia), 0.282, rel_tol=5e-3)
    # Solución orientativa oficial: 0,37 cm y 441 nm (esta última, con la velocidad redondeada).
    assert math.isclose(res["separacion"], 0.37, abs_tol=0.005)
    assert math.isclose(avance(n1), 8.71, abs_tol=0.005) and math.isclose(avance(n2), 8.34, abs_tol=0.005)
    assert math.isclose(res["longitud"], 4.41e-7, rel_tol=5e-3)
