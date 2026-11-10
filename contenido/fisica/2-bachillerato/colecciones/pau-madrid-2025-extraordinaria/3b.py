"""Verificación de fis2b-pau-madrid-2025-ext-3b (lente convergente: tamaños y distancia total)."""

import math

# Datos del enunciado (cm, criterio DIN)
y = 4.0
y_imagen = -2.0          # imagen real: invertida
distancia = 45.0
y_imagen_b = -4.0


def resolver() -> dict:
    M = y_imagen / y
    s_im = distancia / (1 - 1 / M)       # s' − s = d con s = s'/M
    s = s_im / M
    f = 1 / (1 / s_im - 1 / s)
    M_b = y_imagen_b / y
    s_nueva = f * (1 - M_b) / M_b        # de 1/(M s) − 1/s = 1/f
    return {"s": s, "s_im": s_im, "f": f, "s_nueva": s_nueva}


def comprobar(res: dict) -> None:
    s, s_im, f = res["s"], res["s_im"], res["f"]
    assert s < 0 < s_im and f > 0
    assert math.isclose(s_im - s, distancia, rel_tol=1e-12)
    assert math.isclose(s_im / s * y, y_imagen, rel_tol=1e-12)
    # Apartado b: con el objeto en s_nueva la imagen mide −4 cm y es real.
    s2 = res["s_nueva"]
    s2_im = 1 / (1 / f + 1 / s2)
    assert s2_im > 0 and math.isclose(s2_im / s2 * y, y_imagen_b, rel_tol=1e-12)
    assert math.isclose(s2, -2 * f, rel_tol=1e-12), "el objeto debe quedar a 2f"
    # Trazado: el rayo paralelo (pasa por F') y el del centro se cortan en la imagen.
    y_paralelo = y - (y / f) * s2_im
    y_centro = (y / s2) * s2_im
    assert math.isclose(y_paralelo, y_centro, rel_tol=1e-12) and math.isclose(y_centro, y_imagen_b, rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert (round(s), round(s_im), round(f), round(s2)) == (-30, 15, 10, -20)
