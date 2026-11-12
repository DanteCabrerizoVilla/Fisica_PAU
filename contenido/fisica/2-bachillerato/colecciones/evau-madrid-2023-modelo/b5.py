"""Verificación de fis2b-evau-madrid-2023-mod-b5 (yodo-131 a partir de la gráfica de actividad)."""

import math

NA, M = 6.02e23, 131.0
A0 = 6e6                 # Bq, leído de la gráfica
T_dias = 8.0             # la actividad cae a 3 MBq a los 8 días
t_dias = 60.0
DIA = 86400.0


def resolver() -> dict:
    T = T_dias * DIA
    lam = math.log(2) / T
    N0 = A0 / lam
    N = N0 * math.exp(-lam * t_dias * DIA)
    return {"T": T, "constante": lam, "N0": N0, "masa": N / NA * M}


def comprobar(res: dict) -> None:
    # Segunda vía: mitades sucesivas. 60 días son 7,5 periodos.
    N = res["N0"] / 2 ** (t_dias / T_dias)
    assert math.isclose(N / NA * M, res["masa"], rel_tol=1e-12)
    # Tercera vía: integrar dN/dt = −λN paso a paso.
    n, pasos = res["N0"], 200000
    dt = t_dias * DIA / pasos
    for _ in range(pasos):
        n -= res["constante"] * n * dt
    assert math.isclose(n / NA * M, res["masa"], rel_tol=1e-4)
    # La gráfica: 3 MBq a los 8 días, 1,5 MBq a los 16 y 0,75 MBq a los 24.
    for dias, MBq in ((8, 3), (16, 1.5), (24, 0.75)):
        assert math.isclose(A0 * math.exp(-res["constante"] * dias * DIA), MBq * 1e6, rel_tol=1e-12)
    # La actividad a los 60 días corresponde a los núcleos que quedan.
    assert math.isclose(res["constante"] * N, A0 / 2**7.5, rel_tol=1e-12)
    # Solución orientativa oficial: redondea λ a 1,00e-6 y por eso difiere un 2 % en la masa.
    assert math.isclose(res["constante"], 1.00e-6, rel_tol=3e-3)
    assert math.isclose(res["N0"], 6.00e12, rel_tol=3e-3)
    assert math.isclose(res["masa"], 7.35e-12, rel_tol=0.025)
