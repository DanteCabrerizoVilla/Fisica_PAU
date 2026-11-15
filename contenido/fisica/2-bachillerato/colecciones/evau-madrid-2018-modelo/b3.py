"""Verificación de fis2b-evau-madrid-2018-mod-b3 (varilla sobre raíles)."""

import math

L, d, R, t = 0.05, 0.10, 150.0, 0.2
B0, v = 0.020, 4.0


def flujo_a(s):
    return B0 * L * (d + v * s)


def flujo_b(s):
    return 5 * s**3 * L * d


def resolver() -> dict:
    return {"flujo_a": flujo_a(t), "I_a": B0 * L * v / R, "flujo_b": flujo_b(t), "I_b": 15 * t**2 * L * d / R}


def comprobar(res: dict) -> None:
    h = 1e-6
    for flujo, I in ((flujo_a, res["I_a"]), (flujo_b, res["I_b"])):
        fem = (flujo(t + h) - flujo(t - h)) / (2 * h)
        assert math.isclose(fem / R, I, rel_tol=1e-6)
    # Oficial: 0,0009 Wb y 2,67·10⁻⁵ A; 0,0002 Wb y 2·10⁻⁵ A.
    assert math.isclose(res["flujo_a"], 9e-4) and math.isclose(res["flujo_b"], 2e-4)
