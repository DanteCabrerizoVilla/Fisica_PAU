"""Verificación de fis2b-evau-madrid-2023-ordc-b2 (coro en semicircunferencia)."""

import math

I0 = 1e-12
n, nivel_1m, nivel_centro = 12, 90.0, 88.72


def resolver() -> dict:
    P = I0 * 10 ** (nivel_1m / 10) * 4 * math.pi * 1.0**2
    Ic = I0 * 10 ** (nivel_centro / 10)
    return {"P": P, "R": math.sqrt(n * P / (4 * math.pi * Ic))}


def comprobar(res: dict) -> None:
    P, R = res["P"], res["R"]
    # Segunda vía: colocar los 12 cantantes sobre la semicircunferencia y sumar intensidades en el centro.
    total = 0.0
    for i in range(n):
        ang = math.pi * i / (n - 1)
        x, y = R * math.cos(ang), R * math.sin(ang)
        total += P / (4 * math.pi * (x**2 + y**2))
    assert math.isclose(10 * math.log10(total / I0), nivel_centro, abs_tol=1e-9)
    # Tercera vía, en decibelios: 12 fuentes suben 10·log 12 y alejarse a R baja 20·log R.
    assert math.isclose(nivel_1m + 10 * math.log10(n) - 20 * math.log10(R), nivel_centro, abs_tol=1e-9)
    # Un solo cantante a 1 m da 90 dB.
    assert math.isclose(10 * math.log10(P / (4 * math.pi) / I0), nivel_1m, abs_tol=1e-9)
    # Valores de la solución orientativa oficial (que redondea el radio a 4 m).
    assert math.isclose(P, 1.26e-2, rel_tol=3e-3) and math.isclose(R, 4.0, rel_tol=5e-3)
