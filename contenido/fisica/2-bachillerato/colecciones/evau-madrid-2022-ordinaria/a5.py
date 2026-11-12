"""Verificación de fis2b-evau-madrid-2022-ord-a5 (polonio-210)."""

import math

NA, M = 6.02e23, 210.0
m0, m_final = 30e-3, 5e-3        # g
T_dias = 138.38
DIA = 86400.0


def resolver() -> dict:
    tau_dias = T_dias / math.log(2)
    N0 = m0 / M * NA
    t_dias = tau_dias * math.log(m0 / m_final)
    return {"tau": tau_dias * DIA, "tau_dias": tau_dias, "actividad": N0 / (tau_dias * DIA),
            "tiempo": t_dias * DIA, "tiempo_dias": t_dias}


def comprobar(res: dict) -> None:
    lam = math.log(2) / (T_dias * DIA)
    assert math.isclose(1 / lam, res["tau"], rel_tol=1e-12)
    # Segunda vía para el tiempo: número de periodos, log2(30/5).
    assert math.isclose(res["tiempo_dias"], T_dias * math.log2(m0 / m_final), rel_tol=1e-12)
    # A ese tiempo quedan 5 mg.
    assert math.isclose(m0 * math.exp(-lam * res["tiempo"]), m_final, rel_tol=1e-12)
    assert 2 * T_dias < res["tiempo_dias"] < 3 * T_dias
    # Tercera vía para la actividad: desintegraciones en un segundo.
    assert math.isclose(m0 / M * NA * -math.expm1(-lam), res["actividad"], rel_tol=1e-6)
    # Solución orientativa oficial; su tiempo (356,7 días) arrastra redondeos.
    assert math.isclose(res["tau_dias"], 199.64, rel_tol=1e-4)
    assert math.isclose(res["actividad"], 4.99e12, rel_tol=2e-3)
    assert math.isclose(res["tiempo_dias"], 356.7, rel_tol=4e-3)
