"""Verificación de fis2b-evau-madrid-2020-mod-b4 (tres medios y reflexión total)."""

import math

c, n1, n2, n3, lam1 = 3e8, 1.6, 1.4, 1.2, 460e-9


def resolver() -> dict:
    return {
        "f": c / (n1 * lam1),
        "lam2": n1 * lam1 / n2,
        "ang": math.degrees(math.asin(n3 / n1)),
    }


def comprobar(res: dict) -> None:
    assert math.isclose(res["f"] * res["lam2"], c / n2, rel_tol=1e-12)
    t1 = math.radians(res["ang"])
    t2 = math.asin(n1 * math.sin(t1) / n2)
    assert math.isclose(math.degrees(t2), math.degrees(math.asin(n3 / n2)), rel_tol=1e-9)
    # Un poco por debajo, el rayo pasa al medio 3; un poco por encima, no.
    assert n1 * math.sin(t1 - 1e-3) / n3 < 1 < n1 * math.sin(t1 + 1e-3) / n3
    assert math.isclose(res["f"], 4.08e14, rel_tol=1e-3) and math.isclose(res["ang"], 48.59, rel_tol=1e-3)
