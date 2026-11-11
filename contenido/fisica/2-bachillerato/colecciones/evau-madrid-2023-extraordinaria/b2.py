"""Verificación de fis2b-evau-madrid-2023-ext-b2 (dos focos sonoros)."""

import math

# Datos del enunciado (SI)
I_0 = 1e-12
F1, F2 = (-6.0, 0.0), (6.0, 0.0)
nivel = 80.0


def resolver() -> dict:
    cociente = (math.dist((2, 0), F1) / math.dist((2, 0), F2)) ** 2
    I = I_0 * 10 ** (nivel / 10)
    r2 = math.dist((0, 2), F1) ** 2
    P1 = 4 * math.pi * r2 * I / (1 + 1 / cociente)
    return {"cociente": cociente, "P1": P1, "I": P1 / (4 * math.pi * math.dist((0, 8), F1) ** 2)}


def comprobar(res: dict) -> None:
    P1 = res["P1"]
    P2 = P1 / res["cociente"]

    def intensidad(P, foco, punto):
        return P / (4 * math.pi * math.dist(punto, foco) ** 2)

    # Se cumplen las dos condiciones del enunciado.
    assert math.isclose(intensidad(P1, F1, (2, 0)), intensidad(P2, F2, (2, 0)), rel_tol=1e-12)
    total = intensidad(P1, F1, (0, 2)) + intensidad(P2, F2, (0, 2))
    assert math.isclose(10 * math.log10(total / I_0), nivel, rel_tol=1e-12)
    # Valores de la solución orientativa oficial: P1 = 128π·10⁻⁴ W, I1 = 3,2·10⁻⁵ W/m².
    assert math.isclose(P1, 128 * math.pi * 1e-4, rel_tol=1e-12) and math.isclose(res["I"], 3.2e-5, rel_tol=1e-12)
