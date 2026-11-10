"""Verificación de fis2b-evau-madrid-2024-ext-a4 (capa de aire entre dos cristales)."""

import math

# Datos del enunciado
c = 3e8
n1, n2, n_aire = 1.40, 1.50, 1.0
grosor = 10.0        # cm
d = 9.2              # cm
incidencia = math.radians(30)


def resolver() -> dict:
    t_aire = math.asin(n1 * math.sin(incidencia) / n_aire)
    t_2 = math.asin(n_aire * math.sin(t_aire) / n2)
    e = (d - grosor * math.tan(t_2)) / math.tan(t_aire)
    tiempo = (e / math.cos(t_aire) * n_aire + grosor / math.cos(t_2) * n2) * 1e-2 / c
    return {"e": e, "t": tiempo}


def comprobar(res: dict) -> None:
    e = res["e"]
    # Principio de Fermat: entre A y B (fijos), el punto de paso aire-cristal 2 del rayo real
    # hace mínimo el tiempo.
    def tiempo_por(x: float) -> float:          # x: avance horizontal en el aire (cm)
        return (math.hypot(x, e) * n_aire + math.hypot(d - x, grosor) * n2) * 1e-2 / c

    mejor = min((tiempo_por(i * d / 200000), i * d / 200000) for i in range(200001))
    assert math.isclose(mejor[0], res["t"], rel_tol=1e-9), "el tiempo no es el mínimo de Fermat"
    x_real = e * math.tan(math.asin(n1 * math.sin(incidencia)))
    assert math.isclose(mejor[1], x_real, abs_tol=1e-3), "el punto de paso no coincide"
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["e"], 4.0, rel_tol=2e-3) and math.isclose(res["t"], 7.52e-10, rel_tol=2e-3)
