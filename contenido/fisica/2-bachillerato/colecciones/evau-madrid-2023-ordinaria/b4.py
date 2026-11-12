"""Verificación de fis2b-evau-madrid-2023-ord-b4 (prisma equilátero)."""

import math

import numpy as np

# Datos del enunciado
n = 1.66
A = math.radians(60)
incidencia = math.radians(50)


def resolver() -> dict:
    alfa = math.asin(math.sin(incidencia) / n)
    gamma = A - alfa
    beta = math.asin(n * math.sin(gamma))
    limite = math.asin(1 / n)
    minima = math.asin(n * math.sin(A - limite))
    return {"alfa": math.degrees(alfa), "beta": math.degrees(beta), "incidencia": math.degrees(minima)}


def refractar(d, normal, n1, n2):
    """Ley de Snell vectorial. `normal` apunta contra el rayo. Devuelve None si hay reflexión total."""
    cos_i = -np.dot(d, normal)
    k = 1 - (n1 / n2) ** 2 * (1 - cos_i**2)
    if k < 0:
        return None
    return (n1 / n2) * d + ((n1 / n2) * cos_i - math.sqrt(k)) * normal


def trazar(grados):
    """Sigue el rayo por el prisma con vectores. Devuelve (alfa, beta) en grados; beta es None si no sale."""
    # Vértice superior en el origen del ángulo; caras izquierda y derecha a ±30° de la vertical.
    n_izq = np.array([-math.cos(math.radians(30)), math.sin(math.radians(30))])   # normal exterior izquierda
    n_der = np.array([math.cos(math.radians(30)), math.sin(math.radians(30))])    # normal exterior derecha
    # Rayo incidente: forma `grados` con la normal de la cara izquierda, viniendo desde abajo.
    t = math.radians(grados)
    hacia_dentro = -n_izq
    tangente = np.array([-n_izq[1], n_izq[0]])        # a lo largo de la cara, hacia arriba
    if tangente[1] < 0:
        tangente = -tangente
    d = math.cos(t) * hacia_dentro + math.sin(t) * tangente
    dentro = refractar(d, n_izq, 1, n)
    alfa = math.degrees(math.acos(np.dot(dentro, hacia_dentro)))
    fuera = refractar(dentro, -n_der, n, 1)
    if fuera is None:
        return alfa, None
    return alfa, math.degrees(math.acos(np.dot(fuera, n_der)))


def comprobar(res: dict) -> None:
    alfa, beta = trazar(50)
    assert math.isclose(alfa, res["alfa"], abs_tol=1e-9)
    assert math.isclose(beta, res["beta"], abs_tol=1e-9)
    # Justo por encima de la incidencia mínima el rayo sale casi rasante; por debajo, no sale.
    _, sale = trazar(res["incidencia"] + 0.01)
    assert sale is not None and sale > 88
    assert trazar(res["incidencia"] - 0.01)[1] is None
    assert trazar(20)[1] is None and trazar(70)[1] is not None
    # Valores de la solución orientativa oficial (redondea los ángulos intermedios).
    assert math.isclose(res["alfa"], 27.48, abs_tol=0.02)
    assert math.isclose(res["beta"], 63.18, abs_tol=0.05)
    assert math.isclose(res["incidencia"], 40.39, abs_tol=0.05)
