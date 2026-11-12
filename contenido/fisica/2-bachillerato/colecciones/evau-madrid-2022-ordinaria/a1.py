"""Verificación de fis2b-evau-madrid-2022-ord-a1 (campo de una masa y punto más alejado)."""

import math

G = 6.67e-11
M, m = 20.0, 3.0
px, py = 8.0, 6.0
v0 = 1.2e-5


def resolver() -> dict:
    d = math.hypot(px, py)
    g = G * M / d**2
    E = 0.5 * m * v0**2 - G * M * m / d
    return {"g_x": -g * px / d, "g_y": -g * py / d, "F_x": -m * g * px / d, "F_y": -m * g * py / d,
            "r": -G * M * m / E}


def comprobar(res: dict) -> None:
    d = math.hypot(px, py)
    # Segunda vía: integrar el movimiento radial hasta que la velocidad se anula (Verlet).
    r, v, dt = d, v0, 50.0
    a = -G * M / r**2
    while v > 0:
        r_nuevo = r + v * dt + 0.5 * a * dt**2
        a_nuevo = -G * M / r_nuevo**2
        v += 0.5 * (a + a_nuevo) * dt
        r, a = r_nuevo, a_nuevo
    assert math.isclose(r, res["r"], rel_tol=1e-4)
    # No escapa.
    assert v0 < math.sqrt(2 * G * M / d)
    # El error típico (aceleración constante) da un recorrido mucho menor.
    assert math.isclose(v0**2 / (2 * G * M / d**2), 5.4, rel_tol=1e-2) and res["r"] - d > 11
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["g_x"], -1.07e-11, rel_tol=3e-3) and math.isclose(res["g_y"], -8.0e-12, rel_tol=1e-3)
    assert math.isclose(res["F_x"], -3.21e-11, rel_tol=4e-3) and math.isclose(res["F_y"], -2.40e-11, rel_tol=1e-3)
    assert math.isclose(res["r"], 21.73, rel_tol=1e-3)
    assert math.isclose(res["r"] * 0.8, 17.38, rel_tol=1e-3) and math.isclose(res["r"] * 0.6, 13.04, rel_tol=1e-3)
