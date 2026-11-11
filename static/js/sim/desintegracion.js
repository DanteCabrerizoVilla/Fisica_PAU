// Simulación: desintegración radiactiva. Se introduce el dato de ritmo que dé
// el enunciado (periodo, vida media o constante) y la muestra (masa, actividad
// o núcleos), y se sigue su evolución. La física está en fisica-moderna.js.

import * as F from "./fisica-moderna.js";
import {
  TINTA, campoCientifico, campoNumero, crearLienzo, deslizador, duracion, ejes, estructura,
  grupo, lecturas, medida, nota, num, parametroTexto, parametrosURL, punto, rotulo, selector, trazar,
} from "./kit.js";

const TIEMPO = [
  { texto: "s", factor: 1 }, { texto: "min", factor: 60 }, { texto: "h", factor: 3600 },
  { texto: "días", factor: 86400 }, { texto: "años", factor: 365 * 86400 },
];
const INVERSA = TIEMPO.map((u) => ({ texto: `${u.texto}⁻¹`, factor: 1 / u.factor }));
const NUCLEOS = 240;

export function montar(contenedor) {
  const { marco, estado, panel } = estructura(contenedor);
  const lienzo = crearLienzo(marco, { aspecto: 1.05, descripcion: "Núcleos de la muestra, apagándose al desintegrarse, y curva exponencial con los periodos de semidesintegración marcados" });
  const { ctx } = lienzo;

  // Instante (en periodos) en que se desintegra cada núcleo del dibujo: reparto exponencial fijo.
  let semilla = 12345;
  const azar = () => ((semilla = (semilla * 16807) % 2147483647) / 2147483647);
  const vidas = Array.from({ length: NUCLEOS }, () => -Math.log2(1 - azar()));

  // ---- Estado: por defecto, cobalto-60 del modelo de 2027 ----
  const url = parametrosURL();
  const ritmo = { tipo: ["T", "tau", "lambda"].includes(parametroTexto("dato")) ? parametroTexto("dato") : "T", valor: url.ritmo ?? 1925.2 * 86400 };
  const mues = { tipo: ["masa", "actividad", "nucleos"].includes(parametroTexto("muestra")) ? parametroTexto("muestra") : "actividad", valor: url.valor ?? 2.64e9, masaMolar: url.M ?? 59.94 };
  let t = url.t ?? 365 * 86400;
  let objetivo = url.objetivo ?? 1e9;
  let lambda = F.constante(ritmo);
  let m = F.muestra(mues, lambda);

  // ---- Controles ----
  const gRitmo = grupo(panel, "Ritmo de desintegración");
  selector(gRitmo, {
    etiqueta: "Qué dato da el enunciado",
    opciones: [
      { valor: "T", texto: "Periodo de semidesintegración, T½" },
      { valor: "tau", texto: "Vida media, τ" },
      { valor: "lambda", texto: "Constante de desintegración, λ" },
    ],
    valor: ritmo.tipo,
    alCambiar: (v) => {
      // Se conserva el isótopo: el campo pasa a mostrar la magnitud elegida.
      const T = Math.LN2 / lambda;
      ritmo.tipo = v;
      ritmo.valor = v === "T" ? T : v === "tau" ? 1 / lambda : lambda;
      mostrar();
      (v === "lambda" ? cLambda : cTiempo).valor = ritmo.valor;
      recalcular();
    },
  });
  const cTiempo = campoCientifico(gRitmo, { etiqueta: "Valor", valor: ritmo.tipo === "lambda" ? 1 : ritmo.valor, unidades: TIEMPO, alCambiar: (v) => { ritmo.valor = v; recalcular(); } });
  const cLambda = campoCientifico(gRitmo, { etiqueta: "Valor", valor: ritmo.tipo === "lambda" ? ritmo.valor : 1, unidades: INVERSA, alCambiar: (v) => { ritmo.valor = v; recalcular(); } });
  if (ritmo.tipo !== "lambda" && url.ritmo === undefined) cTiempo.ponerUnidad(3, ritmo.valor);

  const gMuestra = grupo(panel, "Muestra inicial");
  selector(gMuestra, {
    etiqueta: "Qué se conoce de la muestra",
    opciones: [
      { valor: "actividad", texto: "Su actividad (Bq)" },
      { valor: "masa", texto: "Su masa (g)" },
      { valor: "nucleos", texto: "Su número de núcleos" },
    ],
    valor: mues.tipo,
    alCambiar: (v) => {
      mues.tipo = v;
      mues.valor = v === "masa" ? m.m0 : v === "actividad" ? m.A0 : m.N0;
      cMuestra.valor = mues.valor;
      recalcular();
    },
  });
  const cMuestra = campoCientifico(gMuestra, { etiqueta: "Valor", valor: mues.valor, unidades: [{ texto: "", factor: 1 }], alCambiar: (v) => { mues.valor = v; recalcular(); } });
  campoNumero(gMuestra, { etiqueta: "Masa molar del isótopo", valor: mues.masaMolar, unidad: "g/mol", min: 0, alCambiar: (v) => { mues.masaMolar = v; recalcular(); } });

  const gTiempo = grupo(panel, "Tiempo transcurrido");
  const dT = deslizador(gTiempo, {
    etiqueta: "t, en periodos", min: 0, max: 6, paso: 0.05, valor: Math.min(6, (t * lambda) / Math.LN2),
    formato: (v) => `${num(v, 2)} T½`,
    alCambiar: (v) => { t = (v * Math.LN2) / lambda; cT.valor = t; actualizar(); },
  });
  const cT = campoCientifico(gTiempo, { etiqueta: "…o escribe el tiempo", valor: t, unidades: TIEMPO, alCambiar: (v) => { t = v; dT.valor = Math.min(6, (t * lambda) / Math.LN2); actualizar(); } });
  if (url.t === undefined) cT.ponerUnidad(3, t);

  const gIni = grupo(panel, "El isótopo y la muestra");
  const ponerI = lecturas(gIni, [
    ["lambda", "Constante, λ"],
    ["T", "Periodo de semidesintegración"],
    ["tau", "Vida media, τ"],
    ["N0", "Núcleos iniciales, N₀"],
    ["A0", "Actividad inicial, A₀"],
    ["m0", "Masa inicial"],
  ]);
  const gAhora = grupo(panel, "Al cabo de ese tiempo");
  const ponerT = lecturas(gAhora, [
    ["fr", "Queda"],
    ["N", "Núcleos"],
    ["A", "Actividad"],
    ["m", "Masa"],
    ["des", "Núcleos desintegrados"],
  ]);
  const gObj = grupo(panel, "¿Cuánto tarda en bajar a…?");
  campoCientifico(gObj, { etiqueta: "Actividad objetivo", valor: objetivo, unidades: [{ texto: "Bq", factor: 1 }], alCambiar: (v) => { objetivo = v; actualizar(); } });
  const ponerO = lecturas(gObj, [["t", "Tiempo necesario"]]);
  nota(gObj, "La masa y el número de núcleos se reducen en la misma proporción que la actividad.");

  function mostrar() {
    cTiempo.caja.hidden = ritmo.tipo === "lambda";
    cLambda.caja.hidden = ritmo.tipo !== "lambda";
  }

  // ---- Cálculo ----
  const unidadMuestra = () => ({ masa: "g", actividad: "Bq", nucleos: "núcleos" })[mues.tipo];
  function recalcular() {
    lambda = F.constante(ritmo);
    if (!(lambda > 0) || !(mues.valor > 0) || !(mues.masaMolar > 0)) {
      estado.textContent = "Faltan datos o alguno no es positivo.";
      return;
    }
    m = F.muestra(mues, lambda);
    cMuestra.caja.querySelector(".sim__unidad").textContent = unidadMuestra();
    const T = Math.LN2 / lambda;
    ponerI("lambda", `${medida(lambda, "s⁻¹")}<br>${medida(lambda * 86400, "días⁻¹")}`);
    ponerI("T", `${medida(T, "s")} (${duracion(T)})`);
    ponerI("tau", `${medida(1 / lambda, "s")} (${duracion(1 / lambda)})`);
    ponerI("N0", medida(m.N0, ""));
    ponerI("A0", medida(m.A0, "Bq"));
    ponerI("m0", medida(m.m0, "g"));
    dT.valor = Math.min(6, (t * lambda) / Math.LN2);
    actualizar();
  }

  function actualizar() {
    if (!(lambda > 0)) return;
    const fr = F.fraccionRestante(lambda, t);
    ponerT("fr", `${num(fr * 100, fr < 0.1 ? 2 : 1)} %`);
    ponerT("N", medida(m.N0 * fr, ""));
    ponerT("A", medida(m.A0 * fr, "Bq"));
    ponerT("m", medida(m.m0 * fr, "g"));
    ponerT("des", medida(m.N0 * (1 - fr), ""));
    const tObj = objetivo > 0 && objetivo < m.A0 ? F.tiempoHastaFraccion(lambda, objetivo / m.A0) : NaN;
    ponerO("t", Number.isFinite(tObj) ? `${medida(tObj, "s")} (${duracion(tObj)})` : "La actividad inicial ya es menor");
    estado.innerHTML = `Tras ${duracion(t)} queda el ${num(fr * 100, 1)} % de la muestra`;
    dibujar();
  }

  // ---- Dibujo ----
  function dibujar() {
    const { ancho, alto } = lienzo;
    ctx.fillStyle = TINTA.fondo;
    ctx.fillRect(0, 0, ancho, alto);
    if (!(lambda > 0)) return;
    const periodos = (t * lambda) / Math.LN2;

    // Núcleos: los desintegrados se apagan.
    const columnas = 24;
    const filas = NUCLEOS / columnas;
    const paso = Math.min((ancho - 36) / columnas, 15);
    const x0 = (ancho - paso * (columnas - 1)) / 2;
    const y0 = 50;
    vidas.forEach((vida, i) => {
      const vivo = vida > periodos;
      punto(ctx, x0 + (i % columnas) * paso, y0 + Math.floor(i / columnas) * paso, vivo ? TINTA.a : "rgba(255,255,255,0.13)", Math.max(2.5, paso * 0.3));
    });
    const yLeyenda = y0 + filas * paso + 4;
    rotulo(ctx, "● sin desintegrar", x0 - 4, yLeyenda, { color: TINTA.a, tam: 11 });
    rotulo(ctx, "● desintegrado", ancho - x0 + 4, yLeyenda, { color: TINTA.suave, tam: 11, alinear: "right" });

    // Curva exponencial
    const g = { x: 44, y: yLeyenda + 40, ancho: ancho - 58, alto: alto - (yLeyenda + 40) - 40 };
    const xMax = Math.max(6, Math.ceil(periodos));
    const a = ejes(ctx, { ...g, xr: [0, xMax], yr: [0, 100], xlab: "tiempo (en periodos T½)", ylab: "queda (%)", nx: xMax });
    const curva = [];
    for (let i = 0; i <= 200; i++) {
      const p = (xMax * i) / 200;
      curva.push([a.X(p), a.Y(100 * 0.5 ** p)]);
    }
    trazar(ctx, curva, TINTA.a, { recorte: g });
    for (let k = 1; k <= 4; k++) {
      const yy = 100 * 0.5 ** k;
      trazar(ctx, [[a.X(0), a.Y(yy)], [a.X(k), a.Y(yy)], [a.X(k), a.Y(0)]], TINTA.suave, { grosor: 1, discontinua: true });
      rotulo(ctx, `1/${2 ** k}`, a.X(k) + 5, a.Y(yy) - 8, { color: TINTA.suave, tam: 11 });
    }
    const fr = 100 * 0.5 ** periodos;
    if (periodos <= xMax) {
      punto(ctx, a.X(periodos), a.Y(fr), TINTA.b, 5.5);
      rotulo(ctx, `${num(fr, 1)} %`, a.X(periodos) + 9, a.Y(fr) - 9, { color: TINTA.b, negrita: true });
    }
  }
  lienzo.alRedimensionar = () => dibujar();

  mostrar();
  recalcular();
  return { get lambda() { return lambda; }, get muestra() { return m; } };
}
