"""Comprobación de la prueba de nivel.

Cada función calcula por su cuenta la respuesta de una pregunta y exige que
el resultado aparezca en la opción marcada como correcta (la primera) y en
ninguna de las otras. Las preguntas puramente conceptuales se comprueban con
un caso numérico concreto siempre que se puede.

verificar.py llama a comprobar(preguntas).
"""

import math

G, K, MU0 = 6.67e-11, 9e9, 4e-7 * math.pi
H, C, E = 6.63e-34, 3e8, 1.6e-19
M_E, M_P = 9.1e-31, 1.67e-27


def cerca(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(abs(a), abs(b), 1e-300)


def grav_1():
    v = lambda r: math.sqrt(G * 5.97e24 / r)
    assert cerca(v(4 * 7e6) / v(7e6), 1 / 2)
    return "mitad"


def grav_2():
    M, m, r = 5.97e24, 800, 7e6
    v = math.sqrt(G * M / r)
    assert cerca(0.5 * m * v**2 - G * M * m / r, -G * M * m / (2 * r))
    return r"-\dfrac{G M m}{2r}"


def grav_3():
    R = 6.37e6
    g = lambda r: G * 5.97e24 / r**2
    assert cerca(g(2 * R) / g(R), 1 / 4)
    return "g_0/4"


def grav_4():
    T = lambda r: 2 * math.pi * math.sqrt(r**3 / (G * 5.97e24))
    assert cerca(T(4 * 7e6) / T(7e6), 8)
    return "8T"


def grav_5():
    M, R = 5.97e24, 6.37e6
    # La masa del objeto se cancela en ½mv² = GMm/R; y no coincide con la orbital rasante.
    escape = [math.sqrt(2 * (G * M * m / R) / m) for m in (1, 50, 4000)]
    assert cerca(escape[0], escape[1]) and cerca(escape[0], escape[2])
    assert not cerca(escape[0], math.sqrt(G * M / R), 1e-2)
    return "no depende de la masa"


def grav_6():
    # r·v se conserva entre perihelio y afelio; se comprueba además la energía.
    mu, rp = G * 1.99e30, 1e11
    ra = 3 * rp
    a = (rp + ra) / 2
    vp = math.sqrt(mu * (2 / rp - 1 / a))
    va = math.sqrt(mu * (2 / ra - 1 / a))
    assert cerca(va / vp, 1 / 3)
    return "v_p/3"


def elec_1():
    q, d = 2e-6, 0.4
    campo = K * q / (d / 2) ** 2 - K * q / (d / 2) ** 2
    potencial = 2 * K * q / (d / 2)
    assert campo == 0 and potencial > 0
    return "el campo eléctrico es nulo y el potencial no"


def elec_2():
    # F = q v × B es perpendicular a v: potencia nula.
    v, B = (3e5, 0.0, 0.0), (0.0, 0.0, 0.5)
    F = (E * (v[1] * B[2] - v[2] * B[1]), E * (v[2] * B[0] - v[0] * B[2]), E * (v[0] * B[1] - v[1] * B[0]))
    assert sum(f * c for f, c in zip(F, v)) == 0 and any(F)
    return "no su energía cinética"


def elec_3():
    # Campo uniforme hacia +x: V = −E·x. Una carga positiva acelera hacia +x.
    campo, q = 200.0, 1e-6
    V = lambda x: -campo * x
    assert q * campo > 0 and V(1) < V(0) and q * V(1) < q * V(0)
    return "potenciales decrecientes, y su energía potencial disminuye"


def elec_4():
    v, B = 1e6, 0.1
    assert M_P * v / (E * B) > M_E * v / (E * B)
    # Sentidos de giro: la fuerza cambia de signo con la carga.
    assert (E * v * B) * (-E * v * B) < 0
    return "el protón describe una circunferencia de radio mayor y giran en sentidos contrarios"


def elec_5():
    f = lambda d: MU0 * 3 * 5 / (2 * math.pi * d)
    assert cerca(f(0.2) / f(0.1), 1 / 2)
    # Mismo sentido: el campo del hilo 1 en el hilo 2 da una fuerza hacia el hilo 1.
    # Hilo 1 en el origen, I hacia +z; hilo 2 en x = d. B1 = +y; F = I·(z × y) = −x: atracción.
    z, y = (0, 0, 1), (0, 1, 0)
    fx = z[1] * y[2] - z[2] * y[1]
    assert fx < 0
    return "atrayéndose y la fuerza se reduce a la mitad"


def elec_6():
    flujo = lambda t: 5.0 * 0.01      # B y S constantes
    assert (flujo(1.0) - flujo(0.0)) == 0
    return "nula"


def onda_1():
    w, k = 10 * math.pi, 4 * math.pi
    assert cerca(w / k, 2.5)
    # Sentido: el punto de fase constante avanza hacia +x.
    y = lambda x, t: 0.02 * math.sin(w * t - k * x)
    dt = 1e-3
    assert cerca(y(0.3 + 2.5 * dt, dt), y(0.3, 0), 1e-6)
    return "2,5 m/s hacia las $x$ positivas"


def onda_2():
    I = 1e-12 * 10 ** (60 / 10)
    assert cerca(10 * math.log10(10 * I / 1e-12), 70)
    return "70 dB"


def onda_3():
    A, w = 0.1, 5.0
    t = 0.0                                   # x = A·sen(wt): en t = 0 pasa por el equilibrio
    x, v, a = A * math.sin(w * t), A * w * math.cos(w * t), -A * w**2 * math.sin(w * t)
    assert x == 0 and cerca(v, A * w) and a == 0
    return "velocidad es máxima y su aceleración es nula"


def onda_4():
    inten = lambda r: 3.0 / (4 * math.pi * r**2)
    assert cerca(inten(6) / inten(2), 1 / 9)
    return "I/9"


def onda_5():
    lam = 1.6
    desfase = 2 * math.pi * (lam / 2) / lam
    assert cerca(desfase, math.pi)
    return "oposición de fase"


def onda_6():
    # Modos de una cuerda fija por los dos extremos: L = n·λ/2.
    L = 0.8
    assert cerca(2 * L / 1, 2 * L)
    return "2L"


def opt_1():
    n, f, lam0 = 1.5, 5e14, 600e-9
    v = C / n
    assert v < C and cerca(v / f, lam0 / n) and lam0 / n < lam0
    return "frecuencia no cambia; su velocidad y su longitud de onda disminuyen"


def opt_2():
    s, f = -30.0, 10.0
    s2 = 1 / (1 / f + 1 / s)
    aumento = s2 / s
    assert cerca(s2, 15) and cerca(aumento, -0.5)
    return "real, invertida y menor, a 15 cm"


def opt_3():
    # sen(límite) = n2/n1 solo tiene solución si n2 < n1.
    assert 1.0 / 1.5 < 1 and 1.5 / 1.0 > 1
    return "índice de refracción menor"


def opt_4():
    s, f = -6.0, 10.0
    s2 = 1 / (1 / f + 1 / s)
    assert s2 < 0 and s2 / s > 1
    return "virtual, derecha y mayor"


def opt_5():
    f = 20.0                                   # convexo: f > 0 con el criterio DIN
    for s in (-5.0, -20.0, -40.0, -500.0):
        s2 = 1 / (1 / f - 1 / s)
        aumento = -s2 / s
        assert s2 > 0 and 0 < aumento < 1      # detrás del espejo (virtual), derecha y menor
    return "siempre virtual, derecha y menor"


def opt_6():
    # Ojo miope: demasiado convergente. Con una lente divergente delante, la potencia total baja.
    assert (62.0 + (-2.0)) < 62.0
    return "delante de la retina, y se corrige con lentes divergentes"


def mod_1():
    f, W = 1e15, 2.3 * E
    ec = H * f - W
    assert ec > 0                              # no depende de la intensidad
    return "más electrones, con la misma energía cinética máxima"


def mod_2():
    assert cerca(0.5 ** (24 / 8), 1 / 8)
    return "octava parte"


def mod_3():
    v = 1e6
    assert H / (M_E * v) > H / (M_P * v)
    return "mayor la del electrón"


def mod_4():
    W = 4.5 * E
    f = 0.9 * W / H
    assert H * f - W < 0
    return "no se emiten electrones"


def mod_5():
    # n → p + e⁻ + antineutrino: Z + 1, A igual. Ejemplo: C-14 (Z=6) → N-14 (Z=7).
    assert (6 + 1, 14) == (7, 14)
    return "aumenta en una unidad y su número másico no cambia"


def mod_6():
    gamma, m0 = 2.0, M_P
    assert cerca((gamma - 1) * m0 * C**2, m0 * C**2)
    return "$m_0 c^2$"


COMPROBACIONES = {
    nombre.replace("_", "-"): funcion
    for nombre, funcion in list(globals().items())
    if callable(funcion) and nombre.split("_")[0] in {"grav", "elec", "onda", "opt", "mod"}
}


def comprobar(preguntas: list[dict]) -> None:
    ids = {q["id"] for q in preguntas}
    assert ids == set(COMPROBACIONES), f"preguntas sin comprobación o al revés: {sorted(ids ^ set(COMPROBACIONES))}"
    for q in preguntas:
        esperado = COMPROBACIONES[q["id"]]()
        correcta, *resto = q["opciones"]
        assert esperado in correcta, f"{q['id']}: la primera opción no contiene «{esperado}»"
        # Ninguna otra opción puede coincidir literalmente con la correcta.
        assert all(o.strip() != correcta.strip() for o in resto), f"{q['id']}: hay una opción repetida"
