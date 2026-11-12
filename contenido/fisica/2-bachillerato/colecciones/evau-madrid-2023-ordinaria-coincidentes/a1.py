"""Verificación de fis2b-evau-madrid-2023-ordc-a1 (órbita alrededor de Fomalhaut II)."""

import math

G, M, R = 6.67e-11, 4e23, 5e6
T = 4.36 * 3600
dE = 1.5e10


def resolver() -> dict:
    r = (G * M * T**2 / (4 * math.pi**2)) ** (1 / 3)
    return {"h": r - R, "m": 2 * r * dE / (G * M)}


def comprobar(res: dict) -> None:
    r = R + res["h"]
    # Segunda vía: con ese radio, la velocidad orbital da el periodo del enunciado.
    v = math.sqrt(G * M / r)
    assert math.isclose(2 * math.pi * r / v, T, rel_tol=1e-12)
    # Con la masa obtenida, cinética + potencial + energía aportada = 0.
    m = res["m"]
    assert math.isclose(0.5 * m * v**2 - G * M * m / r + dE, 0, abs_tol=1e-3)
    # Con más masa no escaparía.
    assert 0.5 * (m + 1) * v**2 - G * M * (m + 1) / r + dE < 0
    # Valores de la solución orientativa oficial.
    assert math.isclose(r, 5.501e6, rel_tol=1e-4)
    assert math.isclose(res["h"], 5.01e5, rel_tol=2e-3)
    assert math.isclose(m, 6186, rel_tol=1e-4)
