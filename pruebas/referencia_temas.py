"""Valores de referencia para las simulaciones de ondas, campos, óptica,
inducción y física moderna.

Se calculan por caminos distintos de los del código JavaScript siempre que es
posible:

- ondas: velocidad y aceleración de oscilación por derivación numérica;
- campos de cargas: con números complejos, y el campo como −gradiente numérico
  del potencial;
- hilos: integrando la ley de Biot-Savart sobre un hilo muy largo;
- refracción: ley de Snell en forma vectorial, sin fórmulas de ángulos;
- inducción: fem como derivada numérica del flujo;
- desintegración y carga en campos: integrando la ecuación diferencial con SciPy;
- relatividad: resolviendo numéricamente la velocidad y con E² = (pc)² + (m₀c²)².

Escribe temas.ref.json, que la página de pruebas compara con la simulación.
"""

import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

K, G, MU0 = 9e9, 6.67e-11, 4e-7 * math.pi
H, C, E, M_E = 6.63e-34, 3e8, 1.6e-19, 9.1e-31
I0 = 1e-12

ref = {}

# ---- Ondas ------------------------------------------------------------------
ondas = []
for A, T, lam, fase, sentido, coseno in [
    (0.05, 0.02, 0.4, 0.0, 1, False),
    (0.02, 0.5, 1.5, math.pi / 3, -1, False),
    (0.1, 2.0, 4.0, math.pi / 2, 1, True),
    (3e-3, 1 / 440, 340 / 440, 1.2, -1, True),
]:
    f = math.cos if coseno else math.sin
    y = lambda x, t: A * f(2 * math.pi * (t / T - sentido * x / lam) + fase)
    puntos = []
    for x, t in [(0.0, 0.0), (0.13 * lam, 0.31 * T), (1.7 * lam, 2.2 * T), (-0.4 * lam, 0.75 * T)]:
        h = T * 1e-5
        vy = (y(x, t + h) - y(x, t - h)) / (2 * h)
        ay = (y(x, t + h) - 2 * y(x, t) + y(x, t - h)) / h**2
        puntos.append({"x": x, "t": t, "y": y(x, t), "vy": vy, "ay": ay})
    ondas.append({"A": A, "T": T, "lambda": lam, "fase": fase, "sentido": sentido, "coseno": coseno,
                  "v": lam / T, "puntos": puntos})
ref["ondas"] = ondas

sonido = []
for focos, p in [
    ([(0.05, 0, 0)], (3, 4)),
    ([(1e-3, 0, 3), (4e-3, 4, 0)], (0, 0)),
    ([(2.0, -1, 0), (0.5, 2, 1), (1.2, 0, 5)], (1.5, 2.5)),
]:
    total = sum(P / (4 * math.pi * ((p[0] - x) ** 2 + (p[1] - y) ** 2)) for P, x, y in focos)
    sonido.append({"focos": [{"P": P, "x": x, "y": y} for P, x, y in focos], "p": {"x": p[0], "y": p[1]},
                   "I": total, "dB": 10 * math.log10(total / I0)})
ref["sonido"] = sonido
# Punto de igual intensidad entre dos focos, buscado numéricamente.
ref["igual"] = []
for P1, P2, d in [(1.0, 4.0, 6.0), (3e-3, 1e-3, 10.0), (2.0, 2.0, 5.0)]:
    x = brentq(lambda x: P1 / x**2 - P2 / (d - x) ** 2, 1e-6, d - 1e-6, xtol=1e-14)
    ref["igual"].append({"P1": P1, "P2": P2, "d": d, "x": x})

# ---- Cargas y masas ---------------------------------------------------------
def campo_complejo(fuentes, p, k):
    z = complex(*p)
    total = sum(k * q * (z - complex(x, y)) / abs(z - complex(x, y)) ** 3 for q, x, y in fuentes)
    return total.real, total.imag

def potencial(fuentes, p, k):
    return sum(k * q / math.hypot(p[0] - x, p[1] - y) for q, x, y in fuentes)

radiales = []
for k, fuentes, a, b, prueba in [
    (K, [(2e-6, 0, 0), (-3e-6, 0.4, 0)], (0.2, 0.3), (0.1, -0.2), 1e-9),
    (K, [(5e-9, -0.03, 0), (5e-9, 0.03, 0), (-2e-9, 0, 0.04)], (0, -0.04), (0.02, 0.02), -1.6e-19),
    (-G, [(2, 0, 0), (4, 4, 0)], (0, 2), (1.5, 0), 0.5),
    (-G, [(5.97e24, 0, 0), (7.35e22, 3.84e8, 0)], (3.0e8, 5e7), (1e8, -2e7), 1000),
]:
    h = 1e-6 * math.hypot(a[0] - fuentes[0][1], a[1] - fuentes[0][2])
    gx = -(potencial(fuentes, (a[0] + h, a[1]), k) - potencial(fuentes, (a[0] - h, a[1]), k)) / (2 * h)
    gy = -(potencial(fuentes, (a[0], a[1] + h), k) - potencial(fuentes, (a[0], a[1] - h), k)) / (2 * h)
    ex, ey = campo_complejo(fuentes, a, k)
    radiales.append({
        "k": k, "fuentes": [{"valor": q, "x": x, "y": y} for q, x, y in fuentes],
        "a": {"x": a[0], "y": a[1]}, "b": {"x": b[0], "y": b[1]}, "prueba": prueba,
        "Ex": ex, "Ey": ey, "gradX": gx, "gradY": gy,
        "Va": potencial(fuentes, a, k), "W": prueba * (potencial(fuentes, a, k) - potencial(fuentes, b, k)),
    })
ref["radiales"] = radiales

# Punto de campo nulo entre dos cargas del mismo signo, y fuera con signos opuestos.
nulos = []
for q1, q2, d in [(2e-6, 8e-6, 0.3), (4.0, 1.0, 6.0), (1e-9, 1e-9, 0.1)]:
    nulos.append({"q1": q1, "q2": q2, "d": d, "x": d / (1 + math.sqrt(q2 / q1))})
for q1, q2, d in [(1e-6, -4e-6, 0.2), (-9e-9, 1e-9, 0.5)]:
    # |q1|/x² = |q2|/(x−d)²: fuera del segmento, del lado de la carga menor
    r = math.sqrt(abs(q2 / q1))
    x = d / (1 - r)
    nulos.append({"q1": q1, "q2": q2, "d": d, "x": x})
ref["nulos"] = nulos

# ---- Hilos: Biot-Savart integrado sobre un hilo de 2 km ----------------------
def campo_hilo(I, hx, hy, px, py, L=1e3):
    dx, dy = px - hx, py - hy
    d = math.hypot(dx, dy)
    # dB = μ0 I/(4π) · dz · d / (d² + z²)^{3/2}; con z = d·tan u queda cos u du / d
    integral, _ = quad(math.cos, -math.atan(L / d), math.atan(L / d), epsabs=0, epsrel=1e-13)
    modulo = MU0 * I / (4 * math.pi) * integral / d
    return -modulo * dy / d, modulo * dx / d          # k × r̂

hilos = []
for lista, p in [
    ([(5, 0, 0.06), (2.5, 0.06, 0)], (0.03, 0.05)),
    ([(10, 0, 0), (-10, 0.1, 0)], (0.05, 0)),
    ([(3, -0.02, 0), (3, 0.02, 0), (-6, 0, 0.05)], (0.01, 0.03)),
]:
    bx = sum(campo_hilo(I, x, y, *p)[0] for I, x, y in lista)
    by = sum(campo_hilo(I, x, y, *p)[1] for I, x, y in lista)
    hilos.append({"hilos": [{"valor": I, "x": x, "y": y} for I, x, y in lista], "p": {"x": p[0], "y": p[1]}, "Bx": bx, "By": by})
ref["hilos"] = hilos

# ---- Óptica -----------------------------------------------------------------
ref["lentes"] = [{"s": s, "f": f, "sIm": s * f / (s + f), "M": f / (s + f)}
                 for s, f in [(-12, 8), (-30, 10), (-5, 10), (-20, -15), (-0.25, 0.1), (-16, 8)]]
ref["espejos"] = [{"s": s, "f": f, "sIm": s * f / (s - f), "M": -f / (s - f)}
                  for s, f in [(-30, -10), (-15, -10), (-5, -10), (-20, 15), (-0.6, -0.2)]]

def refractar(d, n, n1, n2):
    """Snell vectorial. d: dirección unitaria; n: normal unitaria contraria a d. None si hay reflexión total."""
    eta = n1 / n2
    cos_i = -float(np.dot(d, n))
    sen2_t = eta**2 * (1 - cos_i**2)
    if sen2_t > 1:
        return None
    return eta * d + (eta * cos_i - math.sqrt(1 - sen2_t)) * n

def angulo(u, v):
    """Ángulo entre dos vectores del plano, preciso también cerca de 0."""
    return math.atan2(abs(float(u[0] * v[1] - u[1] * v[0])), float(np.dot(u, v)))

capas = []
for medios, espesores, inc in [
    ([1, 1.7, 1], [0.03], 48),
    ([1, 1.5, 1.33, 1], [0.02, 0.05], 30),
    ([1.33, 1.6, 1.4, 1.2, 1], [0.01, 0.02, 0.015], 20),
    ([1, 1.5, 1.33, 1], [0.02, 0.05], 0),
    ([1.5, 1.7, 1], [0.04], 50),          # reflexión total en la última cara
]:
    d = np.array([math.sin(math.radians(inc)), -math.cos(math.radians(inc))])
    normal = np.array([0.0, 1.0])
    avance = tiempo = 0.0
    reflexion = None
    for i in range(1, len(medios)):
        d = refractar(d, normal, medios[i - 1], medios[i])
        if d is None:
            reflexion = i - 1
            break
        if i < len(medios) - 1:
            e = espesores[i - 1]
            pasos = e / -d[1]
            avance += pasos * d[0]
            tiempo += pasos * medios[i] / C
    capas.append({"medios": medios, "espesores": espesores, "incidencia": math.radians(inc),
                  "reflexionEn": reflexion, "avance": avance, "tiempo": tiempo,
                  "salida": None if d is None else math.atan2(d[0], -d[1])})
ref["capas"] = capas

prismas = []
for n, A_g, inc_g, n_ext in [(1.66, 60, 50, 1), (1.5, 60, 48.59, 1), (1.5, 45, 30, 1), (1.6, 60, 20, 1), (1.7, 50, 40, 1.33), (1.52, 30, 0, 1)]:
    A, inc = math.radians(A_g), math.radians(inc_g)
    n1 = np.array([-math.cos(A / 2), math.sin(A / 2)])     # normal exterior de la cara de entrada
    n2 = np.array([math.cos(A / 2), math.sin(A / 2)])      # normal exterior de la cara de salida
    ang = -A / 2 + inc
    d0 = np.array([math.cos(ang), math.sin(ang)])
    d1 = refractar(d0, n1, n_ext, n)
    alfa = angulo(d1, -n1)
    gamma = angulo(d1, n2)
    d2 = refractar(d1, -n2, n, n_ext)
    caso = {"n": n, "A": A, "incidencia": inc, "nExt": n_ext, "alfa": alfa, "gamma": gamma, "sale": d2 is not None}
    if d2 is not None:
        caso["beta"] = angulo(d2, n2)
        caso["desviacion"] = angulo(d0, d2)
    prismas.append(caso)
ref["prismas"] = prismas

# ---- Física moderna ---------------------------------------------------------
foto = []
for lam, W in [(365e-9, 2.29), (850e-9, 2.29), (200e-9, 4.7), (450e-9, 2.1), (589e-9, 2.28)]:
    foton = H * C / lam
    ec = max(0.0, foton - W * E)
    foto.append({"lambda": lam, "W": W, "fotonJ": foton, "EcJ": ec, "hay": foton > W * E,
                 "lambda0": H * C / (W * E), "f0": W * E / H, "vMax": math.sqrt(2 * ec / M_E)})
ref["fotoelectrico"] = foto

desint = []
for lam, t in [(math.log(2) / 5730, 10000.0), (math.log(2) / 8.02, 20.0), (0.05, 100.0), (1.2e-4, 3000.0)]:
    sol = solve_ivp(lambda _t, N: -lam * N, (0, t), [1.0], rtol=1e-12, atol=1e-15)
    desint.append({"lambda": lam, "t": t, "fraccion": float(sol.y[0, -1])})
ref["desintegracion"] = desint

relat = []
for m0, ec in [(1.67e-27, 1.4e9 * E), (9.1e-31, 0.511e6 * E), (9.1e-31, 1e3 * E), (1.67e-27, 5e11 * E), (6.64e-27, 2e8 * E)]:
    e0 = m0 * C**2
    beta = brentq(lambda b: (1 / math.sqrt(1 - b * b) - 1) * e0 - ec, 0, 1 - 1e-15, xtol=1e-16, rtol=1e-15)
    total = e0 + ec
    relat.append({"m0": m0, "Ec": ec, "beta": beta, "E0": e0, "Etotal": total,
                  "p": math.sqrt(total**2 - e0**2) / C, "gamma": total / e0})
ref["relatividad"] = relat

# ---- Carga en campos --------------------------------------------------------
lorentz = []
for m, q, v, Bz, Ey, fraccion in [
    (40 * 1.66e-27, 3.2e-19, 2.4e5, -1.5, 0.0, 1.5),
    (9.1e-31, -1.6e-19, 2e6, 1e-3, 0.0, 0.8),
    (1.67e-27, 1.6e-19, 1e5, 0.2, 1e4, 1.2),
    (1.67e-27, 1.6e-19, 5e4, -0.2, -1e4, 1.0),      # selector: v = E/B, va recta
]:
    periodo = 2 * math.pi * m / (abs(q) * abs(Bz))
    tiempo = fraccion * periodo
    qm = q / m
    sol = solve_ivp(lambda _t, s: [s[2], s[3], qm * s[3] * Bz, qm * (Ey - s[2] * Bz)],
                    (0, tiempo), [0, 0, v, 0], rtol=1e-12, atol=1e-18, method="DOP853")
    lorentz.append({"m": m, "q": q, "v": v, "Bz": Bz, "Ey": Ey, "tiempo": tiempo,
                    "radio": m * v / (abs(q) * abs(Bz)), "periodo": periodo,
                    "x": float(sol.y[0, -1]), "y": float(sol.y[1, -1]),
                    "vx": float(sol.y[2, -1]), "vy": float(sol.y[3, -1])})
ref["lorentz"] = lorentz

# ---- Resultados de problemas de examen ya resueltos y verificados en la web ---
ref["oficiales"] = {
    "fotoelectrico_2026_ext": {"lambda": 365e-9, "W": 2.29, "Ec_eV": 1.12},
    "lamina_2026_ord": {"n": 1.7, "e": 0.03, "incidencia_grados": 48, "refraccion_grados": 25.9},
    "espectrometro_2025_ext": {"m": 40 * 1.66e-27, "q": 3.2e-19, "v": 2.4e5, "B": 1.5, "radio": 3.32e-2},
}

destino = Path(__file__).with_name("temas.ref.json")
destino.write_text(json.dumps(ref, indent=1), encoding="utf-8")
print(f"{destino.name}: {sum(len(v) for v in ref.values())} casos de referencia")
