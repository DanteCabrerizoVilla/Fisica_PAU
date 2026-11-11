"""Comprobación de la prueba de nivel.

Para cada variante de cada pregunta hay una función que calcula por su cuenta
la respuesta (con un caso numérico concreto siempre que se puede) y devuelve
el texto que debe aparecer en la opción marcada como correcta, la primera.

verificar.py llama a comprobar(preguntas).
"""

import math

G, K, MU0 = 6.67e-11, 9e9, 4e-7 * math.pi
H, C, E = 6.63e-34, 3e8, 1.6e-19
M_E, M_P = 9.1e-31, 1.67e-27
M_T, R_T = 5.97e24, 6.37e6


def cerca(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(abs(a), abs(b), 1e-300)


def v_orbital(r, M=M_T):
    return math.sqrt(G * M / r)


def periodo(r, M=M_T):
    return 2 * math.pi * math.sqrt(r**3 / (G * M))


def gravedad(r, M=M_T):
    return G * M / r**2


def lente(s, f):
    """Posición de la imagen y aumento (criterio DIN: s < 0 para un objeto real)."""
    s2 = 1 / (1 / f + 1 / s)
    return s2, s2 / s


def espejo(s, f):
    s2 = 1 / (1 / f - 1 / s)
    return s2, -s2 / s


def nivel(intensidad):
    return 10 * math.log10(intensidad / 1e-12)


# ---- Gravitación -------------------------------------------------------------

def grav_1a():
    assert cerca(v_orbital(4 * 7e6) / v_orbital(7e6), 1 / 2)
    return "mitad"


def grav_1b():
    assert cerca(v_orbital(9 * 7e6) / v_orbital(7e6), 1 / 3)
    return "tercera parte"


def grav_1c():
    assert cerca(v_orbital(7e6 / 4) / v_orbital(7e6), 2)
    return "cuarta parte"


def grav_2a():
    m, r = 800, 7e6
    assert cerca(0.5 * m * v_orbital(r) ** 2 - G * M_T * m / r, -G * M_T * m / (2 * r))
    return r"-\dfrac{G M m}{2r}"


def grav_2b():
    m, r = 800, 7e6
    ec = 0.5 * m * v_orbital(r) ** 2
    assert cerca(-G * M_T * m / r, -2 * ec)
    return "-2E_c"


def grav_2c():
    m, r = 800, 7e6
    ec = 0.5 * m * v_orbital(r) ** 2
    em = ec - G * M_T * m / r
    assert em < 0 and cerca(ec, -em)
    return "$-E$"


def grav_3a():
    assert cerca(gravedad(2 * R_T) / gravedad(R_T), 1 / 4)
    return "g_0/4"


def grav_3b():
    assert cerca(gravedad(2 * R_T) / gravedad(R_T), 1 / 4)      # misma masa, doble radio
    return "g_0/4"


def grav_3c():
    assert cerca(gravedad(R_T + 2 * R_T) / gravedad(R_T), 1 / 9)
    return "g_0/9"


def grav_4a():
    assert cerca(periodo(4 * 7e6) / periodo(7e6), 8)
    return "8T"


def grav_4b():
    assert cerca(periodo(4 * 7e6) / periodo(7e6), 8)            # periodo 8T ↔ radio 4r
    return "4r"


def grav_4c():
    assert cerca(periodo(9 * 1e11, 2e30) / periodo(1e11, 2e30), 27)
    return "27T"


def grav_5a():
    escape = [math.sqrt(2 * (G * M_T * m / R_T) / m) for m in (1, 50, 4000)]
    assert cerca(escape[0], escape[1]) and cerca(escape[0], escape[2])
    assert not cerca(escape[0], v_orbital(R_T), 1e-2)
    return "no depende de la masa"


def grav_5b():
    ve = lambda M: math.sqrt(2 * G * M / R_T)
    assert cerca(ve(4 * M_T) / ve(M_T), 2)
    return "el doble"


def grav_5c():
    m = 10.0
    ve = math.sqrt(2 * G * M_T / R_T)
    assert abs(0.5 * m * ve**2 - G * M_T * m / R_T) < 1e-6 * (G * M_T * m / R_T)
    return "nula"


def _elipse(rp, ra, mu=G * 1.99e30):
    a = (rp + ra) / 2
    return math.sqrt(mu * (2 / rp - 1 / a)), math.sqrt(mu * (2 / ra - 1 / a))


def grav_6a():
    vp, va = _elipse(1e11, 3e11)
    assert cerca(va / vp, 1 / 3)
    return "v_p/3"


def grav_6b():
    vp, va = _elipse(1e11, 2.5e11)
    assert vp > va
    return "máxima en el punto más cercano"


def grav_6c():
    vp, va = _elipse(1e11, 2e11)
    assert cerca(va / vp, 1 / 2)
    return "2r_p"


# ---- Electromagnetismo -------------------------------------------------------

def _campo_x(cargas, x):
    """Campo sobre el eje x de cargas [(q, posición)], con signo."""
    return sum(K * q * (x - x0) / abs(x - x0) ** 3 for q, x0 in cargas)


def _potencial(cargas, x):
    return sum(K * q / abs(x - x0) for q, x0 in cargas)


def elec_1a():
    cargas = [(2e-6, 0.0), (2e-6, 0.4)]
    assert abs(_campo_x(cargas, 0.2)) < 1e-6 and _potencial(cargas, 0.2) > 0
    return "el campo eléctrico es nulo y el potencial no"


def elec_1b():
    cargas = [(2e-6, 0.0), (-2e-6, 0.4)]
    assert abs(_potencial(cargas, 0.2)) < 1e-6 and abs(_campo_x(cargas, 0.2)) > 1
    return "el potencial es nulo y el campo eléctrico no"


def elec_1c():
    d = 0.6
    cargas = [(1e-6, 0.0), (4e-6, d)]
    assert abs(_campo_x(cargas, d / 3)) < 1e-6 * K * 1e-6 / (d / 3) ** 2
    return "$d/3$ de la carga $q$"


def _fuerza_magnetica(q, v, B):
    return (q * (v[1] * B[2] - v[2] * B[1]), q * (v[2] * B[0] - v[0] * B[2]), q * (v[0] * B[1] - v[1] * B[0]))


def elec_2a():
    v, B = (3e5, 0.0, 0.0), (0.0, 0.0, 0.5)
    F = _fuerza_magnetica(E, v, B)
    assert any(F) and sum(f * c for f, c in zip(F, v)) == 0
    return "no su energía cinética"


def elec_2b():
    assert not any(_fuerza_magnetica(-E, (0.0, 0.0, 2e5), (0.0, 0.0, 0.5)))
    return "línea recta con velocidad constante"


def elec_2c():
    for v in [(3e5, 0.0, 0.0), (1e5, -2e5, 4e4), (0.0, 7e4, 7e4)]:
        F = _fuerza_magnetica(E, v, (0.0, 0.0, 0.5))
        assert abs(sum(f * c for f, c in zip(F, v))) < 1e-25
    return "siempre nulo"


def elec_3a():
    campo, q = 200.0, 1e-6                     # campo uniforme hacia +x: V = −E·x
    V = lambda x: -campo * x
    assert q * campo > 0 and V(1) < V(0) and q * V(1) < q * V(0)
    return "potenciales decrecientes, y su energía potencial disminuye"


def elec_3b():
    campo, q = 200.0, -E
    V = lambda x: -campo * x
    assert q * campo < 0 and V(-1) > V(0) and q * V(-1) < q * V(0)   # se mueve hacia −x
    return "potenciales crecientes, y su energía potencial disminuye"


def elec_3c():
    q, V = 3e-6, 150.0
    assert q * (V - V) == 0
    return "nulo, sea cual sea el camino"


def _radio(m, q, v, B):
    return m * v / (abs(q) * B)


def elec_4a():
    assert _radio(M_P, E, 1e6, 0.1) > _radio(M_E, E, 1e6, 0.1)
    assert _fuerza_magnetica(E, (1e6, 0, 0), (0, 0, 0.1))[1] * _fuerza_magnetica(-E, (1e6, 0, 0), (0, 0, 0.1))[1] < 0
    return "el protón describe una circunferencia de radio mayor y giran en sentidos contrarios"


def elec_4b():
    T = lambda v: 2 * math.pi * _radio(M_P, E, v, 0.1) / v
    assert cerca(_radio(M_P, E, 2e5, 0.1) / _radio(M_P, E, 1e5, 0.1), 2) and cerca(T(2e5), T(1e5))
    return "el radio se duplica y el periodo no cambia"


def elec_4c():
    assert cerca(_radio(4 * M_P, 2 * E, 1e5, 0.1) / _radio(M_P, E, 1e5, 0.1), 2)
    return "el doble"


def _fuerza_hilos(i1, i2, d):
    """Fuerza por metro sobre el hilo 2 (en x = d) debida al hilo 1 (en x = 0); corrientes según z."""
    b1 = MU0 * i1 / (2 * math.pi * d)          # B1 = +y si i1 > 0
    return -i2 * b1                             # I2·(z × y) = −x


def elec_5a():
    assert _fuerza_hilos(3, 5, 0.1) < 0 and cerca(_fuerza_hilos(3, 5, 0.2) / _fuerza_hilos(3, 5, 0.1), 1 / 2)
    return "atrayéndose y la fuerza se reduce a la mitad"


def elec_5b():
    assert _fuerza_hilos(3, -5, 0.1) > 0 and cerca(_fuerza_hilos(6, -5, 0.1) / _fuerza_hilos(3, -5, 0.1), 2)
    return "repeliéndose y la fuerza se duplica"


def elec_5c():
    d, i = 0.1, 4.0
    b1 = MU0 * i / (2 * math.pi * (d / 2))      # hilo en x = 0: +y en el punto medio
    b2 = -MU0 * i / (2 * math.pi * (d / 2))     # hilo en x = d: −y en el punto medio
    assert b1 + b2 == 0
    return "nulo"


def elec_6a():
    flujo = lambda t: 5.0 * 0.01
    assert flujo(1.0) - flujo(0.0) == 0
    return "nula"


def elec_6b():
    w, BS = 50.0, 2e-4
    t = (math.pi / 2) / w                       # instante de fem máxima: sen(wt) = 1
    assert cerca(BS * w * math.sin(w * t), BS * w) and abs(BS * math.cos(w * t)) < 1e-12 * BS + 1e-18
    return "flujo magnético a través de la espira es nulo"


def elec_6c():
    # Ley de Lenz: el flujo inducido tiene signo contrario a la variación del flujo.
    variacion = +1.0
    assert -variacion < 0
    return "se opone al aumento del flujo"


# ---- Ondas ---------------------------------------------------------------------

def _avanza(A, w, k, signo):
    """True si y = A·sen(wt + signo·kx) se desplaza hacia las x positivas."""
    y = lambda x, t: A * math.sin(w * t + signo * k * x)
    dt = 1e-4
    return abs(y(0.3 + (w / k) * dt, dt) - y(0.3, 0)) < 1e-9


def onda_1a():
    w, k = 10 * math.pi, 4 * math.pi
    assert cerca(w / k, 2.5) and _avanza(0.02, w, k, -1)
    return "2,5 m/s hacia las $x$ positivas"


def onda_1b():
    w, k = 6 * math.pi, 2 * math.pi
    assert cerca(w / k, 3) and not _avanza(0.05, w, k, +1)
    return "3 m/s hacia las $x$ negativas"


def onda_1c():
    assert cerca(2 * math.pi / math.pi, 2) and cerca(2 * math.pi / (4 * math.pi), 0.5)
    return "2 m y 0,5 s"


def onda_2a():
    assert cerca(nivel(10 * 1e-12 * 10**6), 70)
    return "70 dB"


def onda_2b():
    assert cerca(nivel(1e-12 * 10**8 / 100), 60)
    return "60 dB"


def onda_2c():
    assert cerca(nivel(100 * 1e-12 * 10**7), 90)
    return "90 dB"


def _mas(fase, A=0.1, w=5.0):
    return A * math.sin(fase), A * w * math.cos(fase), -A * w**2 * math.sin(fase)


def onda_3a():
    x, v, a = _mas(0.0)
    assert x == 0 and cerca(v, 0.5) and a == 0
    return "velocidad es máxima y su aceleración es nula"


def onda_3b():
    x, v, a = _mas(math.pi / 2)
    assert cerca(x, 0.1) and abs(v) < 1e-12 and cerca(abs(a), 0.1 * 25)
    return "velocidad es nula y su aceleración es máxima"


def onda_3c():
    for fase in (0.3, 1.1, 2.5, 4.0):
        x, _, a = _mas(fase)
        assert cerca(a, -25 * x)
    return "proporcional a la elongación y de sentido contrario"


def _intensidad(P, r):
    return P / (4 * math.pi * r**2)


def onda_4a():
    assert cerca(_intensidad(3, 6) / _intensidad(3, 2), 1 / 9)
    return "I/9"


def onda_4b():
    assert cerca(_intensidad(3, 5) / _intensidad(3, 10), 4)
    return "5 m"


def onda_4c():
    assert cerca(_intensidad(6, 8) / _intensidad(3, 4), 1 / 2)
    return "mitad"


def _desfase(separacion, lam):
    return (2 * math.pi * separacion / lam) % (2 * math.pi)


def onda_5a():
    assert cerca(_desfase(0.8, 1.6), math.pi)
    return "oposición de fase"


def onda_5b():
    assert cerca(_desfase(2.4, 1.6), math.pi)
    return "oposición de fase"


def onda_5c():
    assert cerca(_desfase(1, 4), math.pi / 2)
    return r"\pi/2"


def onda_6a():
    L = 0.8
    assert cerca(2 * L / 1, 2 * L)              # L = n·λ/2 con n = 1
    return "2L"


def onda_6b():
    # y = 2A·sen(kx)·cos(wt): nodos donde kx = nπ, separados π/k = λ/2.
    lam = 1.2
    k = 2 * math.pi / lam
    assert cerca(math.pi / k, lam / 2)
    return "media longitud de onda"


def onda_6c():
    L = 0.8
    assert cerca(2 * L / 2, L)                  # n = 2
    return "$L$"


# ---- Óptica ----------------------------------------------------------------------

def opt_1a():
    n, f, lam0 = 1.5, 5e14, 600e-9
    assert C / n < C and cerca((C / n) / f, lam0 / n)
    return "frecuencia no cambia; su velocidad y su longitud de onda disminuyen"


def opt_1b():
    assert cerca(600 / 1.5, 400)
    return "400 nm"


def opt_1c():
    n = 1.33
    incidencia = math.radians(30)
    refraccion = math.asin(n * math.sin(incidencia))
    assert refraccion > incidencia and C > C / n
    return "se aleja de la normal y la luz se propaga más rápido"


def opt_2a():
    s2, m = lente(-30, 10)
    assert cerca(s2, 15) and cerca(m, -0.5)
    return "real, invertida y menor, a 15 cm"


def opt_2b():
    s2, m = lente(-20, 10)
    assert cerca(s2, 20) and cerca(m, -1)
    return "real, invertida y del mismo tamaño, a 20 cm"


def opt_2c():
    s2, m = lente(-15, 10)
    assert cerca(s2, 30) and cerca(m, -2)
    return "real, invertida y mayor, a 30 cm"


def opt_3a():
    assert 1.0 / 1.5 < 1 < 1.5 / 1.0            # sen(límite) = n2/n1 exige n2 < n1
    return "índice de refracción menor"


def opt_3b():
    assert cerca(math.degrees(math.asin(1 / 2)), 30)
    return "30°"


def opt_3c():
    limite = math.asin(1 / 1.33)
    assert 1.33 * math.sin(limite + 0.05) > 1   # no hay rayo refractado
    return "toda la luz se refleja"


def opt_4a():
    s2, m = lente(-6, 10)
    assert s2 < 0 and m > 1
    return "virtual, derecha y mayor"


def opt_4b():
    for s in (-3.0, -15.0, -40.0, -900.0):
        s2, m = lente(s, -15)
        assert s2 < 0 and 0 < m < 1
    return "siempre virtual, derecha y menor"


def opt_4c():
    # Con el objeto en el foco objeto, 1/s' = 1/f + 1/s = 0.
    assert 1 / 10 + 1 / (-10) == 0
    return "paralelos"


def opt_5a():
    for s in (-5.0, -20.0, -40.0, -500.0):
        s2, m = espejo(s, 20)                   # convexo: f > 0
        assert s2 > 0 and 0 < m < 1
    return "siempre virtual, derecha y menor"


def opt_5b():
    s2, m = espejo(-8, -20)                     # cóncavo: f < 0; objeto entre foco y espejo
    assert s2 > 0 and m > 1
    return "virtual, derecha y mayor"


def opt_5c():
    s2, m = espejo(-40, -20)
    assert cerca(s2, -40) and cerca(m, -1)
    return "real, invertida y del mismo tamaño"


def opt_6a():
    # Ojo demasiado convergente: una lente de potencia negativa reduce la potencia total.
    assert 62.0 + (-2.0) < 62.0
    return "delante de la retina, y se corrige con lentes divergentes"


def opt_6b():
    assert 58.0 + 2.0 > 58.0
    return "detrás de la retina, y se corrige con lentes convergentes"


def opt_6c():
    f = 1 / -2
    assert f < 0 and cerca(abs(f) * 100, 50)
    return "divergente, de 50 cm"


# ---- Física moderna --------------------------------------------------------------

def mod_1a():
    assert H * 1e15 - 2.3 * E > 0               # la energía de cada electrón no depende de la intensidad
    return "más electrones, con la misma energía cinética máxima"


def mod_1b():
    W = 2.3 * E
    assert H * 1.2e15 - W > H * 1e15 - W
    return "los mismos electrones, con más energía cinética máxima"


def mod_1c():
    # e·V = h·f − W: depende de f y del metal (W), no de la intensidad.
    V = lambda f, W: (H * f - W) / E
    assert V(1.2e15, 2.3 * E) != V(1e15, 2.3 * E) and V(1e15, 2.3 * E) != V(1e15, 3.0 * E)
    return "de la frecuencia de la luz y del metal, pero no de la intensidad"


def mod_2a():
    assert cerca(0.5 ** (24 / 8), 1 / 8)
    return "octava parte"


def mod_2b():
    assert cerca(800 * 0.5 ** (15 / 5), 100)
    return "100 Bq"


def mod_2c():
    assert cerca(0.5 ** (20 / 10), 1 / 4)
    return "10 días"


def mod_3a():
    assert H / (M_E * 1e6) > H / (M_P * 1e6)
    return "mayor la del electrón"


def mod_3b():
    assert cerca((H / (M_E * 2e6)) / (H / (M_E * 1e6)), 1 / 2)
    return "mitad"


def mod_3c():
    p = 3e-24
    assert H / p == H / p                       # λ = h/p solo depende de p
    return "la misma para los dos"


def mod_4a():
    W = 4.5 * E
    assert H * (0.9 * W / H) - W < 0
    return "no se emiten electrones"


def mod_4b():
    assert 5 - 2 == 3
    return "3 eV"


def mod_4c():
    assert cerca((4 * E / H) / (2 * E / H), 2)
    return "el doble"


def mod_5a():
    assert (6 + 1, 14) == (7, 14)               # C-14 → N-14
    return "aumenta en una unidad y su número másico no cambia"


def mod_5b():
    assert (92 - 2, 238 - 4) == (90, 234)       # U-238 → Th-234
    return "disminuye en dos unidades y su número másico en cuatro"


def mod_5c():
    assert (27 + 0, 60 + 0) == (27, 60)         # el fotón no tiene carga ni nucleones
    return "no cambian"


def mod_6a():
    assert cerca((2 - 1) * M_P * C**2, M_P * C**2)
    return "$m_0 c^2$"


def mod_6b():
    assert cerca(3 * M_P * C**2 / (M_P * C**2), 3)
    return "$3\\,m_0 c^2$"


def mod_6c():
    assert cerca(2 * 1.0, 2)                    # Δt = γ·Δt₀
    return "2 horas"


COMPROBACIONES = {
    nombre.replace("_", "-"): funcion
    for nombre, funcion in list(globals().items())
    if callable(funcion) and nombre.split("_")[0] in {"grav", "elec", "onda", "opt", "mod"}
}


def comprobar(preguntas: list[dict]) -> None:
    ids = {f"{q['id']}{'abcdefgh'[i]}" for q in preguntas for i in range(len(q["variantes"]))}
    assert ids == set(COMPROBACIONES), f"variantes sin comprobación o al revés: {sorted(ids ^ set(COMPROBACIONES))}"
    for q in preguntas:
        for i, variante in enumerate(q["variantes"]):
            ident = f"{q['id']}{'abcdefgh'[i]}"
            esperado = COMPROBACIONES[ident]()
            correcta, *resto = variante["opciones"]
            assert esperado in correcta, f"{ident}: la primera opción no contiene «{esperado}»"
            assert all(o.strip() != correcta.strip() for o in resto), f"{ident}: hay una opción repetida"
