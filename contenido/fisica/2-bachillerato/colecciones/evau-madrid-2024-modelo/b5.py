"""Verificación de fis2b-evau-madrid-2024-mod-b5 (cobre: frenado frente a longitud de onda)."""

import math

# Datos del enunciado y lecturas de la gráfica (SI)
c = 3e8
e = 1.6e-19
m_e = 9.1e-31
l1, V1 = 100e-9, 7.75
l2, V2 = 200e-9, 1.5
beta = 0.8


def resolver() -> dict:
    h = e * (V1 - V2) / (c * (1 / l1 - 1 / l2))
    W = h * c / l2 - e * V2
    Ec2 = (1 / math.sqrt(1 - beta**2) - 1) * m_e * c**2
    return {"h": h, "W": W / e, "dE": Ec2 - e * V1}


def comprobar(res: dict) -> None:
    h, W = res["h"], res["W"] * e
    # El trabajo de extracción sale igual con el otro punto.
    assert math.isclose(h * c / l1 - e * V1, W, rel_tol=1e-9)
    # La curva V = hc/(e·lambda) − W0 pasa por un punto intermedio razonable de la gráfica (150 nm, unos 3,6 V).
    assert math.isclose((h * c / 150e-9 - W) / e, 3.58, abs_tol=0.05)
    # Energía relativista por E² = (pc)² + (mc²)².
    gamma = 1 / math.sqrt(1 - beta**2)
    p = gamma * m_e * beta * c
    total = math.sqrt((p * c) ** 2 + (m_e * c**2) ** 2)
    assert math.isclose(total - m_e * c**2 - e * V1, res["dE"], rel_tol=1e-9)
    # La cinética clásica a 0,8c sería 2,6e-14 J (error típico citado).
    assert math.isclose(0.5 * m_e * (beta * c) ** 2, 2.6e-14, rel_tol=1e-2)
    # Valores de la solución orientativa oficial.
    assert math.isclose(h, 6.67e-34, rel_tol=1e-3) and math.isclose(res["W"], 4.75, rel_tol=1e-3)
    assert math.isclose(res["dE"], 5.5e-14, rel_tol=1e-2)
