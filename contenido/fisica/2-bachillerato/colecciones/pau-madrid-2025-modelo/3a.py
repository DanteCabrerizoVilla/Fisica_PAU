"""Verificación de fis2b-pau-madrid-2025-mod-3a (dos fuentes sonoras)."""

import math

import numpy as np

# Datos del enunciado (SI)
separacion = 8.0
suma = 50.0
r1 = 2.0
I_A = 7.3e-1
I_0 = 1e-12


def intensidad(P1, P2, d1):
    d2 = separacion - d1
    return P1 / (4 * math.pi * d1**2) + P2 / (4 * math.pi * d2**2)


def resolver() -> dict:
    r2 = separacion - r1
    # Sistema lineal: P1 + P2 = suma ; P1/(4π r1²) + P2/(4π r2²) = I_A
    matriz = np.array([[1.0, 1.0], [1 / (4 * math.pi * r1**2), 1 / (4 * math.pi * r2**2)]])
    P1, P2 = np.linalg.solve(matriz, np.array([suma, I_A]))
    I_medio = intensidad(P1, P2, separacion / 2)
    return {"P1": float(P1), "P2": float(P2), "nivel": 10 * math.log10(I_medio / I_0)}


def comprobar(res: dict) -> None:
    # Con las potencias halladas se recupera la intensidad medida en A.
    assert math.isclose(intensidad(res["P1"], res["P2"], r1), I_A, rel_tol=1e-12)
    # El nivel en el punto medio solo depende de la suma de potencias.
    assert math.isclose(res["nivel"], 10 * math.log10(suma / (4 * math.pi * 16) / I_0), rel_tol=1e-12)
    # Por sustitución, como en la solución escrita: 8 P1 = 144π·I_A − 50.
    assert math.isclose(res["P1"], (144 * math.pi * I_A - suma) / 8, rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    for clave, oficial in (("P1", 35.03), ("P2", 14.97), ("nivel", 113.96)):
        assert math.isclose(res[clave], oficial, rel_tol=1e-3), f"{clave} no coincide con la solución oficial"
