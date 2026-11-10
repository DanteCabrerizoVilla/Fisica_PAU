"""Verificación de fis2b-pau-madrid-2026-ord-4b (desintegración beta del radio-228)."""

import math

# Datos del enunciado
m0 = 30.0            # g
A0 = 3.03e14         # Bq
masa_molar = 228.0   # g/mol
N_A = 6.02e23
t = 10 * 365 * 24 * 3600.0


def resolver() -> dict:
    N0 = m0 / masa_molar * N_A
    lam = A0 / N0
    periodo = math.log(2) / lam
    transformada = m0 * (1 - math.exp(-lam * t))
    return {"particulas": A0, "constante": lam, "periodo": periodo, "masa": transformada}


def comprobar(res: dict) -> None:
    # Masa restante por periodos de semidesintegración.
    restante = m0 * 0.5 ** (t / res["periodo"])
    assert math.isclose(m0 - restante, res["masa"], rel_tol=1e-12), "no coincide por periodos"
    # El periodo real del radio-228 es de 5,75 años.
    assert math.isclose(res["periodo"] / (365 * 86400), 5.75, rel_tol=5e-3)
    # Entre uno y dos periodos: queda entre la mitad y la cuarta parte.
    assert m0 / 4 < restante < m0 / 2
    # Valores de la solución orientativa oficial.
    for clave, oficial in (("constante", 3.83e-9), ("periodo", 1.81e8), ("masa", 21.02)):
        assert math.isclose(res[clave], oficial, rel_tol=3e-3), f"{clave} no coincide con la solución oficial"
