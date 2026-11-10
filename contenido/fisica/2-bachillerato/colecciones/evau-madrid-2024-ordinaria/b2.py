"""Verificación de fis2b-evau-madrid-2024-ord-b2 (campanas y límite acústico)."""

import math

# Datos del enunciado (SI)
P = 10e-3
H = 35.0
D = 100.0
I_0 = 1e-12
limite = 55.0


def nivel(potencia: float, distancia: float) -> float:
    return 10 * math.log10(potencia / (4 * math.pi * distancia**2) / I_0)


def resolver() -> dict:
    return {"nivel_1": nivel(P, H), "nivel_4": nivel(4 * P, math.hypot(H, D))}


def comprobar(res: dict) -> None:
    assert res["nivel_4"] < limite, "no debe superarse el límite"
    # Segunda vía: +10·log(4) por las cuatro campanas y −20·log(d/H) por la distancia.
    d = math.hypot(H, D)
    assert math.isclose(res["nivel_4"], res["nivel_1"] + 10 * math.log10(4) - 20 * math.log10(d / H), rel_tol=1e-12)
    assert math.isclose(10 * math.log10(4), 6.0, abs_tol=0.03) and math.isclose(20 * math.log10(d / H), 9.6, abs_tol=0.03)
    # A menos distancia (por ejemplo 90 m) sí se superaría.
    assert nivel(4 * P, math.hypot(H, 90)) > limite
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["nivel_1"], 58.1, abs_tol=0.05) and math.isclose(res["nivel_4"], 54.5, abs_tol=0.05)
