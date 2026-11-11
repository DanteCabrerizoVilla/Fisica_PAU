// Física de ondas: onda armónica y sonido. Funciones puras, sin dibujo,
// comprobadas contra valores de referencia (ver pruebas/). Unidades del SI.

// ---- Onda armónica ----------------------------------------------------------

/**
 * Onda armónica y(x,t) = A·f(ωt ∓ kx + φ0), con f = sen o cos.
 * `sentido`: +1 si avanza hacia las x positivas, −1 hacia las negativas.
 */
export function onda({ A, T, lambda, fase = 0, sentido = 1, coseno = false }) {
  const w = (2 * Math.PI) / T;
  const k = (2 * Math.PI) / lambda;
  const argumento = (x, t) => w * t - sentido * k * x + fase;
  const f = coseno ? Math.cos : Math.sin;
  const df = coseno ? (a) => -Math.sin(a) : Math.cos;
  return {
    A, T, lambda, fase, sentido, coseno, w, k,
    f: 1 / T,
    v: lambda / T,                 // velocidad de propagación
    vMax: A * w,                   // velocidad máxima de oscilación
    aMax: A * w * w,
    argumento,
    y: (x, t) => A * f(argumento(x, t)),
    vy: (x, t) => A * w * df(argumento(x, t)),
    ay: (x, t) => -w * w * A * f(argumento(x, t)),
  };
}

/**
 * Fases iniciales compatibles con una elongación y0 en (x0, t0). Devuelve las
 * dos soluciones en [0, 2π) con el signo de la velocidad de oscilación de cada una.
 */
export function fasesPosibles({ A, T, lambda, sentido = 1, coseno = false }, x0, t0, y0) {
  const cociente = Math.max(-1, Math.min(1, y0 / A));
  const base = (2 * Math.PI * t0) / T - (sentido * 2 * Math.PI * x0) / lambda;
  const candidatos = coseno
    ? [Math.acos(cociente), -Math.acos(cociente)]
    : [Math.asin(cociente), Math.PI - Math.asin(cociente)];
  const dosPi = 2 * Math.PI;
  return candidatos.map((arg) => {
    const fase = (((arg - base) % dosPi) + dosPi) % dosPi;
    const o = onda({ A, T, lambda, fase, sentido, coseno });
    return { fase, velocidad: o.vy(x0, t0) };
  });
}

// ---- Sonido -----------------------------------------------------------------

export const I0 = 1e-12; // W/m², intensidad umbral

export const intensidad = (P, r) => P / (4 * Math.PI * r * r);
export const nivel = (I) => 10 * Math.log10(I / I0);
export const intensidadDeNivel = (dB) => I0 * 10 ** (dB / 10);
/** Potencia de un foco que produce un nivel `dB` a una distancia r. */
export const potenciaDeNivel = (dB, r) => 4 * Math.PI * r * r * intensidadDeNivel(dB);

/** Intensidad total en un punto debida a varios focos [{P, x, y}] (se suman intensidades). */
export function intensidadTotal(focos, p) {
  return focos.reduce((suma, f) => suma + intensidad(f.P, Math.hypot(p.x - f.x, p.y - f.y)), 0);
}

/**
 * Punto del segmento que une dos focos donde ambos dan la misma intensidad.
 * Devuelve la distancia al primer foco.
 */
export function puntoIgualIntensidad(P1, P2, d) {
  return d / (1 + Math.sqrt(P2 / P1));
}
