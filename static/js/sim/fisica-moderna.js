// Física moderna: efecto fotoeléctrico, desintegración radiactiva y relatividad.
// Funciones puras (ver pruebas/). Constantes con los valores de los enunciados.

export const H = 6.63e-34;   // J s
export const C = 3e8;        // m/s
export const E = 1.6e-19;    // C (y julios por electronvoltio)
export const M_E = 9.1e-31;  // kg
export const N_A = 6.02e23;  // mol⁻¹
export const U = 1.66e-27;   // kg

// ---- Efecto fotoeléctrico ---------------------------------------------------

/**
 * Luz de longitud de onda `lambda` (m) sobre un metal de trabajo de extracción
 * `W_eV` (eV). Energías en eV salvo que se indique.
 */
export function fotoelectrico(lambda, W_eV) {
  const f = C / lambda;
  const fotonJ = H * f;
  const foton = fotonJ / E;
  const Ec = foton - W_eV;
  const hay = Ec > 0;
  return {
    f,
    foton, fotonJ,
    f0: (W_eV * E) / H,
    lambda0: (H * C) / (W_eV * E),
    hay,
    Ec: hay ? Ec : 0,
    EcJ: hay ? Ec * E : 0,
    Vfrenado: hay ? Ec : 0,                       // en voltios: numéricamente igual a Ec en eV
    vMax: hay ? Math.sqrt((2 * Ec * E) / M_E) : 0,
  };
}

/** Constante de Planck y trabajo de extracción (J) a partir de dos medidas (λ, V de frenado). */
export function planckDeDosMedidas(l1, V1, l2, V2) {
  const h = (E * (V1 - V2)) / (C * (1 / l1 - 1 / l2));
  return { h, W: (h * C) / l1 - E * V1 };
}

// ---- Desintegración radiactiva ----------------------------------------------

/** Constante de desintegración (s⁻¹) a partir del dato que dé el enunciado. */
export function constante({ tipo, valor }) {
  if (tipo === "T") return Math.LN2 / valor;   // periodo de semidesintegración (s)
  if (tipo === "tau") return 1 / valor;         // vida media (s)
  return valor;                                 // la propia constante (s⁻¹)
}

/**
 * Muestra radiactiva. Se da uno de: masa (g), actividad (Bq) o número de
 * núcleos, además de la masa molar (g/mol). Devuelve los tres valores iniciales.
 */
export function muestra({ tipo, valor, masaMolar }, lambda) {
  let N0;
  if (tipo === "masa") N0 = (valor / masaMolar) * N_A;
  else if (tipo === "actividad") N0 = valor / lambda;
  else N0 = valor;
  return { N0, A0: lambda * N0, m0: (N0 / N_A) * masaMolar };
}

export const fraccionRestante = (lambda, t) => Math.exp(-lambda * t);

/** Tiempo para que la muestra (o su actividad) se reduzca a una fracción dada. */
export const tiempoHastaFraccion = (lambda, fraccion) => -Math.log(fraccion) / lambda;

// ---- Relatividad ------------------------------------------------------------

export const gamma = (beta) => 1 / Math.sqrt(1 - beta * beta);

/** Partícula de masa en reposo m0 (kg) con velocidad beta·c. Energías en julios. */
export function relativista(m0, beta) {
  const g = gamma(beta);
  const E0 = m0 * C * C;
  return {
    gamma: g,
    m: g * m0,
    E0,
    Etotal: g * E0,
    Ec: (g - 1) * E0,
    EcClasica: 0.5 * m0 * (beta * C) ** 2,
    p: g * m0 * beta * C,
    v: beta * C,
  };
}

/** Velocidad (como fracción de c) de una partícula con energía cinética Ec (J). */
export function betaDeEnergiaCinetica(m0, Ec) {
  const g = 1 + Ec / (m0 * C * C);
  return Math.sqrt(1 - 1 / (g * g));
}
