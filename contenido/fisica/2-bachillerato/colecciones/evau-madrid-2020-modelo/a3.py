"""Verificación de fis2b-evau-madrid-2020-mod-a3 (electrón en campos E y B)."""

import numpy as np

q = -1.6e-19
v0, B, E = np.array([2.0, 0, 0]), np.array([0, 0, 3.0]), np.array([-1.0, 0, 0])


def resolver() -> dict:
    F = q * (E + np.cross(v0, B))
    dV = -E @ np.array([2.0, 0, 0])               # V(2,0,0) − V(0,0,0)
    return {"Fx": F[0], "Fy": F[1], "dV": dV, "W": q * (0 - dV)}


def comprobar(res: dict) -> None:
    # Trabajo directo: fuerza eléctrica por desplazamiento (la magnética es perpendicular a v).
    assert np.isclose(res["W"], (q * E) @ np.array([2.0, 0, 0]), rtol=1e-12)
    assert np.isclose(np.cross(v0, B) @ v0, 0)
    assert np.isclose(res["Fx"], 1.6e-19) and np.isclose(res["Fy"], 9.6e-19)
    assert res["dV"] > 0 and np.isclose(res["W"], 3.2e-19)
