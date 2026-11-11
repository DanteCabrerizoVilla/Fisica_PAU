// Óptica geométrica paraxial con el criterio de signos DIN: distancias medidas
// desde la lente o el vértice del espejo, positivas hacia la derecha; la luz
// llega desde la izquierda. Funciones puras (ver pruebas/). Cualquier unidad
// de longitud vale, siempre que sea la misma en todos los datos.

/** Lente delgada: 1/s' − 1/s = 1/f'. Devuelve posición de la imagen y aumento. */
export function lente(s, f) {
  const inv = 1 / f + 1 / s;
  if (Math.abs(inv) < 1e-12) return { sIm: Infinity, M: Infinity, enInfinito: true };
  const sIm = 1 / inv;
  return { sIm, M: sIm / s, enInfinito: false };
}

/** Espejo esférico: 1/s' + 1/s = 1/f, con f = R/2. */
export function espejo(s, f) {
  const inv = 1 / f - 1 / s;
  if (Math.abs(inv) < 1e-12) return { sIm: Infinity, M: Infinity, enInfinito: true };
  const sIm = 1 / inv;
  return { sIm, M: -sIm / s, enInfinito: false };
}

/**
 * Dos lentes separadas una distancia d. Las posiciones de la segunda parte se
 * miden desde la segunda lente. Devuelve también el aumento total.
 */
export function dosLentes(s, f1, d, f2) {
  const primera = lente(s, f1);
  if (primera.enInfinito) {
    // Rayos paralelos entre las lentes: la imagen final se forma en el plano focal de la segunda.
    // Todos salen de la primera con pendiente −y/f1, y a la altura f2·(−y/f1) cortan ese plano.
    return { primera, s2: -Infinity, segunda: { sIm: f2, M: NaN, enInfinito: false }, M: -f2 / f1 };
  }
  const s2 = primera.sIm - d;
  const segunda = Math.abs(s2) < 1e-12 ? { sIm: 0, M: 1, enInfinito: false } : lente(s2, f2);
  return { primera, s2, segunda, M: primera.M * segunda.M };
}

/** Descripción de la imagen a partir de su posición y aumento. `esEspejo` invierte el criterio real/virtual. */
export function naturaleza(sIm, M, esEspejo = false) {
  if (!Number.isFinite(sIm)) return "en el infinito (rayos paralelos)";
  const real = esEspejo ? sIm < 0 : sIm > 0;
  const tam = Math.abs(Math.abs(M) - 1) < 1e-9 ? "del mismo tamaño" : Math.abs(M) > 1 ? "mayor" : "menor";
  return `${real ? "real" : "virtual"}, ${M > 0 ? "derecha" : "invertida"} y ${tam}`;
}

// ---- Trazado de rayos (para dibujar y para comprobar las fórmulas) ----------
// Un rayo se describe por su altura h al llegar a un elemento y su pendiente p
// (dy/dx, con x creciente en el sentido en que viaja la luz).

/** Rayo que sale de (s, y) con pendiente p: altura a la que corta el plano x = 0. */
export const alturaEnElemento = (s, y, p) => y - p * s;

/** Pendiente tras atravesar una lente delgada de focal f a la altura h. */
export const tras_lente = (h, p, f) => p - h / f;

/**
 * Pendiente tras reflejarse en un espejo de focal f a la altura h. El rayo
 * reflejado es la recta y = h + q·x, que se recorre hacia las x negativas.
 */
export const tras_espejo = (h, p, f) => -p - h / f;

/** Pendientes de los tres rayos principales que salen del extremo del objeto (s, y) hacia una lente. */
export function rayosPrincipalesLente(s, y, f) {
  const lista = [
    { nombre: "paralelo", p: 0 },
    { nombre: "centro", p: (0 - y) / (0 - s) },         // pasa por el centro de la lente
  ];
  if (Math.abs(-f - s) > 1e-9) lista.push({ nombre: "foco", p: (0 - y) / (-f - s) });  // pasa (o apunta) por el foco objeto
  return lista;
}

/** Pendientes de los rayos principales hacia un espejo: paralelo, por el foco y hacia el centro de curvatura. */
export function rayosPrincipalesEspejo(s, y, f) {
  const lista = [{ nombre: "paralelo", p: 0 }];
  if (Math.abs(f - s) > 1e-9) lista.push({ nombre: "foco", p: (0 - y) / (f - s) });
  if (Math.abs(2 * f - s) > 1e-9) lista.push({ nombre: "centro", p: (0 - y) / (2 * f - s) });
  return lista;
}

// ---- Refracción -------------------------------------------------------------

export const C_LUZ = 3e8; // m/s

/** Ángulo límite (rad) al pasar de un medio n1 a otro n2 < n1; null si no existe. */
export const anguloLimite = (n1, n2) => (n2 < n1 ? Math.asin(n2 / n1) : null);

/**
 * Rayo que atraviesa capas planas y paralelas. `medios` es la lista de índices
 * de refracción en el orden en que los recorre la luz (el primero y el último
 * son los medios exteriores) y `espesores` los de las capas intermedias (m).
 * Devuelve el ángulo en cada medio y, para cada capa, el avance lateral, el
 * camino y el tiempo. Si hay reflexión total, `reflexionEn` es el índice de la
 * superficie donde ocurre (0 = primera).
 */
export function capasPlanas(medios, espesores, incidencia) {
  const angulos = [incidencia];
  const tramos = [];
  let reflexionEn = null;
  const invariante = medios[0] * Math.sin(incidencia);   // n·sen θ se conserva
  for (let i = 1; i < medios.length; i++) {
    const seno = invariante / medios[i];
    if (seno > 1) { reflexionEn = i - 1; break; }
    const angulo = Math.asin(seno);
    angulos.push(angulo);
    if (i < medios.length - 1) {
      const e = espesores[i - 1];
      const camino = e / Math.cos(angulo);
      tramos.push({ n: medios[i], angulo, espesor: e, avance: e * Math.tan(angulo), camino, tiempo: (camino * medios[i]) / C_LUZ });
    }
  }
  return {
    angulos, tramos, reflexionEn,
    avanceTotal: tramos.reduce((s, x) => s + x.avance, 0),
    tiempoTotal: tramos.reduce((s, x) => s + x.tiempo, 0),
    anguloSalida: reflexionEn === null ? angulos[angulos.length - 1] : null,
  };
}

/**
 * Prisma de ángulo A e índice n en un medio de índice nExt. El rayo entra por
 * una cara con ángulo de incidencia i (rad). Devuelve los ángulos de la marcha.
 */
export function prisma({ n, A, incidencia, nExt = 1 }) {
  const alfa = Math.asin((nExt * Math.sin(incidencia)) / n);    // refracción en la primera cara
  const gamma = A - alfa;                                        // incidencia en la segunda cara
  const limite = Math.asin(nExt / n);
  const sale = Math.abs(gamma) < limite;
  const beta = sale ? Math.asin((n * Math.sin(gamma)) / nExt) : null;
  // Incidencia por debajo de la cual hay reflexión total en la segunda cara.
  const alfaCritica = A - limite;
  const senoMin = (n * Math.sin(alfaCritica)) / nExt;
  const incidenciaMinima = alfaCritica <= 0 ? 0 : senoMin >= 1 ? null : Math.asin(senoMin);
  return { alfa, gamma, limite, sale, beta, desviacion: sale ? incidencia + beta - A : null, incidenciaMinima };
}
