"""Verificación de fis2b-evau-madrid-2023-ordc-b5 (radón-222: actividad y masa límite)."""

import math

NA, M = 6.02e23, 222.0
T = 3.82 * 86400
masa_a = 1e-3                    # g
limite, volumen = 300.0, 20.0    # Bq/m³, m³


def resolver() -> dict:
    lam = math.log(2) / T
    A0 = lam * masa_a / M * NA
    return {"constante": lam, "actividad": A0, "masa": limite * volumen / lam / NA * M}


def comprobar(res: dict) -> None:
    lam = res["constante"]
    # Segunda vía: la actividad es proporcional a la masa.
    assert math.isclose(res["masa"], masa_a * limite * volumen / res["actividad"], rel_tol=1e-12)
    # Tercera vía para la actividad: contar las desintegraciones en un intervalo corto.
    N0 = masa_a / M * NA
    dt = 1.0
    assert math.isclose(N0 * (1 - math.exp(-lam * dt)) / dt, res["actividad"], rel_tol=1e-5)
    # Tras un periodo queda la mitad.
    assert math.isclose(math.exp(-lam * T), 0.5, rel_tol=1e-12)
    # Con la masa límite, la actividad por metro cúbico es justo la legal.
    assert math.isclose(lam * res["masa"] / M * NA / volumen, limite, rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(lam, 2.1e-6, rel_tol=1e-3)
    assert math.isclose(res["actividad"], 5.69e12, rel_tol=2e-3)
    assert math.isclose(res["masa"], 1.05e-12, rel_tol=5e-3)
