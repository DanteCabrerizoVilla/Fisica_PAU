"""Verificación de fis2b-evau-madrid-2019-mod-b3 (teorema de Gauss para una carga puntual).

No hay resultados numéricos; se comprueba numéricamente que el flujo del campo de Coulomb
por una esfera vale q/ε0 sea cual sea el radio, y también por una superficie no esférica.
"""

import numpy as np

eps0 = 8.854e-12
K = 1 / (4 * np.pi * eps0)
q = 3e-9


def flujo_esfera(R, n=400):
    th = (np.arange(n) + 0.5) * np.pi / n
    ph = (np.arange(2 * n) + 0.5) * np.pi / n
    TH, PH = np.meshgrid(th, ph)
    dS = R**2 * np.sin(TH) * (np.pi / n) ** 2
    return np.sum(K * q / R**2 * dS)


def flujo_cubo(L, n=400):
    # Una cara del cubo de lado 2L centrado en la carga, por seis.
    s = (np.arange(n) + 0.5) / n * 2 * L - L
    X, Y = np.meshgrid(s, s)
    r = np.sqrt(X**2 + Y**2 + L**2)
    En = K * q * L / r**3
    return 6 * np.sum(En) * (2 * L / n) ** 2


def resolver() -> dict:
    return {}


def comprobar(res: dict) -> None:
    for R in (0.01, 1.0, 50.0):
        assert np.isclose(flujo_esfera(R), q / eps0, rtol=1e-4)
    assert np.isclose(flujo_cubo(0.3), q / eps0, rtol=1e-4)
