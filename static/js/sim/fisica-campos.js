// Campos creados por fuentes puntuales en el plano: cargas (campo eléctrico),
// masas (campo gravitatorio) e hilos rectos perpendiculares al plano (campo
// magnético). Funciones puras (ver pruebas/). Unidades del SI.

export const K = 9e9;                    // N m² C⁻²
export const G = 6.67e-11;               // N m² kg⁻²
export const MU0 = 4 * Math.PI * 1e-7;   // T m A⁻¹

/**
 * Campo de fuentes puntuales con ley 1/r²: k·valor·r̂/r² (se aleja de la fuente
 * si k·valor > 0). Con k = K son cargas; con k = −G, masas.
 */
export function campoRadial(fuentes, p, k) {
  let x = 0;
  let y = 0;
  for (const f of fuentes) {
    const dx = p.x - f.x;
    const dy = p.y - f.y;
    const d = Math.hypot(dx, dy);
    if (d === 0) return { x: NaN, y: NaN };
    x += (k * f.valor * dx) / d ** 3;
    y += (k * f.valor * dy) / d ** 3;
  }
  return { x, y };
}

/** Potencial de fuentes puntuales: suma de k·valor/r. */
export function potencial(fuentes, p, k) {
  return fuentes.reduce((suma, f) => suma + (k * f.valor) / Math.hypot(p.x - f.x, p.y - f.y), 0);
}

/** Trabajo que hace el campo al llevar una carga (o masa) de prueba de A a B. */
export const trabajo = (fuentes, a, b, k, prueba) => prueba * (potencial(fuentes, a, k) - potencial(fuentes, b, k));

/**
 * Campo magnético de hilos rectos indefinidos perpendiculares al plano.
 * `valor` es la intensidad, positiva si sale del plano (sentido +z).
 */
export function campoHilos(hilos, p) {
  let x = 0;
  let y = 0;
  for (const h of hilos) {
    const dx = p.x - h.x;
    const dy = p.y - h.y;
    const d2 = dx * dx + dy * dy;
    if (d2 === 0) return { x: NaN, y: NaN };
    const c = (MU0 * h.valor) / (2 * Math.PI * d2);   // módulo/d, con signo
    x += -c * dy;                                      // k × r = (−dy, dx)
    y += c * dx;
  }
  return { x, y };
}

/** Fuerza por unidad de longitud entre dos hilos paralelos separados d. */
export function fuerzaEntreHilos(I1, I2, d) {
  return { modulo: (MU0 * Math.abs(I1 * I2)) / (2 * Math.PI * d), atractiva: I1 * I2 > 0 };
}

/**
 * Puntos de la recta que pasa por p1 y p2 en los que se anula el campo dado
 * por `campo(p)`. Busca cambios de signo de la componente relevante y afina
 * por bisección. Devuelve como mucho dos puntos, con su parámetro t (0 en p1,
 * 1 en p2).
 */
export function puntosNulos(campo, p1, p2, { transversal = false } = {}) {
  const ux = p2.x - p1.x;
  const uy = p2.y - p1.y;
  const largo = Math.hypot(ux, uy);
  if (!(largo > 0)) return [];
  // Componente del campo a lo largo de la recta (o perpendicular a ella, para los hilos).
  const dir = transversal ? { x: -uy / largo, y: ux / largo } : { x: ux / largo, y: uy / largo };
  const g = (t) => {
    const c = campo({ x: p1.x + t * ux, y: p1.y + t * uy });
    return c.x * dir.x + c.y * dir.y;
  };
  const encontrados = [];
  const N = 2200;
  const T0 = -5;
  const T1 = 6;
  let tPrevio = T0;
  let gPrevio = g(T0);
  for (let i = 1; i <= N; i++) {
    const t = T0 + ((T1 - T0) * i) / N;
    const valor = g(t);
    // Se descartan los saltos de signo que ocurren al cruzar una fuente (el campo diverge).
    const cruzaFuente = (tPrevio < 0 && t >= 0) || (tPrevio < 1 && t >= 1);
    if (Number.isFinite(valor) && Number.isFinite(gPrevio) && valor * gPrevio <= 0 && gPrevio !== 0 && !cruzaFuente) {
      let a = tPrevio;
      let b = t;
      let ga = gPrevio;
      for (let k = 0; k < 60; k++) {
        const m = (a + b) / 2;
        const gm = g(m);
        if (ga * gm <= 0) b = m; else { a = m; ga = gm; }
      }
      const tm = (a + b) / 2;
      // Si en el punto hallado el campo no es realmente pequeño, era otra fuente sobre la recta.
      if (!(Math.abs(g(tm)) <= 1e-6 * Math.max(Math.abs(gPrevio), Math.abs(valor)))) {
        tPrevio = t;
        gPrevio = valor;
        continue;
      }
      encontrados.push({ t: tm, x: p1.x + tm * ux, y: p1.y + tm * uy });
      if (encontrados.length === 2) break;
    }
    tPrevio = t;
    gPrevio = valor;
  }
  return encontrados;
}
