"""Verificación de fis2b-evau-madrid-2020-mod-b3 (dipolo de ±10 nC en micras)."""

import numpy as np

K, u = 9e9, 1e-6
cargas = [(10e-9, np.array([0, -6.0]) * u), (-10e-9, np.array([0, 6.0]) * u)]
A, B, qp = np.array([8.0, 0]) * u, np.array([8.0, 6]) * u, 5e-9


def campo(p):
    return sum(K * q * (p - c) / np.linalg.norm(p - c) ** 3 for q, c in cargas)


def potencial(p):
    return sum(K * q / np.linalg.norm(p - c) for q, c in cargas)


def resolver() -> dict:
    E = campo(A)
    return {"Ey": E[1], "V": potencial(A), "VB": potencial(B), "W": qp * (potencial(A) - potencial(B))}


def comprobar(res: dict) -> None:
    assert abs(campo(A)[0]) < 1e-3 * abs(res["Ey"])
    # Trabajo integrando la fuerza a lo largo del segmento vertical de A a B.
    ys = np.linspace(0, 6, 20001) * u
    Fy = np.array([qp * campo(np.array([8 * u, y]))[1] for y in ys])
    W = float(np.sum((Fy[1:] + Fy[:-1]) / 2 * np.diff(ys)))
    assert np.isclose(W, res["W"], rtol=1e-6)
    # Oficial: E = 1,08·10¹² j N/C, V = 0, V(8,6) = −5,04·10⁶ V (redondeo; sale −5,01·10⁶), W = 0,025 J.
    assert np.isclose(res["Ey"], 1.08e12) and abs(res["V"]) < 1e-6 and np.isclose(res["W"], 0.025, rtol=3e-3)
