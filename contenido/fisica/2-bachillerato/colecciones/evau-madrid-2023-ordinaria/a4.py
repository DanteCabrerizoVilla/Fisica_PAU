"""Verificación de fis2b-evau-madrid-2023-ord-a4 (lente, pantalla y segunda lente)."""

import math

# Datos del enunciado (cm, criterio DIN)
distancia_pantalla = 18.0
s = -14.2
y = 2.0
separacion = 5.0
f2 = 1.2


def resolver() -> dict:
    s_im = distancia_pantalla + s
    f = 1 / (1 / s_im - 1 / s)
    return {"f": f, "y_im": s_im / s * y}


def comprobar(res: dict) -> None:
    f1 = res["f"]
    s_im = distancia_pantalla + s
    # El objeto de la segunda lente cae en su foco objeto.
    s2 = s_im - separacion
    assert math.isclose(s2, -f2, rel_tol=1e-9)
    # Trazado matricial paraxial de dos rayos distintos: deben salir con la misma pendiente.
    def atravesar(h, p, focal):
        return h, p - h / focal

    def avanzar(h, p, d):
        return h + p * d, p

    pendientes = []
    for p0 in (0.0, -y / abs(s), 0.05):
        h, p = avanzar(y, p0, abs(s))
        h, p = atravesar(h, p, f1)
        h, p = avanzar(h, p, separacion)
        h, p = atravesar(h, p, f2)
        pendientes.append(p)
    assert max(pendientes) - min(pendientes) < 1e-9, f"los rayos no salen paralelos: {pendientes}"
    # Valores de la solución orientativa oficial.
    assert math.isclose(f1, 3.0, rel_tol=2e-3) and math.isclose(res["y_im"], -0.54, rel_tol=1e-2)
