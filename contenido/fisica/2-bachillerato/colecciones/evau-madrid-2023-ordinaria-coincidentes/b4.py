"""Verificación de fis2b-evau-madrid-2023-ordc-b4 (rayo horizontal en un prisma 30-60-90)."""

import math

import numpy as np

n = 1.33


def resolver() -> dict:
    t = math.asin(math.sin(math.radians(30)) / n)
    inc2 = math.radians(30) - t
    return {"refraccion": math.degrees(t), "salida": math.degrees(math.asin(n * math.sin(inc2)))}


def refractar(d, normal, n1, n2):
    """Ley de Snell vectorial; `normal` unitaria, apuntando contra el rayo."""
    cos_i = -np.dot(d, normal)
    k = 1 - (n1 / n2) ** 2 * (1 - cos_i**2)
    assert k >= 0, "reflexión total inesperada"
    return (n1 / n2) * d + ((n1 / n2) * cos_i - math.sqrt(k)) * normal


def comprobar(res: dict) -> None:
    # Segunda vía: trazado vectorial. Ejes: x a la derecha, y hacia arriba.
    # Cara inclinada: sube hacia la derecha formando 60° con la base. Normal exterior, arriba-izquierda.
    n_inclinada = np.array([-math.sin(math.radians(60)), math.cos(math.radians(60))])
    cara = np.array([math.cos(math.radians(60)), math.sin(math.radians(60))])
    assert abs(np.dot(n_inclinada, cara)) < 1e-12
    rayo = np.array([1.0, 0.0])
    assert math.isclose(math.degrees(math.acos(-np.dot(rayo, n_inclinada))), 30, abs_tol=1e-9)
    dentro = refractar(rayo, n_inclinada, 1, n)
    assert math.isclose(math.degrees(math.acos(np.dot(dentro, -n_inclinada))), res["refraccion"], abs_tol=1e-9)
    # Dentro del vidrio el rayo baja 7,92° respecto a la horizontal.
    assert dentro[1] < 0 and math.isclose(math.degrees(math.atan2(-dentro[1], dentro[0])), 30 - res["refraccion"], abs_tol=1e-9)
    # Cara posterior vertical: normal exterior (1, 0).
    fuera = refractar(dentro, np.array([-1.0, 0.0]), n, 1)
    assert math.isclose(math.degrees(math.atan2(-fuera[1], fuera[0])), res["salida"], abs_tol=1e-9)
    # Lejos del ángulo límite.
    assert 30 - res["refraccion"] < math.degrees(math.asin(1 / n))
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["refraccion"], 22.08, abs_tol=0.01) and math.isclose(res["salida"], 10.56, abs_tol=0.01)
