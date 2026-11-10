"""Verificación de fis2b-pau-madrid-2026-ord-3b (lámina de caras paralelas)."""

import math

# Datos del enunciado (SI)
c = 3e8
n_aire = 1.0
n = 1.7
e = 3e-2
incidencia = math.radians(48)


def resolver() -> dict:
    refraccion = math.asin(n_aire * math.sin(incidencia) / n)
    d = e / math.cos(refraccion)
    return {
        "angulo": math.degrees(refraccion),
        "tiempo": d / (c / n),
        "separacion": 2 * e * math.tan(refraccion) * 100,      # cm
    }


def comprobar(res: dict) -> None:
    # Segunda vía: seguir el rayo con vectores. Dirección dentro de la lámina (x, hacia abajo).
    sen_r = n_aire * math.sin(incidencia) / n
    direccion = (sen_r, math.sqrt(1 - sen_r**2))
    pasos = e / direccion[1]                       # longitud hasta la cara inferior
    x_abajo = direccion[0] * pasos
    assert math.isclose(pasos * n / c, res["tiempo"], rel_tol=1e-12)
    # La reflexión invierte la componente vertical: al volver a la cara superior ha avanzado el doble.
    assert math.isclose(2 * x_abajo * 100, res["separacion"], rel_tol=1e-12)
    # Principio de Fermat: el camino real hace mínimo el tiempo aire-lámina entre dos puntos fijos.
    origen = (-math.tan(incidencia) * 0.05, 0.05)   # punto del rayo incidente, 5 cm por encima
    destino = (x_abajo, -e)

    def tiempo_por(x: float) -> float:
        return (math.hypot(x - origen[0], origen[1]) * n_aire + math.hypot(destino[0] - x, e) * n) / c

    assert tiempo_por(0.0) < tiempo_por(1e-4) and tiempo_por(0.0) < tiempo_por(-1e-4), "no cumple Fermat"
    # El rayo (2) sale con el mismo ángulo de incidencia.
    assert math.isclose(math.degrees(math.asin(n * sen_r / n_aire)), 48, rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    for clave, oficial in (("angulo", 25.92), ("tiempo", 1.89e-10), ("separacion", 2.92)):
        assert math.isclose(res[clave], oficial, rel_tol=3e-3), f"{clave} no coincide con la solución oficial"
