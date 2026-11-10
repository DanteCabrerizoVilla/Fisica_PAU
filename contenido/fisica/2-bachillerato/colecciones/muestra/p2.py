"""Verificación del problema de muestra 2: efecto fotoeléctrico."""

import math

# Datos del enunciado (SI)
h = 6.63e-34
c = 3.00e8
e = 1.60e-19
W0_eV = 2.30
lam = 400e-9


def resolver() -> dict:
    W0 = W0_eV * e
    f0 = W0 / h
    Ec = h * c / lam - W0
    return {"f0": f0, "Ec_eV": Ec / e, "V_frenado": Ec / e}


def comprobar(res: dict) -> None:
    # La luz incidente debe superar la frecuencia umbral para que haya emisión.
    assert c / lam > res["f0"], "la luz no supera la frecuencia umbral"
    # Misma energía cinética trabajando en eV desde el principio.
    Ec_eV = h * c / (lam * e) - W0_eV
    assert math.isclose(res["Ec_eV"], Ec_eV, rel_tol=1e-9), "la energía cinética no coincide"
