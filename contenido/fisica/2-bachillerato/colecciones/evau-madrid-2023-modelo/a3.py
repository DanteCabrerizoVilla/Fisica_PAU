"""Verificación de fis2b-evau-madrid-2023-mod-a3 (corteza esférica cargada)."""

import math

import numpy as np

K = 9e9
R, sigma, q = 0.03, 2e-6, 1e-9


def resolver() -> dict:
    Q = sigma * 4 * math.pi * R**2
    r = math.hypot(2, 3)
    E = K * Q / r**2
    W = q * (K * Q / 2 - K * Q / 3)
    return {"E_dentro": 0.0, "E": E, "E_x": E * 2 / r, "E_y": E * 3 / r, "W": W}


def campo_numerico(p, n=400):
    """Suma directa del campo de la corteza troceada en n×2n parches."""
    p = np.asarray(p, dtype=float)
    theta = (np.arange(n) + 0.5) * math.pi / n
    phi = (np.arange(2 * n) + 0.5) * math.pi / n
    T, F = np.meshgrid(theta, phi, indexing="ij")
    pts = R * np.stack([np.sin(T) * np.cos(F), np.sin(T) * np.sin(F), np.cos(T)], axis=-1)
    dq = sigma * R**2 * np.sin(T) * (math.pi / n) ** 2
    d = p - pts
    dist = np.linalg.norm(d, axis=-1)
    return K * np.sum((dq / dist**3)[..., None] * d, axis=(0, 1)), K * np.sum(dq / dist)


def comprobar(res: dict) -> None:
    # Segunda vía: integrar numéricamente el campo de la corteza, sin usar Gauss.
    E_in, _ = campo_numerico([0.01, 0.01, 0])
    E_out, _ = campo_numerico([2, 3, 0])
    assert np.linalg.norm(E_in) < 1e-3 * K * sigma * 4 * math.pi, "dentro el campo debe anularse"
    assert math.isclose(E_out[0], res["E_x"], rel_tol=1e-4)
    assert math.isclose(E_out[1], res["E_y"], rel_tol=1e-4)
    assert abs(E_out[2]) < 1e-9
    _, VA = campo_numerico([0, 2, 0])
    _, VB = campo_numerico([3, 0, 0])
    assert math.isclose(q * (VA - VB), res["W"], rel_tol=1e-4)
    assert math.isclose(math.hypot(res["E_x"], res["E_y"]), res["E"], rel_tol=1e-12)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["E"], 15.66, rel_tol=1e-3)
    assert math.isclose(res["W"], 3.39e-8, rel_tol=2e-3)
