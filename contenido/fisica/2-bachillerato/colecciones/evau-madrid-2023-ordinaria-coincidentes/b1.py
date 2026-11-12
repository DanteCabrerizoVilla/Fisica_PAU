"""Verificación de fis2b-evau-madrid-2023-ordc-b1 (campo de una masa y alejamiento máximo)."""

import math

G = 6.67e-11
M, px, py = 5e4, 0.06, 0.08
m, v0 = 25e-6, 5e-3


def resolver() -> dict:
    d0 = math.hypot(px, py)
    g = G * M / d0**2
    E = 0.5 * m * v0**2 - G * M * m / d0
    return {"g_x": g * px / d0, "g_y": g * py / d0, "d": -G * M * m / E}


def comprobar(res: dict) -> None:
    d0 = math.hypot(px, py)
    # Segunda vía: integrar el movimiento radial hasta que la velocidad se anula (Verlet).
    r, v, dt = d0, v0, 1e-3
    a = -G * M / r**2
    while v > 0:
        r_nuevo = r + v * dt + 0.5 * a * dt**2
        a_nuevo = -G * M / r_nuevo**2
        v += 0.5 * (a + a_nuevo) * dt
        r, a = r_nuevo, a_nuevo
    assert math.isclose(r, res["d"], rel_tol=1e-4)
    # No escapa: la velocidad de lanzamiento es menor que la de escape desde d0.
    assert v0 < math.sqrt(2 * G * M / d0)
    # El campo apunta hacia la masa.
    assert res["g_x"] > 0 and res["g_y"] > 0
    assert math.isclose(res["g_y"] / res["g_x"], py / px, rel_tol=1e-12)
    # El error típico (aceleración constante) da un recorrido distinto del real.
    recorrido_mal = v0**2 / (2 * G * M / d0**2)
    assert math.isclose(recorrido_mal, 0.0375, rel_tol=1e-2) and res["d"] - d0 > recorrido_mal
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["g_x"], 2.00e-4, rel_tol=1e-3) and math.isclose(res["g_y"], 2.67e-4, rel_tol=1e-3)
    assert math.isclose(res["d"], 0.16, rel_tol=1e-3)
