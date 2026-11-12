"""Verificación de fis2b-evau-madrid-2022-ext-b2 (cuatro altavoces)."""

import math

I0 = 1e-12
nivel, n, d = 100.0, 4, 10.0
S, t = 2e-4, 5 * 3600


def resolver() -> dict:
    I = I0 * 10 ** (nivel / 10)
    return {"P": I * 4 * math.pi * d**2 / n, "E": I * S * t}


def comprobar(res: dict) -> None:
    # Segunda vía: colocar los cuatro altavoces alrededor y sumar intensidades en el centro.
    total = sum(res["P"] / (4 * math.pi * (d * math.cos(a)) ** 2 + 4 * math.pi * (d * math.sin(a)) ** 2)
                for a in (0, math.pi / 2, math.pi, 3 * math.pi / 2))
    assert math.isclose(10 * math.log10(total / I0), nivel, abs_tol=1e-9)
    # Cada altavoz por separado da 100 − 10·log 4 ≈ 94 dB.
    uno = 10 * math.log10(res["P"] / (4 * math.pi * d**2) / I0)
    assert math.isclose(uno, nivel - 10 * math.log10(n), abs_tol=1e-9)
    # La energía es potencia captada por el oído por el tiempo.
    assert math.isclose(res["E"], total * S * t, rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["P"], math.pi, rel_tol=1e-12) and math.isclose(res["E"], 36e-3, rel_tol=1e-9)
