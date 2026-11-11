// Inducción electromagnética: flujo y fem en los montajes típicos de examen.
// La normal a la espira se toma en el sentido del campo, de modo que el flujo
// es positivo y la fem es −dΦ/dt. Funciones puras (ver pruebas/). SI.

/** Espira rectangular (lado L perpendicular al avance, longitud a) que entra con velocidad v en un campo B. */
export function espiraEntrando({ B, L, a, v, N = 1 }) {
  const tEntrada = a / v;
  return {
    tMax: 2 * tEntrada,
    tEntrada,
    flujo: (t) => N * B * L * Math.min(Math.max(v * t, 0), a),
    fem: (t) => (t >= 0 && t < tEntrada ? -N * B * L * v : 0),
    femMax: N * B * L * v,
  };
}

/** Espira fija de superficie S en un campo perpendicular B(t) dado por tramos rectos: vertices = [[t, B], ...]. */
export function campoPorTramos({ S, N = 1 }, vertices) {
  const tramo = (t) => {
    for (let i = 0; i < vertices.length - 1; i++) {
      if (t >= vertices[i][0] && t <= vertices[i + 1][0] && vertices[i + 1][0] > vertices[i][0]) return i;
    }
    return -1;
  };
  const campo = (t) => {
    const i = tramo(t);
    if (i < 0) return t < vertices[0][0] ? vertices[0][1] : vertices[vertices.length - 1][1];
    const [t1, b1] = vertices[i];
    const [t2, b2] = vertices[i + 1];
    return b1 + ((b2 - b1) * (t - t1)) / (t2 - t1);
  };
  const pendiente = (t) => {
    // En un vértice exacto se toma el tramo que empieza ahí.
    for (let i = 0; i < vertices.length - 1; i++) {
      if (t >= vertices[i][0] && t < vertices[i + 1][0]) return (vertices[i + 1][1] - vertices[i][1]) / (vertices[i + 1][0] - vertices[i][0]);
    }
    return 0;
  };
  const pendientes = vertices.slice(0, -1).map((v, i) => Math.abs((vertices[i + 1][1] - v[1]) / (vertices[i + 1][0] - v[0] || Infinity)));
  return {
    tMax: vertices[vertices.length - 1][0],
    campo,
    flujo: (t) => N * S * campo(t),
    fem: (t) => -N * S * pendiente(t) || 0,
    femMax: N * S * Math.max(0, ...pendientes),
  };
}

/** Bobina de N espiras de superficie S que gira con velocidad angular w en un campo uniforme B (alternador). */
export function espiraGirando({ N = 1, S, B, w }) {
  return {
    tMax: (4 * Math.PI) / w,
    angulo: (t) => w * t,
    flujo: (t) => N * B * S * Math.cos(w * t),
    fem: (t) => N * B * S * w * Math.sin(w * t),
    femMax: N * B * S * w,
  };
}

/** Bobina fija en un campo perpendicular que varía como B0·sen(w·t). */
export function campoSenoidal({ N = 1, S, B0, w }) {
  return {
    tMax: (4 * Math.PI) / w,
    campo: (t) => B0 * Math.sin(w * t),
    flujo: (t) => N * S * B0 * Math.sin(w * t),
    fem: (t) => -N * S * B0 * w * Math.cos(w * t),
    femMax: N * S * B0 * w,
  };
}

/**
 * Sentido de la corriente inducida (ley de Lenz), mirando el dibujo de frente.
 * `variacion`: signo de la variación del flujo en valor absoluto (+ crece, − decrece).
 * `entra`: true si el campo entra en el papel.
 */
export function sentidoCorriente(variacion, entra) {
  if (variacion === 0) return "no hay corriente";
  // Si el flujo crece, el campo inducido se opone al campo; si decrece, lo refuerza.
  const inducidoSale = variacion > 0 ? entra : !entra;
  return inducidoSale ? "antihorario" : "horario";
}
