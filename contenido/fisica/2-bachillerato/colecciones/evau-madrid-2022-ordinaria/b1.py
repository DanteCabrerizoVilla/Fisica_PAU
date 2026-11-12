"""Verificación de fis2b-evau-madrid-2022-ord-b1 (escape de Marte y lanzamiento en la Tierra)."""

import math

RT = 6.37e6


def resolver() -> dict:
    cociente = math.sqrt((1 / 10) * 2)
    r = RT / (1 - cociente**2)          # de (1/5 − 1)/RT = −1/r
    return {"cociente": cociente, "h": r - RT}


def comprobar(res: dict) -> None:
    # Segunda vía: con valores numéricos de G y de la masa (cualesquiera), el resultado no cambia.
    for G, MT in ((6.67e-11, 5.97e24), (1.0, 3.3e20)):
        MM, RM = MT / 10, RT / 2
        veM, veT = math.sqrt(2 * G * MM / RM), math.sqrt(2 * G * MT / RT)
        assert math.isclose(veM / veT, res["cociente"], rel_tol=1e-12)
        E = 0.5 * veM**2 - G * MT / RT
        assert math.isclose(-G * MT / E - RT, res["h"], rel_tol=1e-9)
    # Tercera vía: integrar la subida con los valores reales.
    G, MT = 6.67e-11, 5.97e24
    r, v, dt = RT, math.sqrt(2 * G * (MT / 10) / (RT / 2)), 0.05
    a = -G * MT / r**2
    while v > 0:
        r_nuevo = r + v * dt + 0.5 * a * dt**2
        a_nuevo = -G * MT / r_nuevo**2
        v += 0.5 * (a + a_nuevo) * dt
        r, a = r_nuevo, a_nuevo
    assert math.isclose(r - RT, res["h"], rel_tol=1e-4)
    # El error típico con m·g·h da menos altura.
    g0 = G * MT / RT**2
    assert (2 * G * (MT / 10) / (RT / 2)) / (2 * g0) < res["h"]
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["cociente"], 1 / math.sqrt(5)) and math.isclose(res["h"], 1592.5e3, rel_tol=1e-9)
