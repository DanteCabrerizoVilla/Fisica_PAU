// Carga en campos eléctrico y magnético uniformes. El campo magnético es
// perpendicular al plano del movimiento (componente Bz, positiva si sale del
// papel) y el eléctrico está en el plano. Funciones puras (ver pruebas/). SI.

export const E_CARGA = 1.6e-19;
export const U = 1.66e-27;
export const H = 6.63e-34;

export const PARTICULAS = {
  electron: { nombre: "Electrón", m: 9.1e-31, q: -1.6e-19 },
  proton: { nombre: "Protón", m: 1.67e-27, q: 1.6e-19 },
  alfa: { nombre: "Partícula alfa", m: 6.64e-27, q: 3.2e-19 },
};

/** Movimiento circular de una carga con velocidad v perpendicular a un campo B. */
export function giro({ m, q, v, B }) {
  const carga = Math.abs(q);
  return {
    fuerza: carga * v * Math.abs(B),
    radio: (m * v) / (carga * Math.abs(B)),
    periodo: (2 * Math.PI * m) / (carga * Math.abs(B)),
    frecuencia: (carga * Math.abs(B)) / (2 * Math.PI * m),
  };
}

/** Velocidad que pasa sin desviarse por campos E y B perpendiculares. */
export const velocidadSelector = (E, B) => Math.abs(E / B);

/** Velocidad de una carga acelerada desde el reposo por una diferencia de potencial (no relativista). */
export const velocidadTrasPotencial = (m, q, dV) => Math.sqrt((2 * Math.abs(q) * Math.abs(dV)) / m);

export const longitudDeBroglie = (m, v) => H / (m * v);

/** Fuerza de Lorentz en el plano: q(E + v × B), con B = (0, 0, Bz). */
export function fuerza(q, { vx, vy }, { Ex = 0, Ey = 0, Bz = 0 }) {
  return { x: q * (Ex + vy * Bz), y: q * (Ey - vx * Bz) };
}

/**
 * Un paso del método de Boris (conserva exactamente el módulo de la velocidad
 * cuando solo hay campo magnético). Modifica y devuelve el estado.
 */
export function paso(s, { qm, Ex = 0, Ey = 0, Bz = 0 }, dt) {
  // Medio impulso eléctrico
  let vx = s.vx + 0.5 * qm * Ex * dt;
  let vy = s.vy + 0.5 * qm * Ey * dt;
  // Giro magnético
  const tt = 0.5 * qm * Bz * dt;
  const ss = (2 * tt) / (1 + tt * tt);
  const px = vx + vy * tt;
  const py = vy - vx * tt;
  vx += py * ss;
  vy -= px * ss;
  // Medio impulso eléctrico
  vx += 0.5 * qm * Ex * dt;
  vy += 0.5 * qm * Ey * dt;
  // Posición con la velocidad media del paso (segundo orden).
  s.x += 0.5 * (s.vx + vx) * dt;
  s.y += 0.5 * (s.vy + vy) * dt;
  s.vx = vx;
  s.vy = vy;
  s.t += dt;
  return s;
}

/** Trayectoria completa: lista de puntos [x, y] durante un tiempo dado. */
export function trayectoria(inicial, campos, tiempo, pasos = 1500) {
  const s = { ...inicial, t: 0 };
  const puntos = [[s.x, s.y]];
  const dt = tiempo / pasos;
  for (let i = 0; i < pasos; i++) {
    paso(s, campos, dt);
    puntos.push([s.x, s.y]);
  }
  return puntos;
}
