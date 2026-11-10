// Simulación: satélite en órbita circular. Funciona como comprobador de
// problemas: se escriben los datos del enunciado y da todos los resultados.
// La física está en fisica-orbitas.js; aquí solo van controles y dibujo.

import * as F from "./fisica-orbitas.js";
import {
  barras, botones, bucle, campoCientifico, crearLienzo, duracion, estructura,
  flecha, grupo, lecturas, medida, parametrosURL, selector,
} from "./kit.js";

const LONGITUD = [{ texto: "m", factor: 1 }, { texto: "km", factor: 1e3 }];
const TIEMPO = [{ texto: "s", factor: 1 }, { texto: "h", factor: 3600 }, { texto: "días", factor: 86400 }];
const MASA = [{ texto: "kg", factor: 1 }];
const VUELTA_EN_PANTALLA = 10; // segundos que tarda el dibujo en dar una vuelta

const COLOR = {
  fondo: "#0e1320",
  estrella: "rgba(255,255,255,0.55)",
  astro: "#3a7bd5",
  astroBorde: "#9cc4ff",
  orbita: "rgba(255,255,255,0.45)",
  radio: "rgba(243,239,230,0.75)",
  altura: "#ffd166",
  satelite: "#ffffff",
  velocidad: "#7ee081",
  fuerza: "#ff9f6b",
  texto: "rgba(243,239,230,0.88)",
  ec: "#7ee081",
  ep: "#ff9f6b",
  em: "#ffd166",
};

export function montar(contenedor) {
  const { marco, estado, panel } = estructura(contenedor);
  marco.style.setProperty("--sim-fondo", COLOR.fondo);
  const lienzo = crearLienzo(marco, {
    aspecto: 1,
    descripcion: "Vista desde arriba del astro y de la órbita circular del satélite",
  });
  const { ctx } = lienzo;

  let semilla = 7;
  const azar = () => ((semilla = (semilla * 16807) % 2147483647) / 2147483647);
  const estrellas = Array.from({ length: 70 }, () => [azar(), azar(), 0.4 + azar() * 0.9]);

  // ---- Estado: por defecto, el problema de muestra (o lo que diga la URL) ----
  const url = parametrosURL();
  let M = url.M ?? F.ASTROS.tierra.M;
  let R = url.R ?? (url.M === undefined ? F.ASTROS.tierra.R : 0);
  let m = url.m ?? 1200;
  let modo = url.T !== undefined ? "T" : url.r !== undefined ? "r" : "h";
  const dato = { h: url.h ?? 6e5, r: url.r ?? 6.97e6, T: url.T ?? 86164 };
  let angulo = 0.6;
  let orb = null;
  let problema = "";

  const astroActual = () =>
    Object.keys(F.ASTROS).find((k) => F.ASTROS[k].M === M && F.ASTROS[k].R === R) ?? "otro";

  // ---- Controles ----
  const gDatos = grupo(panel, "Datos del problema");
  const sAstro = selector(gDatos, {
    etiqueta: "Astro central",
    opciones: [
      ...Object.entries(F.ASTROS).map(([valor, a]) => ({ valor, texto: a.nombre })),
      { valor: "otro", texto: "Otro (escribe su masa y su radio)" },
    ],
    valor: astroActual(),
    alCambiar: (clave) => {
      if (clave === "otro") return;
      ({ M, R } = F.ASTROS[clave]);
      cM.valor = M;
      cR.valor = R;
      recalcular();
    },
  });
  const cM = campoCientifico(gDatos, {
    etiqueta: "Masa del astro, M", valor: M, unidades: MASA,
    alCambiar: (v) => { M = v; sAstro.valor = astroActual(); recalcular(); },
  });
  const cR = campoCientifico(gDatos, {
    etiqueta: "Radio del astro, R", valor: R, unidades: LONGITUD,
    alCambiar: (v) => { R = v; sAstro.valor = astroActual(); recalcular(); },
  });
  selector(gDatos, {
    etiqueta: "Qué dato da el enunciado",
    opciones: [
      { valor: "h", texto: "La altura sobre la superficie" },
      { valor: "r", texto: "El radio de la órbita" },
      { valor: "T", texto: "El periodo" },
    ],
    valor: modo,
    alCambiar: (v) => { modo = v; mostrarCampo(); recalcular(); },
  });
  const campos = {
    h: campoCientifico(gDatos, {
      etiqueta: "Altura, h", valor: dato.h, unidades: LONGITUD,
      alCambiar: (v) => { dato.h = v; recalcular(); },
    }),
    r: campoCientifico(gDatos, {
      etiqueta: "Radio de la órbita, r", valor: dato.r, unidades: LONGITUD,
      alCambiar: (v) => { dato.r = v; recalcular(); },
    }),
    T: campoCientifico(gDatos, {
      etiqueta: "Periodo, T", valor: dato.T, unidades: TIEMPO,
      alCambiar: (v) => { dato.T = v; recalcular(); },
    }),
  };
  // Sin datos en la URL, la altura se muestra en kilómetros, como en el enunciado.
  if (url.h === undefined) campos.h.ponerUnidad(1, dato.h);
  const mostrarCampo = () => {
    for (const [clave, campo] of Object.entries(campos)) campo.caja.hidden = clave !== modo;
  };
  mostrarCampo();
  campoCientifico(gDatos, {
    etiqueta: "Masa del satélite, m", valor: m, unidades: MASA,
    alCambiar: (v) => { m = v; recalcular(); },
  });
  const boton = botones(gDatos);
  const bPausa = boton("Pausa", () => (animacion.activo ? pausar() : seguir()), { suave: true });

  const gOrbita = grupo(panel, "En la órbita");
  const poner = lecturas(gOrbita, [
    ["r", "Radio de la órbita, r"],
    ["h", "Altura sobre la superficie"],
    ["v", "Velocidad orbital"],
    ["T", "Periodo"],
    ["g", "Gravedad a esa distancia"],
  ]);

  const gEnergia = grupo(panel, "Energía del satélite");
  const ponerE = lecturas(gEnergia, [
    ["ec", "Cinética"],
    ["ep", "Potencial"],
    ["em", "Mecánica"],
  ]);
  const barra = barras(gEnergia, [
    ["ec", "Ec", COLOR.ec],
    ["ep", "Ep", COLOR.ep],
    ["em", "Em", COLOR.em],
  ]);

  const gEscape = grupo(panel, "Escape y lanzamiento");
  const ponerX = lecturas(gEscape, [
    ["escapar", "Energía para escapar desde la órbita"],
    ["g0", "Gravedad en la superficie"],
    ["ve", "Velocidad de escape desde la superficie"],
    ["subir", "Energía para ponerlo en órbita desde el suelo"],
  ]);
  const nota = document.createElement("p");
  nota.className = "sim__nota";
  nota.textContent = "La energía de puesta en órbita parte del reposo en la superficie y no cuenta la rotación del astro.";
  gEscape.append(nota);

  // ---- Cálculo ----
  function recalcular() {
    let r = NaN;
    if (modo === "h") r = R + dato.h;
    else if (modo === "r") r = dato.r;
    else r = F.radioDesdePeriodo(M, dato.T);

    problema = "";
    if (!(M > 0) || !(m > 0) || !(r > 0)) problema = "Faltan datos o hay alguno que no es positivo.";
    else if (modo === "h" && !(R > 0)) problema = "Para usar la altura hace falta el radio del astro.";
    else if (R > 0 && r < R) problema = "Esa órbita quedaría por debajo de la superficie. Revisa los datos.";

    orb = problema ? null : F.orbitaCircular({ M, r, m });
    actualizarLecturas();
    dibujar();
  }

  function actualizarLecturas() {
    if (!orb) {
      estado.textContent = problema;
      for (const c of ["r", "h", "v", "T", "g"]) poner(c, "—");
      for (const c of ["ec", "ep", "em"]) { ponerE(c, "—"); barra(c, 0); }
      for (const c of ["escapar", "g0", "ve", "subir"]) ponerX(c, "—");
      return;
    }
    estado.textContent = `Órbita circular · una vuelta cada ${duracion(orb.T)}`;
    poner("r", medida(orb.r, "m"));
    poner("h", R > 0 ? medida(orb.r - R, "m") : "—");
    poner("v", medida(orb.v, "m/s"));
    poner("T", `${medida(orb.T, "s")}`);
    poner("g", medida(orb.g, "m/s²"));
    ponerE("ec", medida(orb.Ec, "J"));
    ponerE("ep", medida(orb.Ep, "J"));
    ponerE("em", medida(orb.Em, "J"));
    barra("ec", orb.Ec / -orb.Ep);
    barra("ep", -1);
    barra("em", orb.Em / -orb.Ep);
    ponerX("escapar", medida(orb.energiaEscape, "J"));
    if (R > 0) {
      const sup = F.superficie({ M, R, m });
      ponerX("g0", medida(sup.g, "m/s²"));
      ponerX("ve", medida(sup.vEscape, "m/s"));
      ponerX("subir", medida(F.energiaPuestaEnOrbita({ M, R, r: orb.r, m }), "J"));
    } else {
      for (const c of ["g0", "ve", "subir"]) ponerX(c, "—");
    }
  }

  // ---- Dibujo ----
  function dibujar() {
    const { ancho, alto } = lienzo;
    const cx = ancho / 2;
    const cy = alto / 2 + 6;
    ctx.fillStyle = COLOR.fondo;
    ctx.fillRect(0, 0, ancho, alto);
    ctx.fillStyle = COLOR.estrella;
    for (const [x, y, t] of estrellas) ctx.fillRect(x * ancho, y * alto, t, t);
    if (!orb) return;

    const rPx = Math.min(ancho, alto) / 2 - 62;
    const esc = rPx / orb.r;
    const astroPx = Math.max(R * esc, 4);

    // Órbita
    ctx.beginPath();
    ctx.arc(cx, cy, rPx, 0, 2 * Math.PI);
    ctx.setLineDash([5, 6]);
    ctx.lineWidth = 1.5;
    ctx.strokeStyle = COLOR.orbita;
    ctx.stroke();
    ctx.setLineDash([]);

    // Astro, a escala con la órbita (con un tamaño mínimo para que se vea)
    const degradado = ctx.createRadialGradient(cx - astroPx * 0.35, cy - astroPx * 0.35, astroPx * 0.1, cx, cy, astroPx);
    degradado.addColorStop(0, "#6aa9f4");
    degradado.addColorStop(1, COLOR.astro);
    ctx.beginPath();
    ctx.arc(cx, cy, astroPx, 0, 2 * Math.PI);
    ctx.fillStyle = degradado;
    ctx.fill();
    ctx.lineWidth = 1;
    ctx.strokeStyle = COLOR.astroBorde;
    ctx.stroke();

    // Radio: tramo dentro del astro (R) y tramo de altura (h)
    const ux = Math.cos(angulo);
    const uy = -Math.sin(angulo);
    const sx = cx + ux * rPx;
    const sy = cy + uy * rPx;
    ctx.lineWidth = 1.5;
    ctx.strokeStyle = COLOR.radio;
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(cx + ux * Math.min(astroPx, rPx), cy + uy * Math.min(astroPx, rPx));
    ctx.stroke();
    if (rPx > astroPx) {
      ctx.strokeStyle = R > 0 ? COLOR.altura : COLOR.radio;
      ctx.beginPath();
      ctx.moveTo(cx + ux * astroPx, cy + uy * astroPx);
      ctx.lineTo(sx, sy);
      ctx.stroke();
    }

    // Vectores: la velocidad es tangente y la fuerza apunta al centro
    flecha(ctx, sx, sy, -Math.sin(angulo) * 52, -Math.cos(angulo) * 52, COLOR.velocidad);
    flecha(ctx, sx, sy, -ux * 38, -uy * 38, COLOR.fuerza);
    ctx.beginPath();
    ctx.arc(sx, sy, 5, 0, 2 * Math.PI);
    ctx.fillStyle = COLOR.satelite;
    ctx.fill();

    // Leyenda
    ctx.font = "600 12px system-ui, sans-serif";
    ctx.textBaseline = "middle";
    ctx.textAlign = "left";
    const filas = [[COLOR.velocidad, "velocidad"], [COLOR.fuerza, "fuerza gravitatoria"]];
    if (R > 0) filas.push([COLOR.altura, "altura h (r = R + h)"]);
    filas.forEach(([color, texto], i) => {
      const y = alto - 14 - (filas.length - 1 - i) * 18;
      ctx.fillStyle = color;
      ctx.fillRect(12, y - 1.5, 14, 3);
      ctx.fillStyle = COLOR.texto;
      ctx.fillText(texto, 32, y);
    });
  }
  lienzo.alRedimensionar = () => { if (orb !== undefined) dibujar(); };

  // ---- Animación ----
  const animacion = bucle((dt) => {
    angulo = (angulo + (dt * 2 * Math.PI) / VUELTA_EN_PANTALLA) % (2 * Math.PI);
    dibujar();
  });
  function pausar() { animacion.parar(); bPausa.textContent = "Seguir"; }
  function seguir() { animacion.arrancar(); bPausa.textContent = "Pausa"; }

  recalcular();
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) pausar();
  else seguir();

  // Acceso para pruebas automáticas.
  return { get orbita() { return orb; }, get problema() { return problema; }, pausar, seguir };
}
