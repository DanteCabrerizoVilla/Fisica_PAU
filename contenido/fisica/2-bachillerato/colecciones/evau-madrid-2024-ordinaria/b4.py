"""Verificación de fis2b-evau-madrid-2024-ord-b4 (prisma: reflexión total y refracción)."""

import math

import numpy as np

# Datos del enunciado
limite = math.radians(45.58)


def resolver() -> dict:
    n = 1 / math.sin(limite)
    return {"n": n, "angulo": math.degrees(math.asin(n * math.sin(math.radians(30))))}


def comprobar(res: dict) -> None:
    n = res["n"]
    # Segunda vía: seguir el rayo con vectores. Ejes: x a la derecha, y hacia arriba.
    # Prisma: cara vertical x = 0, base y = 0, cara inclinada a 30° de la vertical.
    a = math.radians(30)
    u_inclinada = np.array([math.sin(a), -math.cos(a)])      # dirección de la cara inclinada (hacia abajo)
    normal_entrada = np.array([-math.cos(a), -math.sin(a)])  # perpendicular a ella, hacia dentro
    assert abs(np.dot(u_inclinada, normal_entrada)) < 1e-12
    rayo = normal_entrada                                    # entra sin desviarse
    # Base: normal (0, 1). Ángulo de incidencia.
    inc_base = math.degrees(math.acos(abs(np.dot(rayo, [0, 1]))))
    assert math.isclose(inc_base, 60, abs_tol=1e-9) and inc_base > math.degrees(limite)
    rayo = rayo - 2 * np.dot(rayo, [0, 1]) * np.array([0.0, 1.0])     # reflexión total
    # Cara vertical: normal (1, 0).
    inc_vertical = math.degrees(math.acos(abs(np.dot(rayo, [1, 0]))))
    assert math.isclose(inc_vertical, 30, abs_tol=1e-9) and inc_vertical < math.degrees(limite)
    assert rayo[0] < 0 and rayo[1] > 0, "tras reflejarse va hacia la cara vertical, subiendo"
    salida = math.degrees(math.asin(n * math.sin(math.radians(inc_vertical))))
    assert math.isclose(salida, res["angulo"], rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(n, 1.40, rel_tol=1e-3) and math.isclose(res["angulo"], 44.43, abs_tol=0.02)
