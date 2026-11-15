"""Verificación de fis2b-evau-madrid-2018-mod-b2 (onda 0,01 sen[π(100t − 2,5x)])."""

import math
import numpy as np

A, w, k = 0.01, 100 * math.pi, 2.5 * math.pi


def resolver() -> dict:
    return {"v": w / k, "f": w / (2 * math.pi), "lam": 2 * math.pi / k, "k": k,
            "amax": A * w**2, "vmax": A * w}


def comprobar(res: dict) -> None:
    t = np.linspace(0, 0.02, 200001)
    y = A * np.sin(w * t - k * 0.37)
    v = np.gradient(y, t)
    a = np.gradient(v, t)
    assert math.isclose(np.max(np.abs(v)), res["vmax"], rel_tol=1e-4)
    assert math.isclose(np.max(np.abs(a[5:-5])), res["amax"], rel_tol=1e-4)
    # Una cresta avanza λ en un periodo.
    assert math.isclose(res["lam"] * res["f"], res["v"], rel_tol=1e-12)
