"""Verificación de fis2b-evau-madrid-2022-mod-a2 (onda a partir de aceleración y desplazamiento)."""

import math

v = 4 / 3
y11, a11 = 0.02, -32 * math.pi**2 * 0.01      # SI
y00 = -0.02


def resolver() -> dict:
    w = math.sqrt(-a11 / y11)
    return {"w": w, "k": w / v, "A": abs(y00), "fase": math.acos(y00 / abs(y00))}


def comprobar(res: dict) -> None:
    w, k, A, fase = res["w"], res["k"], res["A"], res["fase"]
    y = lambda x, t: A * math.cos(w * t - k * x + fase)
    # Los tres datos del enunciado.
    assert math.isclose(y(0, 0), y00, abs_tol=1e-12)
    assert math.isclose(y(1, 1), y11, abs_tol=1e-12)
    dt = 1e-4
    a_num = (y(1, 1 + dt) - 2 * y(1, 1) + y(1, 1 - dt)) / dt**2
    assert math.isclose(a_num, a11, rel_tol=1e-5)
    # En (0, 0) la velocidad es nula: es un extremo.
    assert abs((y(0, 1e-7) - y(0, -1e-7)) / 2e-7) < 1e-6
    # Se propaga hacia +x con v = 4/3 m/s.
    assert math.isclose(y(0.2, 0.3), y(0.2 + v * 0.1, 0.4), abs_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(w, 4 * math.pi) and math.isclose(k, 3 * math.pi) and math.isclose(fase, math.pi)
