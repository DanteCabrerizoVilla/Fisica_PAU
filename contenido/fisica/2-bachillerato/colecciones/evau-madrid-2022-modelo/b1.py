"""Verificación de fis2b-evau-madrid-2022-mod-b1 (experimento de Cavendish)."""

import math

MT, RT = 5.97e24, 6.37e6
M = 10.0


def resolver() -> dict:
    return {"cociente": math.sqrt(10 - 1), "d": RT * math.sqrt(1e9 * M / MT)}


def comprobar(res: dict) -> None:
    d = res["d"]
    D = res["cociente"] * d
    # Con valores cualesquiera de G y m, se cumplen las dos condiciones.
    for G, m in ((6.67e-11, 0.05), (1.0, 3.0)):
        FB = G * M * m / d**2
        FC = G * M * m / (D**2 + d**2)
        peso = G * MT * m / RT**2
        assert math.isclose(FC, FB / 10, rel_tol=1e-12)
        assert math.isclose(FB, 1e-9 * peso, rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["cociente"], 3) and math.isclose(d, 0.26, rel_tol=5e-3)
