"""Valores de referencia para las simulaciones de órbitas.

Calcula por caminos independientes del código JavaScript:

- órbitas circulares: velocidad a partir del periodo de la tercera ley de
  Kepler, y energías sumando cinética y potencial;
- órbitas elípticas: posición, velocidad y área barrida integrando las
  ecuaciones de Newton con SciPy (no se usa la ecuación de Kepler);
- los resultados de dos preguntas del modelo oficial 2026-2027, tal como
  los da la solución orientativa.

Escribe orbitas.ref.json, que la página de pruebas compara con la simulación.
"""

import json
import math
from pathlib import Path

from scipy.integrate import solve_ivp

G = 6.67e-11

# (masa central, radio de la órbita, masa del satélite)
CIRCULARES = [
    (5.97e24, 6.37e6 + 600e3, 1200),      # problema de muestra
    (5.97e24, 6.37e6 + 400e3, 4.2e5),     # Estación Espacial
    (5.97e24, 4.2164e7, 3000),            # geoestacionario
    (7.35e22, 1.74e6 + 100e3, 500),       # órbita lunar baja
    (6.37e29, 3.14e9, 6 * 5.97e24),       # modelo 2027, pregunta 2.A
    (1.99e30, 1.496e11, 5.97e24),         # la Tierra alrededor del Sol
]

# (masa central, semieje mayor, excentricidad)
ELIPTICAS = [
    (1.99e30, 5.906e12, 0.244),           # Plutón
    (1.99e30, 5.79e10, 0.206),            # Mercurio
    (1.99e30, 1.496e11, 0.017),           # Tierra
    (1.99e30, 2.67e12, 0.967),            # cometa Halley
    (5.97e24, 2.66e7, 0.74),              # satélite Molniya
    (5.97e24, 1.0e7, 0.0),                # circular, como caso límite
]
FRACCIONES = [0.05, 0.13, 0.37, 0.5, 0.71, 0.94]   # instantes, en periodos


def circular(M: float, r: float, m: float) -> dict:
    T = 2 * math.pi * math.sqrt(r**3 / (G * M))     # tercera ley de Kepler
    v = 2 * math.pi * r / T
    Ec = 0.5 * m * v**2
    Ep = -G * M * m / r
    return {"M": M, "r": r, "m": m, "v": v, "T": T, "g": G * M / r**2, "Ec": Ec, "Ep": Ep,
            "Em": Ec + Ep, "vEscape": math.sqrt(2) * v, "L": m * r * v}


def eliptica(M: float, a: float, e: float) -> dict:
    mu = G * M
    rp, ra = a * (1 - e), a * (1 + e)
    # Velocidad en el pericentro por conservación de energía y momento angular.
    vp = math.sqrt(2 * mu * (1 / rp - 1 / ra) / (1 - (rp / ra) ** 2)) if e > 0 else math.sqrt(mu / a)
    T = 2 * math.pi * math.sqrt(a**3 / mu)

    def f(_, y):
        x, yy, vx, vy, _area = y
        r3 = (x * x + yy * yy) ** 1.5
        return [vx, vy, -mu * x / r3, -mu * yy / r3, 0.5 * (x * vy - yy * vx)]

    tiempos = [k * T for k in FRACCIONES]
    sol = solve_ivp(f, (0, tiempos[-1]), [rp, 0, 0, vp, 0], method="DOP853",
                    t_eval=tiempos, rtol=1e-13, atol=1e-3)
    estados = [
        {"t": t, "x": sol.y[0, i], "y": sol.y[1, i], "vx": sol.y[2, i], "vy": sol.y[3, i], "area": sol.y[4, i]}
        for i, t in enumerate(tiempos)
    ]
    return {"M": M, "a": a, "e": e, "rp": rp, "ra": ra, "vp": vp, "va": vp * rp / ra, "T": T,
            "Em_por_kg": 0.5 * vp**2 - mu / rp, "estados": estados}


def main() -> None:
    datos = {
        "G": G,
        "circulares": [circular(*c) for c in CIRCULARES],
        "elipticas": [eliptica(*c) for c in ELIPTICAS],
        # Resultados publicados en la solución orientativa del modelo 2026-2027.
        "oficial": {
            "2A": {"M": 6.37e29, "r": 3.14e9, "m": 6 * 5.97e24, "v": 1.16e5, "T": 1.70e5, "Em": -2.42e35},
            "2B": {"M": 1.99e30, "T": 248 * 365.25 * 86400, "e": 0.244,
                   "a": 5.9e12, "rp": 4.46e12, "ra": 7.34e12, "va": 3.69e3, "vp": 6.08e3},
        },
    }
    destino = Path(__file__).with_name("orbitas.ref.json")
    destino.write_text(json.dumps(datos, indent=1), encoding="utf-8")
    print(f"{len(CIRCULARES)} órbitas circulares y {len(ELIPTICAS)} elípticas de referencia en {destino.name}")


if __name__ == "__main__":
    main()
