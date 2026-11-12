"""Verificación de fis2b-evau-madrid-2022-ord-a2 (dos puntos en fase que cruzan el eje cada 4 s)."""

import math

separacion, entre_cruces = 2.0, 4.0
y0 = 0.10


def resolver() -> dict:
    return {"v": separacion / (2 * entre_cruces), "A": y0}


def comprobar(res: dict) -> None:
    T, longitud = 2 * entre_cruces, separacion
    w, k, A = 2 * math.pi / T, 2 * math.pi / longitud, res["A"]
    y = lambda x, t: A * math.cos(w * t + k * x)
    # A y B empiezan en +10 cm con velocidad nula, y oscilan en fase.
    dt = 1e-6
    for x in (0.0, 2.0):
        assert math.isclose(y(x, 0), y0, abs_tol=1e-12)
        assert abs((y(x, dt) - y(x, -dt)) / (2 * dt)) < 1e-9
    for t in (0.7, 3.3, 5.9):
        assert math.isclose(y(0, t), y(2, t), abs_tol=1e-12)
    # Entre A y B ningún otro punto está en fase con ellos.
    assert all(abs(y(x / 100, 1.3) - y(0, 1.3)) > 1e-6 or abs(y(x / 100, 0) - y(0, 0)) > 1e-6 for x in range(1, 200))
    # Cruces por cero del elemento A: buscar cambios de signo en 16 s.
    cruces, n = [], 160000
    for i in range(n):
        t1, t2 = 16 * i / n, 16 * (i + 1) / n
        if y(0, t1) * y(0, t2) < 0:
            cruces.append(0.5 * (t1 + t2))
    assert len(cruces) == 4 and all(math.isclose(b - a, entre_cruces, abs_tol=1e-3) for a, b in zip(cruces, cruces[1:]))
    # Viaja hacia −x con la velocidad calculada.
    assert math.isclose(y(1.0, 0.5), y(1.0 - res["v"] * 0.4, 0.9), abs_tol=1e-12)
    # La versión con seno es la misma onda.
    assert math.isclose(A * math.sin(w * 1.7 + k * 0.4 + math.pi / 2), y(0.4, 1.7), abs_tol=1e-12)
    assert math.isclose(res["v"], 0.25)
