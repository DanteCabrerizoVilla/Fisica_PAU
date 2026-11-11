"""Verificación de fis2b-evau-madrid-2024-mod-b4 (paralelepípedo: tiempo y reflexión total)."""

import math

# Datos del enunciado
c = 3e8
n = 1.34
H = 4e-2


def angulo_en_cara_superior(theta_grados: float) -> float:
    """Ángulo de incidencia (grados) sobre la cara superior para una incidencia exterior dada."""
    t2 = math.asin(math.sin(math.radians(theta_grados)) / n)
    return 90 - math.degrees(t2)


def resolver() -> dict:
    t2 = math.asin(math.sin(math.radians(60)) / n)
    L = (H / 2) / math.sin(t2)
    # Límite: sen(theta) = n·cos(theta_L) = raíz(n² − 1)
    return {"t": L * n / c, "angulo": math.degrees(math.asin(math.sqrt(n**2 - 1)))}


def comprobar(res: dict) -> None:
    limite = math.degrees(math.asin(1 / n))
    # Justo por debajo del ángulo hallado hay reflexión total; justo por encima, no.
    assert angulo_en_cara_superior(res["angulo"] - 0.5) > limite
    assert angulo_en_cara_superior(res["angulo"] + 0.5) < limite
    assert angulo_en_cara_superior(60) > limite, "con 60° debe haber reflexión total"
    # Segunda vía para el tiempo: componentes de la velocidad. Sube H/2 con velocidad vertical (c/n)·sen(t2).
    t2 = math.asin(math.sin(math.radians(60)) / n)
    assert math.isclose((H / 2) / (c / n * math.sin(t2)), res["t"], rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["t"], 1.38e-10, rel_tol=3e-3) and math.isclose(res["angulo"], 63.12, abs_tol=0.02)
