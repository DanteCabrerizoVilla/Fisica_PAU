"""Verificación de fis2b-evau-madrid-2018-mod-a3 (flujo y trabajo con una carga de 5 nC)."""

import math
from scipy.integrate import quad

K, q, R, qp = 9e9, 5e-9, 0.10, 2e-9


def resolver() -> dict:
    return {"flujo": 4 * math.pi * K * q, "W": qp * K * q / R}


def comprobar(res: dict) -> None:
    # Flujo: E(R)·4πR² para varios radios.
    for r in (0.05, 0.10, 2.0):
        assert math.isclose(K * q / r**2 * 4 * math.pi * r**2, res["flujo"], rel_tol=1e-12)
    # Trabajo externo = −(trabajo del campo) desde el infinito hasta R.
    W_campo = quad(lambda r: qp * K * q / r**2, R, math.inf)[0]   # el campo empuja hacia fuera
    assert math.isclose(W_campo, res["W"], rel_tol=1e-9)
    # Oficial: 564,97 V·m (con ε0 = 8,85·10⁻¹²) y 9·10⁻⁷ J.
    assert math.isclose(res["flujo"], 564.97, rel_tol=1e-3)
