"""Verificación de fis2b-evau-madrid-2020-ext-a4 (prisma de 30°)."""

import math

c, n_vidrio, n_diamante, apice, prof = 3e8, 1.5, 2.5, math.radians(30), 0.05


def resolver() -> dict:
    d = prof * math.tan(apice)
    return {"t": d * n_vidrio / c, "angulo": math.degrees(math.asin(n_vidrio * math.sin(apice)))}


def comprobar(res: dict) -> None:
    assert n_diamante * math.sin(apice) > 1, "con diamante hay reflexión total"
    assert math.isclose(1 / math.sin(apice), 2.0), "índice máximo para que salga"
    assert math.isclose(res["t"], 1.44e-10, rel_tol=3e-3) and math.isclose(res["angulo"], 48.6, abs_tol=0.01)
