"""Verificación de fis2b-pau-madrid-2026-ext-4a (desintegración del radón-222)."""

import math

# Datos del enunciado
fraccion_desintegrada_dia = 0.166
DIA = 86400.0
masa = 1e-3            # g
masa_molar = 222.0     # g/mol
N_A = 6.02e23
dias = 9


def resolver() -> dict:
    lam = -math.log(1 - fraccion_desintegrada_dia) / DIA
    periodo = math.log(2) / lam
    N0 = masa / masa_molar * N_A
    desintegrados = N0 * (1 - math.exp(-lam * dias * DIA))
    return {"constante": lam, "periodo": periodo, "desintegrados": desintegrados}


def comprobar(res: dict) -> None:
    N0 = masa / masa_molar * N_A
    # Atajo: cada día queda el 83,4 %.
    por_dias = N0 * (1 - (1 - fraccion_desintegrada_dia) ** dias)
    assert math.isclose(res["desintegrados"], por_dias, rel_tol=1e-12), "no coincide con 0,834^9"
    # El periodo real del radón-222 es de 3,82 días.
    assert math.isclose(res["periodo"] / DIA, 3.82, rel_tol=5e-3), "el periodo no son 3,82 días"
    # Por periodos de semidesintegración.
    por_periodos = N0 * (1 - 0.5 ** (dias * DIA / res["periodo"]))
    assert math.isclose(res["desintegrados"], por_periodos, rel_tol=1e-12)
    # Valores de la solución orientativa oficial (que redondea lambda a dos cifras).
    for clave, oficial in (("constante", 2.1e-6), ("periodo", 3.3e5), ("desintegrados", 2.19e18)):
        assert math.isclose(res[clave], oficial, rel_tol=6e-3), f"{clave} no coincide con la solución oficial"
