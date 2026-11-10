"""Verificación de fis2b-pau-madrid-2027-mod-3b (espira que entra en un campo)."""

import math

# Datos del enunciado (SI)
L = 0.20
B = 0.200
v0 = 2.0
R = 15.0
t1, t2, t3 = 0.050, 0.150, 0.200


def flujo(t: float) -> float:
    """Flujo con la normal en el sentido de B: superficie dentro del campo por B."""
    dentro = min(max(v0 * t, 0.0), L)
    return B * L * dentro


def fem(t: float, h: float = 1e-6) -> float:
    """Ley de Faraday con derivada numérica."""
    return -(flujo(t + h) - flujo(t - h)) / (2 * h)


def resolver() -> dict:
    return {
        "flujo_1": flujo(t1),
        "flujo_2": flujo(t2),
        "fem_1": fem(t1) * 1e3,       # mV
        "fem_2": fem(t2),
        "intensidad": fem(t3) / R,
    }


def comprobar(res: dict) -> None:
    assert math.isclose(L / v0, 0.100), "la espira debe tardar 100 ms en entrar"
    # Fem de movimiento en el lado que corta el campo: B·L·v.
    assert math.isclose(abs(res["fem_1"]), B * L * v0 * 1e3, rel_tol=1e-6), "la fem no es B·L·v"
    assert math.isclose(res["flujo_2"], B * L**2, rel_tol=1e-12), "el flujo final no es B·L²"
    assert res["fem_2"] == 0 and res["intensidad"] == 0, "con la espira dentro no debe haber fem"
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["flujo_1"], 4e-3, rel_tol=1e-9) and math.isclose(res["fem_1"], -80, rel_tol=1e-6)
