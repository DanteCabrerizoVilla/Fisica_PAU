"""Verificación de fis2b-pau-madrid-2026-ext-2b (sistema de dos lentes)."""

import math

# Datos del enunciado (cm, criterio DIN)
f1 = 15.0
f2 = -20.0
separacion = 60.0
s1 = -30.0
y = 10.0


def imagen(s: float, f: float) -> float:
    return 1 / (1 / f + 1 / s)


def resolver() -> dict:
    s1_im = imagen(s1, f1)
    s2 = s1_im - separacion
    s2_im = imagen(s2, f2)
    aumento = (s1_im / s1) * (s2_im / s2)
    return {"s2": s2_im, "y": aumento * y}


def comprobar(res: dict) -> None:
    # Segunda vía: seguir dos rayos con trigonometría paraxial (altura y pendiente).
    def atravesar(altura, pendiente, f):          # lente delgada
        return altura, pendiente - altura / f

    def avanzar(altura, pendiente, d):
        return altura + pendiente * d, pendiente

    finales = []
    for pendiente in (0.0, -y / abs(s1)):          # rayo paralelo y rayo por el centro de la lente 1
        h, p = avanzar(y, pendiente, abs(s1))
        h, p = atravesar(h, p, f1)
        h, p = avanzar(h, p, separacion)
        h, p = atravesar(h, p, f2)
        finales.append((h, p))
    (h1, p1), (h2, p2) = finales
    # Punto donde se cortan las rectas que salen de la lente 2 (x medido desde ella).
    x = (h2 - h1) / (p1 - p2)
    altura = h1 + p1 * x
    assert math.isclose(x, res["s2"], rel_tol=1e-9), f"los rayos se cortan en x = {x}"
    assert math.isclose(altura, res["y"], rel_tol=1e-9), f"altura de la imagen {altura}"
    assert res["s2"] < 0 and res["y"] < 0 and abs(res["y"]) < y      # virtual, invertida, menor
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["s2"], -12, rel_tol=1e-9) and math.isclose(res["y"], -4, rel_tol=1e-9)
