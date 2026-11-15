"""Verificación de fis2b-evau-madrid-2018-ext-b4 (prisma de índice 2)."""

import math

n = 2.0
sen, asen = lambda g: math.sin(math.radians(g)), lambda x: math.degrees(math.asin(x))


def resolver() -> dict:
    L = asen(1 / n)
    alfa = L
    return {"L": L, "alfa": alfa, "i": asen(n * sen(alfa / 2))}


def comprobar(res: dict) -> None:
    alfa, i = res["alfa"], res["i"]
    r = asen(sen(i) / n)
    e = asen(n * sen(alfa - r))
    assert math.isclose(e, i, rel_tol=1e-9)
    # Desviación mínima: δ(i) = i + e − α tiene su mínimo en ese ángulo.
    dev = lambda inc: inc + asen(n * sen(alfa - asen(sen(inc) / n))) - alfa
    assert dev(i) < dev(i - 1) and dev(i) < dev(i + 1)
