"""Verificación de fis2b-evau-madrid-2024-ext-a2 (dos focos sonoros)."""

import math

# Datos del enunciado (SI)
I_0 = 1e-12
F1, F2 = (0.0, 3.0), (4.0, 0.0)
nivel_1, nivel_2 = 55.0, 65.0
r_ref = 2.0


def potencia(nivel: float) -> float:
    return 4 * math.pi * r_ref**2 * I_0 * 10 ** (nivel / 10)


def intensidad(p) -> float:
    return sum(P / (4 * math.pi * math.dist(p, F) ** 2) for P, F in ((potencia(nivel_1), F1), (potencia(nivel_2), F2)))


def resolver() -> dict:
    I = intensidad((0.0, 0.0))
    d = math.dist(F1, F2)
    x = d / (1 + math.sqrt(potencia(nivel_2) / potencia(nivel_1)))
    return {"I": I, "nivel": 10 * math.log10(I / I_0), "x": x}


def comprobar(res: dict) -> None:
    # En el punto hallado las dos intensidades coinciden.
    d = math.dist(F1, F2)
    x = res["x"]
    I1 = potencia(nivel_1) / (4 * math.pi * x**2)
    I2 = potencia(nivel_2) / (4 * math.pi * (d - x) ** 2)
    assert math.isclose(I1, I2, rel_tol=1e-12) and 0 < x < d
    # Es raíz de 9x² + 10x − 25 = 0 (ecuación de la solución oficial).
    assert abs(9 * x**2 + 10 * x - 25) < 1e-9
    # Solución oficial: intensidad 9,31e-7; su nivel (59,62) es una errata de 59,69.
    assert math.isclose(res["I"], 9.31e-7, rel_tol=2e-3)
    assert math.isclose(10 * math.log10(9.31e-7 / I_0), 59.69, abs_tol=0.01)
    assert math.isclose(res["x"], 1.2, rel_tol=2e-3)
