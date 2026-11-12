"""Verificación de fis2b-evau-madrid-2022-mod-b2 (sonómetro en un circo)."""

import math

I0 = 1e-12
r_faquir, nivel_faquir = 5.0, 80.0
nivel_uno, nivel_todos = 73.98, 90.97


def resolver() -> dict:
    P = I0 * 10 ** (nivel_faquir / 10) * 4 * math.pi * r_faquir**2
    I1 = I0 * 10 ** (nivel_uno / 10)
    r = math.sqrt(P / (4 * math.pi * I1))
    n = I0 * 10 ** (nivel_todos / 10) / I1
    return {"P": P, "r": r, "n": n}


def comprobar(res: dict) -> None:
    n = round(res["n"])
    assert abs(res["n"] - n) < 0.05, "el número de personas debe salir prácticamente entero"
    r = 10.0
    nivel = lambda potencia, dist: 10 * math.log10(potencia / (4 * math.pi * dist**2) / I0)
    # Con 50 personas a 10 m se recuperan las tres lecturas del sonómetro (con dos decimales).
    assert math.isclose(nivel(res["P"], r_faquir), nivel_faquir, abs_tol=1e-9)
    assert math.isclose(nivel(res["P"], r), nivel_uno, abs_tol=0.005)
    assert math.isclose(nivel(n * res["P"], r), nivel_todos, abs_tol=0.005)
    # Segunda vía en decibelios.
    assert math.isclose(r_faquir * 10 ** ((nivel_faquir - nivel_uno) / 20), res["r"], rel_tol=1e-9)
    assert math.isclose(10 ** ((nivel_todos - nivel_uno) / 10), res["n"], rel_tol=1e-9)
    # Valores de la solución orientativa oficial.
    assert math.isclose(res["P"], 0.03142, rel_tol=1e-3) and math.isclose(res["r"], 10, rel_tol=1e-3) and n == 50
