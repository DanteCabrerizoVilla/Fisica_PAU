"""Verificación de fis2b-evau-madrid-2023-ext-b4 (lente con aumento −2 y +2)."""

import math

# Datos del enunciado (m, criterio DIN)
s1, M1 = -0.30, -2.0
M2 = 2.0


def resolver() -> dict:
    P = 1 / (M1 * s1) - 1 / s1
    f = 1 / P
    s2 = f * (1 - M2) / M2
    return {"P": P, "s": s2 * 100}


def comprobar(res: dict) -> None:
    f = 1 / res["P"]
    s2 = res["s"] / 100
    s2_im = 1 / (1 / f + 1 / s2)
    assert math.isclose(s2_im / s2, M2, rel_tol=1e-12) and s2_im < 0, "imagen virtual con aumento +2"
    assert abs(s2) < f, "el objeto debe estar entre el foco y la lente"
    # Trazado: prolongación del rayo paralelo (por (0, y) y F') y rayo central se cortan en la imagen.
    y = 1.0
    x = 1 / (1 / s2 + 1 / f)
    assert math.isclose(y * (1 - x / f), y * x / s2, rel_tol=1e-12) and math.isclose(y * x / s2, M2 * y, rel_tol=1e-12)
    assert math.isclose(res["P"], 5.0, rel_tol=1e-12) and math.isclose(res["s"], -10.0, rel_tol=1e-12)
