"""Verificación de fis2b-evau-madrid-2020-ord-a1 (órbita sincrónica)."""

import math

G, M, r = 6.67e-11, 1.90e27, 1.59e8


def resolver() -> dict:
    v = math.sqrt(G * M / r)
    return {"v": v, "T": 2 * math.pi * r / v}


def comprobar(res: dict) -> None:
    assert math.isclose(res["T"], 2 * math.pi * math.sqrt(r**3 / (G * M)), rel_tol=1e-12)
    assert math.isclose(res["v"], 2.82e4, rel_tol=2e-3) and math.isclose(res["T"], 3.54e4, rel_tol=2e-3)
