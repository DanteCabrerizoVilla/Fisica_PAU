// Física de las órbitas: circular (satélites) y elíptica (leyes de Kepler).
// Funciones puras, sin dibujo, para poder comprobarlas contra valores de
// referencia (ver pruebas/). Unidades del SI en todo el archivo.

export const G = 6.67e-11; // N m² kg⁻², el valor que se da en el examen

// Masas y radios con los valores que suelen aparecer en los enunciados.
export const ASTROS = {
  tierra: { nombre: "Tierra", M: 5.97e24, R: 6.37e6 },
  luna: { nombre: "Luna", M: 7.35e22, R: 1.74e6 },
  marte: { nombre: "Marte", M: 6.42e23, R: 3.39e6 },
  jupiter: { nombre: "Júpiter", M: 1.9e27, R: 6.99e7 },
  sol: { nombre: "Sol", M: 1.99e30, R: 6.96e8 },
};

// ---- Órbita circular -------------------------------------------------------

/**
 * Satélite de masa m en órbita circular de radio r (desde el centro) en
 * torno a un astro de masa M.
 */
export function orbitaCircular({ M, r, m = 1 }) {
  const mu = G * M;
  const v = Math.sqrt(mu / r);
  const Ec = 0.5 * m * v * v;
  const Ep = (-mu * m) / r;
  return {
    r,
    v,
    T: (2 * Math.PI * r) / v,
    g: mu / (r * r),
    Ec,
    Ep,
    Em: Ec + Ep,
    energiaEscape: -(Ec + Ep),            // lo que falta para llegar a Em = 0
    vEscape: Math.sqrt((2 * mu) / r),     // partiendo del reposo a esa distancia
    L: m * r * v,
  };
}

/** Radio de la órbita circular (o semieje mayor) con periodo T: tercera ley de Kepler. */
export const radioDesdePeriodo = (M, T) => Math.cbrt((G * M * T * T) / (4 * Math.PI * Math.PI));

/** Magnitudes en la superficie de un astro de masa M y radio R. */
export function superficie({ M, R, m = 1 }) {
  const mu = G * M;
  return {
    g: mu / (R * R),
    vEscape: Math.sqrt((2 * mu) / R),
    Ep: (-mu * m) / R,
  };
}

/**
 * Energía que hay que dar a un cuerpo en reposo sobre la superficie para
 * dejarlo en órbita circular de radio r (no cuenta la rotación del astro).
 */
export const energiaPuestaEnOrbita = ({ M, R, r, m = 1 }) =>
  orbitaCircular({ M, r, m }).Em - superficie({ M, R, m }).Ep;

// ---- Órbita elíptica -------------------------------------------------------

/**
 * Elementos de una órbita elíptica de semieje mayor a y excentricidad e en
 * torno a un astro de masa M. El astro está en el foco.
 */
export function elipse({ M, a, e, m = 1 }) {
  const mu = G * M;
  const b = a * Math.sqrt(1 - e * e);
  const rp = a * (1 - e);
  const ra = a * (1 + e);
  const h = Math.sqrt(mu * a * (1 - e * e)); // momento angular por unidad de masa
  return {
    a, b, e, rp, ra, h,
    c: a * e,                                 // distancia del centro al foco
    T: 2 * Math.PI * Math.sqrt((a * a * a) / mu),
    vp: h / rp,
    va: h / ra,
    L: m * h,
    Em: (-mu * m) / (2 * a),
    velocidadAreolar: h / 2,                  // área barrida por segundo
    area: Math.PI * a * b,
  };
}

/**
 * Cambio de órbita: impulso en un extremo de la elipse ("lejano" o "cercano")
 * para pasar a la órbita circular de ese radio. Devuelve la velocidad antes y
 * después, el cambio de velocidad (positivo si hay que acelerar) y la energía
 * que hay que aportar a un cuerpo de masa m (negativa si hay que frenar).
 */
export function cambioACircular({ M, a, e, m = 1 }, donde = "lejano") {
  const el = elipse({ M, a, e, m });
  const r = donde === "lejano" ? el.ra : el.rp;
  const vAntes = donde === "lejano" ? el.va : el.vp;
  const vCircular = Math.sqrt((G * M) / r);
  return {
    r, vAntes, vCircular,
    deltaV: vCircular - vAntes,
    energia: (-G * M * m) / (2 * r) - el.Em,
  };
}

/** Resuelve la ecuación de Kepler, M = E − e·sen E, por el método de Newton. */
export function anomaliaExcentrica(media, e) {
  const dosPi = 2 * Math.PI;
  const M = ((media % dosPi) + dosPi) % dosPi;
  let E = e < 0.8 ? M : Math.PI;
  for (let i = 0; i < 60; i++) {
    const paso = (E - e * Math.sin(E) - M) / (1 - e * Math.cos(E));
    E -= paso;
    if (Math.abs(paso) < 1e-14) break;
  }
  return E;
}

/**
 * Posición y velocidad en el instante t, contado desde el paso por el
 * pericentro. Ejes con origen en el astro (foco) y el pericentro sobre +x;
 * el cuerpo gira en sentido antihorario.
 */
export function estadoEliptico({ M, a, e }, t) {
  const mu = G * M;
  const n = Math.sqrt(mu / (a * a * a));      // velocidad angular media
  const b = a * Math.sqrt(1 - e * e);
  const E = anomaliaExcentrica(n * t, e);
  const cosE = Math.cos(E);
  const sinE = Math.sin(E);
  const ritmo = n / (1 - e * cosE);           // dE/dt
  const x = a * (cosE - e);
  const y = b * sinE;
  const vx = -a * sinE * ritmo;
  const vy = b * cosE * ritmo;
  const r = Math.hypot(x, y);
  const v = Math.hypot(vx, vy);
  const senFi = (x * vy - y * vx) / (r * v);  // seno del ángulo entre r y v
  return { x, y, vx, vy, r, v, senFi, fi: Math.asin(Math.min(1, Math.max(-1, senFi))) };
}

/**
 * Área que barre el radio vector entre los instantes t1 y t2, medida sobre
 * la trayectoria (suma de triángulos), sin usar la ley de las áreas.
 */
export function areaBarrida(orbita, t1, t2, pasos = 400) {
  let area = 0;
  let previo = estadoEliptico(orbita, t1);
  for (let i = 1; i <= pasos; i++) {
    const actual = estadoEliptico(orbita, t1 + ((t2 - t1) * i) / pasos);
    area += 0.5 * (previo.x * actual.y - previo.y * actual.x);
    previo = actual;
  }
  return area;
}

// ---- Energías con masa y distancia cualesquiera ----------------------------

export const energiaCinetica = (m, v) => 0.5 * m * v * v;
export const energiaPotencial = (M, m, r) => (-G * M * m) / r;
