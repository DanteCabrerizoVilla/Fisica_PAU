"""Verificación de fis2b-evau-madrid-2022-mod-b3 (espira que entra en un campo)."""

import math

a, v, B, R = 0.30, 0.03, 1e-3, 10.0


def resolver() -> dict:
    fem = B * a * v
    return {"fem": fem, "t_entrada": a / v, "I": fem / R}


def flujo(t):
    """Flujo a través de la espira: parte dentro del campo (x > 0) por el campo."""
    dentro = min(max(v * t, 0.0), a)
    return B * a * dentro


def comprobar(res: dict) -> None:
    dt = 1e-5
    fem = lambda t: -(flujo(t + dt) - flujo(t - dt)) / (2 * dt)
    # Mientras entra, la fem es constante e igual a −B·a·v; después, nula.
    for t in (1.0, 5.0, 9.9):
        assert math.isclose(fem(t), -res["fem"], rel_tol=1e-6)
    for t in (10.1, 12.0, 30.0):
        assert fem(t) == 0
    # El flujo final es B·a² y se alcanza a los 10 s.
    assert math.isclose(flujo(res["t_entrada"]), B * a**2, rel_tol=1e-12)
    assert math.isclose(flujo(50), B * a**2, rel_tol=1e-12)
    # Segunda vía: fem media = flujo total entre tiempo de entrada.
    assert math.isclose(B * a**2 / res["t_entrada"], res["fem"], rel_tol=1e-12)
    # Signo negativo con la normal según +z: corriente horaria vista desde +z.
    assert fem(5.0) < 0
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["fem"], 9e-6) and math.isclose(res["I"], 9e-7) and math.isclose(res["t_entrada"], 10)
