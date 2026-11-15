"""Verificación de fis2b-evau-madrid-2018-ord-b2 (onda a partir de dos gráficas)."""

import math

lam, A, T = 2.0, 2.5, 9.0
k, w = 2 * math.pi / lam, 2 * math.pi / T
fase = math.pi


def y(x, t):
    return A * math.sin(w * t - k * x + fase)


def resolver() -> dict:
    return {"lam": lam, "A": A, "T": T, "v": lam / T}


def comprobar(res: dict) -> None:
    # Figura 2: y(1, t) = 2,5 sen(2πt/9), máximo en t = 2,25 s.
    for t in (0, 1.1, 2.25, 6.75, 13):
        assert math.isclose(y(1, t), A * math.sin(w * t), abs_tol=1e-12)
    # Figura 1 en t = 0: cero en x = 0, máximo en 0,5 m, mínimo en 1,5 m.
    assert abs(y(0, 0)) < 1e-12 and math.isclose(y(0.5, 0), A) and math.isclose(y(1.5, 0), -A)
