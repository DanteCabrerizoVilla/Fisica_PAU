"""Verificación de fis2b-pau-madrid-2026-ext-3b (espira en un campo variable)."""

import math

# Datos del enunciado (SI)
S = 10e-4
R = 2.0
# Gráfica B(t): vértices (s, T)
VERTICES = [(0.0, 0.0), (5e-3, 60e-3), (20e-3, 60e-3), (30e-3, 0.0)]


def campo(t: float) -> float:
    for (t1, b1), (t2, b2) in zip(VERTICES, VERTICES[1:]):
        if t1 <= t <= t2:
            return b1 + (b2 - b1) * (t - t1) / (t2 - t1)
    raise ValueError(t)


def fem(t: float, h: float = 1e-7) -> float:
    """Ley de Faraday con derivada numérica; normal en el sentido de B."""
    return -S * (campo(t + h) - campo(t - h)) / (2 * h)


def resolver() -> dict:
    e1, e2, e3 = fem(2.5e-3), fem(12e-3), fem(25e-3)
    return {
        "fem_1": abs(e1) * 1e3, "fem_2": e2, "fem_3": abs(e3) * 1e3,   # mV, V, mV
        "I_1": abs(e1) / R * 1e3, "I_3": abs(e3) / R * 1e3,           # mA
    }


def comprobar(res: dict) -> None:
    # Con la normal a favor de B, la fem es negativa mientras el campo crece
    # (corriente antihoraria) y positiva mientras decrece (horaria).
    assert fem(2.5e-3) < 0 < fem(25e-3), "los signos no corresponden a la ley de Lenz"
    assert math.isclose(res["fem_1"], 2 * res["fem_3"], rel_tol=1e-6)
    # Carga total que circula: |ΔΦ|/R en cada tramo, igual en la subida y en la bajada.
    carga_subida = res["I_1"] * 1e-3 * 5e-3
    carga_bajada = res["I_3"] * 1e-3 * 10e-3
    assert math.isclose(carga_subida, 60e-3 * S / R, rel_tol=1e-6)
    assert math.isclose(carga_subida, carga_bajada, rel_tol=1e-6)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["fem_1"], 12, rel_tol=1e-6) and math.isclose(res["fem_3"], 6, rel_tol=1e-6)
    assert math.isclose(res["I_1"], 6, rel_tol=1e-6) and math.isclose(res["I_3"], 3, rel_tol=1e-6)
