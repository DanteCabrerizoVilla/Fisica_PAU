"""Verificación de fis2b-evau-madrid-2022-ord-a4 (dos lentes idénticas con aumento −1)."""

import math

separacion = 16.0      # cm


def resolver() -> dict:
    f = separacion / 4
    # La imagen de la primera queda a 2f; la segunda debe tenerla a f: se acerca f.
    return {"f": f, "P": 1 / (f / 100), "desplazamiento": (2 * f + f) - separacion}


def imagen(f, s):
    """Posición de la imagen (None si se va al infinito) y aumento."""
    inv = 1 / f + 1 / s
    if abs(inv) < 1e-12:
        return None, None
    sp = 1 / inv
    return sp, sp / s


def comprobar(res: dict) -> None:
    f = res["f"]
    # Segunda vía: buscar la posición del objeto que da M1 = −1 y comprobar que entonces M2 = −1.
    s1 = -2 * f
    s1p, M1 = imagen(f, s1)
    assert math.isclose(M1, -1)
    s2 = s1p - separacion
    s2p, M2 = imagen(f, s2)
    assert math.isclose(M2, -1) and math.isclose(s2p, 2 * f)
    # Con cualquier otra focal no se cumplen las dos condiciones a la vez.
    for otra in (3.0, 5.0, 6.0):
        a, _ = imagen(otra, -2 * otra)
        _, M = imagen(otra, a - separacion)
        assert M is None or not math.isclose(M, -1, rel_tol=1e-6)
    # Tras desplazar la segunda lente, la imagen final se va al infinito.
    nueva = separacion + res["desplazamiento"]
    assert math.isclose(nueva, 12)
    assert imagen(f, s1p - nueva)[0] is None
    # Valores de la solución orientativa oficial.
    assert math.isclose(f, 4) and math.isclose(res["P"], 25) and math.isclose(res["desplazamiento"], -4)
