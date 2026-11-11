"""Verificación de fis2b-evau-madrid-2023-ext-a4 (foco en el fondo de un estanque)."""

import math

# Datos del enunciado (SI)
H, H_ojo, d = 2.0, 1.6, 1.2
l_agua, l_aire = 375e-9, 500e-9


def resolver() -> dict:
    n = l_aire / l_agua
    sen_b = d / math.hypot(d, H_ojo)
    alfa = math.asin(sen_b / n)
    return {"n": n, "D": d + H * math.tan(alfa)}


def comprobar(res: dict) -> None:
    n, D = res["n"], res["D"]
    # Principio de Fermat: entre el foco (D, −H) y el ojo (0, H'), el punto de paso por la
    # superficie que hace mínimo el tiempo debe ser x = d.
    def camino_optico(x: float) -> float:
        return n * math.hypot(D - x, H) + math.hypot(x, H_ojo)

    mejor = min(range(0, 220001), key=lambda i: camino_optico(i * 1e-5)) * 1e-5
    assert math.isclose(mejor, d, abs_tol=2e-5), f"Fermat da x = {mejor}"
    # Sin refracción saldría 2,7 m (error típico citado).
    assert math.isclose(d + H * d / H_ojo, 2.7, rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(n, 1.33, rel_tol=3e-3) and math.isclose(D, 2.21, rel_tol=2e-3)
