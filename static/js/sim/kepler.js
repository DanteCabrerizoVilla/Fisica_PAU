// Simulación: órbita elíptica. Muestra la ley de las áreas y la conservación
// del momento angular (r·v·sen φ no cambia a lo largo de la órbita).
// La física está en fisica-orbitas.js; aquí solo van controles y dibujo.

import * as F from "./fisica-orbitas.js";
import {
  barras, botones, bucle, campoCientifico, casilla, crearLienzo, deslizador, duracion,
  estructura, flecha, grupo, lecturas, medida, num, parametrosURL,
} from "./kit.js";

const ANIO = 365.25 * 86400;
const UA = 1.496e11;
const M_SOL = F.ASTROS.sol.M;
const M_TIERRA = F.ASTROS.tierra.M;
const VUELTA_EN_PANTALLA = 14; // segundos que dura una vuelta en el dibujo

const EJEMPLOS = [
  { texto: "Plutón", M: M_SOL, a: F.radioDesdePeriodo(M_SOL, 248 * ANIO), e: 0.244 },
  { texto: "Mercurio", M: M_SOL, a: 5.79e10, e: 0.206 },
  { texto: "Tierra", M: M_SOL, a: UA, e: 0.017 },
  { texto: "Cometa Halley", M: M_SOL, a: 2.67e12, e: 0.967 },
  { texto: "Satélite Molniya", M: M_TIERRA, a: 2.66e7, e: 0.74 },
];
const LONGITUD = [{ texto: "m", factor: 1 }, { texto: "km", factor: 1e3 }, { texto: "UA", factor: UA }];
const MASA = [{ texto: "kg", factor: 1 }];

const COLOR = {
  fondo: "#0e1320",
  estrella: "rgba(255,255,255,0.5)",
  orbita: "rgba(255,255,255,0.55)",
  tramoA: "rgba(255,209,102,0.20)",
  tramoB: "rgba(122,170,255,0.20)",
  barrido: "rgba(255,209,102,0.62)",
  radio: "rgba(243,239,230,0.9)",
  cuerpo: "#ffffff",
  velocidad: "#7ee081",
  angulo: "#ff9f6b",
  texto: "rgba(243,239,230,0.88)",
  ec: "#7ee081",
  ep: "#ff9f6b",
  em: "#ffd166",
};

/** Nombres de los puntos extremos según el astro central. */
function extremos(M) {
  if (Math.abs(M / M_SOL - 1) < 0.05) return ["perihelio", "afelio"];
  if (Math.abs(M / M_TIERRA - 1) < 0.05) return ["perigeo", "apogeo"];
  return ["punto más cercano", "punto más lejano"];
}

export function montar(contenedor) {
  const { marco, estado, panel } = estructura(contenedor);
  marco.style.setProperty("--sim-fondo", COLOR.fondo);
  const lienzo = crearLienzo(marco, {
    aspecto: 0.82,
    descripcion: "Órbita elíptica con el astro en un foco y los tramos que recorre el cuerpo en tiempos iguales",
  });
  const { ctx } = lienzo;

  let semilla = 11;
  const azar = () => ((semilla = (semilla * 16807) % 2147483647) / 2147483647);
  const estrellas = Array.from({ length: 60 }, () => [azar(), azar(), 0.4 + azar() * 0.9]);

  // ---- Estado: por defecto Plutón, como en el modelo de examen ----
  const url = parametrosURL();
  let M = url.M ?? EJEMPLOS[0].M;
  let a = url.a ?? (url.T !== undefined ? F.radioDesdePeriodo(M, url.T) : EJEMPLOS[0].a);
  let e = Math.min(0.97, Math.max(0, url.e ?? EJEMPLOS[0].e));
  let tramos = 8;
  let t = 0;
  let el = null;      // elementos de la órbita
  let sectores = [];  // contorno de cada tramo, en metros respecto al foco

  // ---- Controles ----
  const gOrbita = grupo(panel, "Órbita");
  // Ejemplos: cada botón carga la masa central, el semieje y la excentricidad.
  const cajaEjemplos = document.createElement("div");
  cajaEjemplos.className = "sim__control";
  const filaEjemplos = document.createElement("div");
  filaEjemplos.className = "sim__marcas";
  for (const ej of EJEMPLOS) {
    const b = document.createElement("button");
    b.type = "button";
    b.textContent = ej.texto;
    b.addEventListener("click", () => aplicarEjemplo(ej));
    filaEjemplos.append(b);
  }
  cajaEjemplos.append(filaEjemplos);
  gOrbita.append(cajaEjemplos);
  const cE = deslizador(gOrbita, {
    etiqueta: "Excentricidad, e",
    min: 0, max: 0.97, paso: 0.005, valor: e,
    formato: (v) => num(v, 3),
    alCambiar: (v) => { e = v; recalcular(); },
  });
  const cM = campoCientifico(gOrbita, {
    etiqueta: "Masa del astro central, M", valor: M, unidades: MASA,
    alCambiar: (v) => { M = v; recalcular(); },
  });
  const cA = campoCientifico(gOrbita, {
    etiqueta: "Semieje mayor, a", valor: a, unidades: LONGITUD,
    alCambiar: (v) => { a = v; recalcular(); },
  });
  deslizador(gOrbita, {
    etiqueta: "Tramos de igual duración",
    min: 4, max: 16, paso: 2, valor: tramos,
    formato: (v) => `${v} por vuelta`,
    alCambiar: (v) => { tramos = v; recalcular(); },
  });
  const boton = botones(gOrbita);
  const bPausa = boton("Pausa", () => (animacion.activo ? pausar() : seguir()), { suave: true });

  function aplicarEjemplo(ej) {
    ({ M, a, e } = ej);
    cE.valor = e;
    cM.valor = M;
    cA.valor = a;
    t = 0;
    recalcular();
  }
  const gAhora = grupo(panel, "Ahora mismo");
  const poner = lecturas(gAhora, [
    ["r", "Distancia al astro, r"],
    ["v", "Velocidad, v"],
    ["fi", "Ángulo entre r y v, φ"],
    ["rv", "r · v · sen φ"],
    ["dA", "Área barrida cada segundo"],
  ]);
  const barra = barras(gAhora, [
    ["ec", "Ec", COLOR.ec],
    ["ep", "Ep", COLOR.ep],
    ["em", "Em", COLOR.em],
  ]);

  const gExtremos = grupo(panel, "Puntos extremos");
  const ponerX = lecturas(gExtremos, [
    ["rp", "r más cercano"],
    ["vp", "v más cercano"],
    ["ra", "r más lejano"],
    ["va", "v más lejano"],
    ["prod", "r · v en los dos puntos"],
    ["T", "Periodo"],
  ]);

  const gAreas = grupo(panel, "Áreas en tiempos iguales");
  const ponerA = lecturas(gAreas, [
    ["dt", "Duración de cada tramo"],
    ["cerca", "Área del tramo más cercano"],
    ["lejos", "Área del tramo más lejano"],
  ]);
  const nota = document.createElement("p");
  nota.className = "sim__nota";
  nota.textContent = "Las áreas están medidas sobre el dibujo, sumando triángulos, no calculadas con la ley.";
  gAreas.append(nota);

  // Cambio de órbita: impulso en un extremo para pasar a la órbita circular de ese radio.
  const gCambio = grupo(panel, "Cambio a órbita circular");
  let masaCuerpo = url.m ?? 1000;
  let verCirculares = url.cambio === 1;
  campoCientifico(gCambio, {
    etiqueta: "Masa del cuerpo, m", valor: masaCuerpo, unidades: MASA,
    alCambiar: (v) => { masaCuerpo = v; recalcular(); },
  });
  const ponerC = lecturas(gCambio, [
    ["vcL", "v circular en el punto más lejano"],
    ["dvL", "Cambio de velocidad allí"],
    ["EL", "Energía que hay que aportar"],
    ["vcC", "v circular en el punto más cercano"],
    ["dvC", "Cambio de velocidad allí"],
    ["EC", "Energía que hay que aportar"],
  ]);
  casilla(gCambio, {
    etiqueta: "Dibujar las dos órbitas circulares", valor: verCirculares,
    alCambiar: (v) => { verCirculares = v; dibujar(); },
  });
  const notaCambio = document.createElement("p");
  notaCambio.className = "sim__nota";
  notaCambio.textContent = "Un impulso breve cambia la velocidad pero no la posición: el punto del impulso pertenece a la órbita antigua y a la nueva.";
  gCambio.append(notaCambio);

  // ---- Cálculo ----
  const valido = () => M > 0 && a > 0 && e >= 0 && e < 1;

  function recalcular() {
    if (!valido()) {
      el = null;
      estado.textContent = "Faltan datos o hay alguno que no es positivo.";
      dibujar();
      return;
    }
    const orbita = { M, a, e };
    el = F.elipse(orbita);
    const dt = el.T / tramos;
    sectores = Array.from({ length: tramos }, (_, i) => {
      const puntos = [];
      for (let j = 0; j <= 28; j++) {
        const s = F.estadoEliptico(orbita, (i + j / 28) * dt);
        puntos.push([s.x, s.y]);
      }
      return puntos;
    });

    const [cerca, lejos] = extremos(M);
    estado.textContent = e < 0.005
      ? "Órbita circular: la velocidad no cambia"
      : `Órbita elíptica: más rápido cerca del ${cerca}`;
    ponerX("rp", medida(el.rp, "m"));
    ponerX("vp", medida(el.vp, "m/s"));
    ponerX("ra", medida(el.ra, "m"));
    ponerX("va", medida(el.va, "m/s"));
    ponerX("prod", medida(el.rp * el.vp, "m²/s"));
    ponerX("T", `${medida(el.T, "s")} (${duracion(el.T)})`);
    ponerA("dt", duracion(dt));
    // Tramo que empieza en el punto más cercano y tramo que empieza en el más lejano.
    ponerA("cerca", medida(F.areaBarrida(orbita, 0, dt), "m²"));
    ponerA("lejos", medida(F.areaBarrida(orbita, el.T / 2, el.T / 2 + dt), "m²"));
    const signo = (x, unidad) => `${x >= 0 ? "+" : "−"}${medida(Math.abs(x), unidad)}`;
    for (const [sufijo, donde] of [["L", "lejano"], ["C", "cercano"]]) {
      const c = F.cambioACircular({ M, a, e, m: masaCuerpo }, donde);
      ponerC(`vc${sufijo}`, medida(c.vCircular, "m/s"));
      ponerC(`dv${sufijo}`, e < 1e-9 ? "ninguno: ya es circular" : `${signo(c.deltaV, "m/s")} (${c.deltaV > 0 ? "acelerar" : "frenar"})`);
      ponerC(`E${sufijo}`, e < 1e-9 || !(masaCuerpo > 0) ? "—" : signo(c.energia, "J"));
    }
    gExtremos.querySelector("h2").textContent = `${cerca[0].toUpperCase()}${cerca.slice(1)} y ${lejos}`;
    actualizarAhora();
    dibujar();
  }

  function actualizarAhora() {
    if (!el) return;
    const s = F.estadoEliptico({ M, a, e }, t);
    poner("r", medida(s.r, "m"));
    poner("v", medida(s.v, "m/s"));
    poner("fi", `${num((Math.acos(Math.max(-1, Math.min(1, (s.x * s.vx + s.y * s.vy) / (s.r * s.v)))) * 180) / Math.PI, 1)}°`);
    poner("rv", medida(s.r * s.v * s.senFi, "m²/s"));
    poner("dA", medida(0.5 * s.r * s.v * s.senFi, "m²/s"));
    // Energías por kilogramo, relativas a la potencial en el punto más cercano.
    const ref = (F.G * M) / el.rp;
    const ec = 0.5 * s.v * s.v;
    const ep = (-F.G * M) / s.r;
    barra("ec", ec / ref);
    barra("ep", ep / ref);
    barra("em", (ec + ep) / ref);
  }

  // ---- Dibujo ----
  function dibujar() {
    const { ancho, alto } = lienzo;
    ctx.fillStyle = COLOR.fondo;
    ctx.fillRect(0, 0, ancho, alto);
    ctx.fillStyle = COLOR.estrella;
    for (const [x, y, tam] of estrellas) ctx.fillRect(x * ancho, y * alto, tam, tam);
    if (!el) return;

    const margenX = 30;
    const arriba = 44;
    const abajo = 70;
    const cy = arriba + (alto - arriba - abajo) / 2;
    // El astro está en el foco, desplazado a·e a la derecha del centro de la elipse.
    // Con las órbitas circulares a la vista, el encuadre se centra en el astro.
    const esc = verCirculares
      ? Math.min(ancho - 2 * margenX, alto - arriba - abajo) / (2 * el.ra)
      : Math.min((ancho - 2 * margenX) / (2 * el.a), (alto - arriba - abajo) / (2 * el.b));
    const fx = verCirculares ? ancho / 2 : ancho / 2 + el.c * esc;
    const cx = fx - el.c * esc;
    const X = (x) => fx + x * esc;
    const Y = (y) => cy - y * esc;

    if (verCirculares && e >= 0.005) {
      ctx.setLineDash([5, 5]);
      ctx.lineWidth = 1.5;
      for (const [radio, color] of [[el.ra, "rgba(122,170,255,0.9)"], [el.rp, "rgba(255,159,107,0.9)"]]) {
        ctx.beginPath();
        ctx.arc(fx, cy, radio * esc, 0, 2 * Math.PI);
        ctx.strokeStyle = color;
        ctx.stroke();
      }
      ctx.setLineDash([]);
    }

    // Tramos de igual duración
    sectores.forEach((puntos, i) => {
      ctx.beginPath();
      ctx.moveTo(fx, cy);
      for (const [x, y] of puntos) ctx.lineTo(X(x), Y(y));
      ctx.closePath();
      ctx.fillStyle = i % 2 ? COLOR.tramoB : COLOR.tramoA;
      ctx.fill();
    });

    // Parte ya barrida del tramo actual
    const dt = el.T / tramos;
    const tVuelta = ((t % el.T) + el.T) % el.T;
    const inicio = Math.floor(tVuelta / dt) * dt;
    ctx.beginPath();
    ctx.moveTo(fx, cy);
    const pasos = Math.max(2, Math.ceil((28 * (tVuelta - inicio)) / dt));
    for (let j = 0; j <= pasos; j++) {
      const s = F.estadoEliptico({ M, a, e }, inicio + ((tVuelta - inicio) * j) / pasos);
      ctx.lineTo(X(s.x), Y(s.y));
    }
    ctx.closePath();
    ctx.fillStyle = COLOR.barrido;
    ctx.fill();

    // Órbita
    ctx.beginPath();
    ctx.ellipse(cx, cy, el.a * esc, el.b * esc, 0, 0, 2 * Math.PI);
    ctx.lineWidth = 1.5;
    ctx.strokeStyle = COLOR.orbita;
    ctx.stroke();

    // Astro en el foco
    const esSol = M > 1e28;
    const brillo = ctx.createRadialGradient(fx, cy, 1, fx, cy, 9);
    brillo.addColorStop(0, esSol ? "#fff3c4" : "#9cc4ff");
    brillo.addColorStop(1, esSol ? "#f5a524" : "#3a7bd5");
    ctx.beginPath();
    ctx.arc(fx, cy, 8, 0, 2 * Math.PI);
    ctx.fillStyle = brillo;
    ctx.fill();

    // Radio vector, velocidad y ángulo entre ambos
    const s = F.estadoEliptico({ M, a, e }, t);
    const sx = X(s.x);
    const sy = Y(s.y);
    ctx.beginPath();
    ctx.moveTo(fx, cy);
    ctx.lineTo(sx, sy);
    ctx.lineWidth = 1.5;
    ctx.strokeStyle = COLOR.radio;
    ctx.stroke();

    const angR = Math.atan2(-(s.y), s.x);      // en pantalla, y hacia abajo
    const angV = Math.atan2(-s.vy, s.vx);
    ctx.beginPath();
    ctx.moveTo(sx, sy);
    ctx.lineTo(sx + Math.cos(angR) * 26, sy + Math.sin(angR) * 26);
    ctx.setLineDash([3, 4]);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.beginPath();
    ctx.arc(sx, sy, 15, angV, angR, false);
    ctx.strokeStyle = COLOR.angulo;
    ctx.lineWidth = 2;
    ctx.stroke();

    const largo = Math.max(12, (58 * s.v) / el.vp);
    flecha(ctx, sx, sy, Math.cos(angV) * largo, Math.sin(angV) * largo, COLOR.velocidad);
    ctx.beginPath();
    ctx.arc(sx, sy, 5, 0, 2 * Math.PI);
    ctx.fillStyle = COLOR.cuerpo;
    ctx.fill();

    // Rótulos de los puntos extremos
    const [cerca, lejos] = extremos(M);
    ctx.font = "600 12px system-ui, sans-serif";
    ctx.fillStyle = COLOR.texto;
    ctx.textBaseline = "middle";
    if (e >= 0.005 && !verCirculares) {
      const yRotulo = cy + el.b * esc + 14;
      ctx.textAlign = "right";
      ctx.fillText(cerca, ancho - 10, yRotulo);
      ctx.textAlign = "left";
      ctx.fillText(lejos, 10, yRotulo);
    }

    // Leyenda
    ctx.textAlign = "left";
    const filas = [
      [COLOR.velocidad, "velocidad"],
      [COLOR.angulo, "ángulo φ entre r y v"],
    ];
    filas.forEach(([color, texto], i) => {
      const y = alto - 14 - (filas.length - 1 - i) * 18;
      ctx.fillStyle = color;
      ctx.fillRect(12, y - 1.5, 14, 3);
      ctx.fillStyle = COLOR.texto;
      ctx.fillText(texto, 32, y);
    });
    ctx.textAlign = "right";
    ctx.fillStyle = COLOR.texto;
    ctx.fillText(verCirculares ? "a trazos: órbitas circulares" : "cada franja: mismo tiempo", ancho - 12, alto - 14);
  }
  lienzo.alRedimensionar = () => dibujar();

  // ---- Animación ----
  const animacion = bucle((dt) => {
    if (el) {
      t = (t + (dt * el.T) / VUELTA_EN_PANTALLA) % el.T;
      actualizarAhora();
    }
    dibujar();
  });
  function pausar() { animacion.parar(); bPausa.textContent = "Seguir"; }
  function seguir() { animacion.arrancar(); bPausa.textContent = "Pausa"; }

  recalcular();
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) pausar();
  else seguir();

  // Acceso para pruebas automáticas.
  return {
    get elementos() { return el; },
    get tiempo() { return t; },
    set tiempo(v) { t = v; actualizarAhora(); dibujar(); },
    pausar, seguir,
  };
}
