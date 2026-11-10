"""Verificación de fis2b-pau-madrid-2026-ext-4b (efecto fotoeléctrico en el potasio)."""

import math

# Datos del enunciado (SI)
h = 6.63e-34
e = 1.6e-19
c = 3e8
W0 = 2.29 * e
lambda_1 = 365e-9
lambda_2 = 850e-9


def resolver() -> dict:
    umbral = h * c / W0
    Ec = h * c / lambda_1 - W0
    return {"umbral": umbral, "Ec": Ec, "Ec_eV": Ec / e}


def comprobar(res: dict) -> None:
    assert lambda_1 < res["umbral"] < lambda_2, "solo la fuente de 365 nm debe estar por debajo del umbral"
    # Con la otra fuente la energía cinética saldría negativa.
    assert h * c / lambda_2 - W0 < 0
    # Segunda vía: en electronvoltios, con hc en eV·nm.
    hc_eV_nm = h * c / e * 1e9
    assert math.isclose(res["Ec_eV"], hc_eV_nm / 365 - 2.29, rel_tol=1e-9)
    assert math.isclose(hc_eV_nm / 850, 1.46, rel_tol=5e-3) and math.isclose(hc_eV_nm / 365, 3.41, rel_tol=5e-3)
    # Valores de la solución orientativa oficial.
    for clave, oficial in (("umbral", 5.43e-7), ("Ec", 1.78e-19), ("Ec_eV", 1.12)):
        assert math.isclose(res[clave], oficial, rel_tol=6e-3), f"{clave} no coincide con la solución oficial"
