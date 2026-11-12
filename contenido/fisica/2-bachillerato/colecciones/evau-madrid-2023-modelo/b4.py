"""Verificación de fis2b-evau-madrid-2023-mod-b4 (índices a partir del ángulo límite y las velocidades)."""

import math

from scipy.optimize import fsolve

c, f = 3e8, 2.94e14
limite = math.radians(49.88)
suma_v = 4.07e8


def resolver() -> dict:
    nB = c * (1 + math.sin(limite)) / suma_v
    nA = nB / math.sin(limite)
    return {"nA": nA, "nB": nB, "lA": c / (nA * f), "lB": c / (nB * f)}


def comprobar(res: dict) -> None:
    # Segunda vía: resolver el sistema numéricamente, sin despejar a mano.
    def sistema(x):
        nA, nB = x
        return [nA * math.sin(limite) - nB, c / nA + c / nB - suma_v]
    nA, nB = fsolve(sistema, [1.5, 1.2])
    assert math.isclose(nA, res["nA"], rel_tol=1e-9) and math.isclose(nB, res["nB"], rel_tol=1e-9)
    assert res["nA"] > res["nB"] > 1, "la reflexión total exige n_A > n_B"
    # La frecuencia es la misma en los dos medios: v = λ·f en cada uno.
    assert math.isclose(res["lA"] * f + res["lB"] * f, suma_v, rel_tol=1e-12)
    # n·λ es la longitud de onda en el vacío en ambos medios.
    assert math.isclose(res["nA"] * res["lA"], res["nB"] * res["lB"], rel_tol=1e-12)
    # Valores de la solución orientativa oficial (que redondea los índices antes de seguir).
    assert math.isclose(res["nA"], 1.70, rel_tol=1e-3) and math.isclose(res["nB"], 1.30, rel_tol=1e-3)
    assert math.isclose(res["lA"], 600.24e-9, rel_tol=2e-3) and math.isclose(res["lB"], 784.93e-9, rel_tol=2e-3)
