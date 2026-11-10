"""Verificación de fis2b-evau-madrid-2024-ord-b5 (dos radioisótopos de igual masa)."""

import math

# Datos del enunciado (kBq, días)
A1_0, A1_1 = 10.00, 8.90
A2_0, A2_1 = 11.70, 10.77
t = 1.0


def periodo(a0: float, a: float) -> float:
    return t * math.log(2) / math.log(a0 / a)


def resolver() -> dict:
    T1, T2 = periodo(A1_0, A1_1), periodo(A2_0, A2_1)
    return {"T1": T1, "T2": T2, "cociente": A1_0 / A2_0 * T1 / T2}


def comprobar(res: dict) -> None:
    # Tras un día, cada actividad es la medida.
    assert math.isclose(A1_0 * 0.5 ** (t / res["T1"]), A1_1, rel_tol=1e-12)
    assert math.isclose(A2_0 * 0.5 ** (t / res["T2"]), A2_1, rel_tol=1e-12)
    # Segunda vía: elegir masas atómicas con ese cociente y comprobar las actividades iniciales.
    N_A, m = 6.02e23, 1e-9
    M1 = 100.0
    M2 = res["cociente"] * M1
    lam1, lam2 = math.log(2) / res["T1"], math.log(2) / res["T2"]
    act1, act2 = lam1 * m / M1 * N_A, lam2 * m / M2 * N_A
    assert math.isclose(act1 / act2, A1_0 / A2_0, rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["T1"], 5.95, rel_tol=2e-3) and math.isclose(res["T2"], 8.37, rel_tol=2e-3)
    assert math.isclose(res["cociente"], 0.61, rel_tol=1e-2)
