"""Verificación de fis2b-evau-madrid-2019-mod-a3 (electrón cerca de un hilo)."""

import numpy as np

mu0, I, e = 4e-7 * np.pi, 0.020, 1.6e-19
P, v = np.array([0, 5.0, 0]), np.array([0, 1e5, 0])


def campo_hilo(p):
    # Biot-Savart para un hilo en el eje z con corriente +z: B = μ0 I/(2π d) · (k × r̂)
    r = np.array([p[0], p[1], 0])
    d = np.linalg.norm(r)
    return mu0 * I / (2 * np.pi * d) * np.cross([0, 0, 1], r / d)


def resolver() -> dict:
    B = campo_hilo(P)
    F = -e * np.cross(v, B)
    return {"B": np.linalg.norm(B), "Fz": F[2]}


def comprobar(res: dict) -> None:
    B = campo_hilo(P)
    assert B[0] < 0 and abs(B[1]) < 1e-25 and abs(B[2]) < 1e-25
    # Circulación numérica de B en una circunferencia de radio 5 m: debe dar μ0·I.
    th = np.linspace(0, 2 * np.pi, 2001)[:-1]
    pts = np.stack([5 * np.cos(th), 5 * np.sin(th), 0 * th], axis=1)
    dl = np.stack([-np.sin(th), np.cos(th), 0 * th], axis=1) * 5 * (2 * np.pi / 2000)
    circ = sum(campo_hilo(p) @ d for p, d in zip(pts, dl))
    assert np.isclose(circ, mu0 * I, rtol=1e-9)
    # Oficial: B = 8·10⁻¹⁰ T, F = −1,28·10⁻²³ k N.
    assert np.isclose(res["Fz"], -1.28e-23) and np.isclose(res["B"], 8e-10)
