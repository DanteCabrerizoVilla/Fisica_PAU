"""Verificación de fis2b-evau-madrid-2022-ord-b2 (foco sonoro a una altura h)."""

import math

I0 = 1e-12
rA, nivel_A, nivel_B = 100.0, 60.0, 80.0


def resolver() -> dict:
    P = I0 * 10 ** (nivel_A / 10) * 4 * math.pi * rA**2
    h = math.sqrt(P / (4 * math.pi * I0 * 10 ** (nivel_B / 10)))
    I = P / (4 * math.pi * h**2) + P / (4 * math.pi * (h / 2) ** 2)
    return {"P": P, "h": h, "nivel": 10 * math.log10(I / I0)}


def comprobar(res: dict) -> None:
    P, h = res["P"], res["h"]
    nivel = lambda r: 10 * math.log10(P / (4 * math.pi * r**2) / I0)
    # Con P y h se recuperan los dos niveles del enunciado.
    assert math.isclose(nivel(rA), nivel_A, abs_tol=1e-9) and math.isclose(nivel(h), nivel_B, abs_tol=1e-9)
    # Segunda vía en decibelios: 20 dB de diferencia son un factor 10 en distancia.
    assert math.isclose(h, rA / 10 ** ((nivel_B - nivel_A) / 20), rel_tol=1e-12)
    # El foco a h/2 da 6,02 dB más que el primero; la suma, 10·log 5 más.
    assert math.isclose(nivel(h / 2) - nivel(h), 20 * math.log10(2), abs_tol=1e-9)
    assert math.isclose(res["nivel"], nivel_B + 10 * math.log10(5), abs_tol=1e-9)
    # A está en el suelo: su distancia horizontal a B es menor que 100 m.
    assert math.isclose(math.sqrt(rA**2 - h**2), 99.5, rel_tol=1e-3)
    # Valores de la solución orientativa oficial.
    assert math.isclose(P, 0.1257, rel_tol=1e-3) and math.isclose(h, 10) and math.isclose(res["nivel"], 87, abs_tol=0.02)
