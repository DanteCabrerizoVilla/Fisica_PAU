// Simulación: efecto fotoeléctrico. Metal, longitud de onda e intensidad de la
// luz; energía de los electrones, potencial de frenado y las dos gráficas que
// aparecen en los exámenes. La física está en fisica-moderna.js.

import * as F from "./fisica-moderna.js";
import {
  TINTA, bucle, campoNumero, crearLienzo, deslizador, ejes, estructura, grupo, lecturas,
  medida, nota, num, parametrosURL, punto, rotulo, selector, trazar,
} from "./kit.js";

const METALES = [
  { nombre: "Cesio", W: 2.14 }, { nombre: "Potasio", W: 2.29 }, { nombre: "Sodio", W: 2.28 },
  { nombre: "Cinc", W: 4.31 }, { nombre: "Cobre", W: 4.7 }, { nombre: "Plata", W: 4.73 },
  { nombre: "Cobalto", W: 5.0 },
];

/** Color aproximado de la luz según su longitud de onda en nm. */
function colorLuz(nm) {
  if (nm < 380) return "#b48cff";       // ultravioleta (se pinta violeta)
  if (nm < 450) return "#7a5cff";
  if (nm < 495) return "#4aa3ff";
  if (nm < 570) return "#5fd36a";
  if (nm < 590) return "#ffe14a";
  if (nm < 620) return "#ff9f3a";
  if (nm < 750) return "#ff5a4a";
  return "#b0504a";                      // infrarrojo
}

export function montar(contenedor) {
  const { marco, estado, panel } = estructura(contenedor);
  const lienzo = crearLienzo(marco, { aspecto: 1.2, descripcion: "Placa metálica iluminada, con los electrones que emite, y gráficas del potencial de frenado y de la corriente" });
  const { ctx } = lienzo;

  // ---- Estado: por defecto, potasio con luz de 365 nm (extraordinaria 2026) ----
  const url = parametrosURL();
  let W = url.W ?? 2.29;
  let nm = url.nm ?? 365;
  let intensidad = url.I ?? 60;   // % (número relativo de fotones por segundo)
  let r = F.fotoelectrico(nm * 1e-9, W);
  let reloj = 0;

  // ---- Controles ----
  const gMetal = grupo(panel, "Metal");
  const sMetal = selector(gMetal, {
    etiqueta: "Material de la placa",
    opciones: [...METALES.map((m) => ({ valor: String(m.W), texto: `${m.nombre} (${num(m.W, 2)} eV)` })), { valor: "otro", texto: "Otro (escribe su trabajo de extracción)" }],
    valor: METALES.some((m) => m.W === W) ? String(W) : "otro",
    alCambiar: (v) => { if (v !== "otro") { W = Number(v); cW.valor = W; recalcular(); } },
  });
  const cW = campoNumero(gMetal, { etiqueta: "Trabajo de extracción, W₀", valor: W, unidad: "eV", min: 0, alCambiar: (v) => { W = v; sMetal.valor = METALES.some((m) => m.W === W) ? String(W) : "otro"; recalcular(); } });

  const gLuz = grupo(panel, "Luz");
  const dNm = deslizador(gLuz, {
    etiqueta: "Longitud de onda, λ", min: 100, max: 900, paso: 1, valor: nm,
    formato: (v) => `${num(v)} nm`,
    alCambiar: (v) => { nm = v; cNm.valor = v; recalcular(); },
  });
  const cNm = campoNumero(gLuz, { etiqueta: "…o escríbela", valor: nm, unidad: "nm", min: 1, alCambiar: (v) => { nm = v; dNm.valor = Math.min(900, Math.max(100, v)); recalcular(); } });
  deslizador(gLuz, {
    etiqueta: "Intensidad de la luz", min: 0, max: 100, paso: 5, valor: intensidad,
    formato: (v) => `${v} %`,
    alCambiar: (v) => { intensidad = v; recalcular(); },
  });
  nota(gLuz, "Más intensidad son más fotones por segundo, todos con la misma energía.");

  const gRes = grupo(panel, "Resultados");
  const poner = lecturas(gRes, [
    ["f", "Frecuencia de la luz, f"],
    ["foton", "Energía de cada fotón"],
    ["umbral", "Umbral del metal"],
    ["hay", "¿Hay emisión?"],
    ["Ec", "Energía cinética máxima"],
    ["V", "Potencial de frenado"],
    ["v", "Velocidad máxima de los electrones"],
    ["I", "Corriente de saturación (relativa)"],
  ]);

  function recalcular() {
    if (!(W > 0) || !(nm > 0)) { estado.textContent = "El trabajo de extracción y la longitud de onda deben ser positivos."; return; }
    r = F.fotoelectrico(nm * 1e-9, W);
    poner("f", medida(r.f, "Hz"));
    poner("foton", `${num(r.foton, 2)} eV = ${medida(r.fotonJ, "J")}`);
    poner("umbral", `f₀ = ${medida(r.f0, "Hz")} · λ₀ = ${num(r.lambda0 * 1e9)} nm`);
    poner("hay", r.hay ? "Sí: el fotón supera W₀" : "No: al fotón le falta energía");
    poner("Ec", r.hay ? `${num(r.Ec, 2)} eV = ${medida(r.EcJ, "J")}` : "—");
    poner("V", r.hay ? `${num(r.Vfrenado, 2)} V` : "—");
    poner("v", r.hay ? medida(r.vMax, "m/s") : "—");
    poner("I", r.hay ? `${intensidad} %` : "0");
    estado.textContent = r.hay
      ? `Se emiten electrones con hasta ${num(r.Ec, 2)} eV`
      : "No se emite ningún electrón, por intensa que sea la luz";
    dibujar();
  }

  // ---- Dibujo ----
  function dibujar() {
    const { ancho, alto } = lienzo;
    ctx.fillStyle = TINTA.fondo;
    ctx.fillRect(0, 0, ancho, alto);
    const color = colorLuz(nm);

    // Escena: placa a la izquierda, fotones que llegan y electrones que salen.
    const y0 = 62;
    const hEscena = Math.max(90, alto * 0.24);
    ctx.fillStyle = "#8a93a6";
    ctx.fillRect(18, y0, 14, hEscena);
    rotulo(ctx, "metal", 25, y0 + hEscena + 10, { alinear: "center", color: TINTA.suave, tam: 11 });
    const nFotones = Math.round(intensidad / 10);
    for (let i = 0; i < nFotones; i++) {
      const fase = (reloj * 0.5 + i / nFotones) % 1;
      const yy = y0 + 10 + ((i * 37) % (hEscena - 20));
      const xx = ancho - 20 - fase * (ancho - 60);
      // Fotón: pequeño tren de ondas
      const tren = [];
      for (let k = 0; k <= 16; k++) tren.push([xx + k * 1.6, yy + Math.sin(k * 1.2 + reloj * 20) * 3.5]);
      trazar(ctx, tren, color, { grosor: 1.8 });
      if (r.hay) {
        const sale = (reloj * (0.25 + 0.5 * Math.min(1, r.Ec / 5)) + i / nFotones) % 1;
        punto(ctx, 36 + sale * (ancho * 0.45), yy + 8 - sale * 10, TINTA.b, 3);
      }
    }
    rotulo(ctx, `fotones de ${num(nm)} nm`, ancho - 14, y0 - 12, { alinear: "right", color, tam: 11, negrita: true });
    if (r.hay) rotulo(ctx, "electrones", 44, y0 - 12, { color: TINTA.b, tam: 11, negrita: true });

    const izq = 44;
    const w = ancho - izq - 14;
    const yG = y0 + hEscena + 46;
    const hG = (alto - yG - 96) / 2;

    // Gráfica 1: potencial de frenado frente a la frecuencia (recta de pendiente h/e)
    const fMax = Math.max(2.2 * r.f0, 1.15 * r.f, 1.2e15);
    const vMax = Math.max((F.H * fMax) / F.E - W, 1);
    const g1 = { x: izq, y: yG, ancho: w, alto: hG };
    const a1 = ejes(ctx, { ...g1, xr: [0, fMax / 1e14], yr: [0, vMax], xlab: "f (10¹⁴ Hz)", ylab: "V frenado (V)", titulo: "Potencial de frenado frente a frecuencia" });
    trazar(ctx, [[a1.X(0), a1.Y(0)], [a1.X(r.f0 / 1e14), a1.Y(0)], [a1.X(fMax / 1e14), a1.Y(vMax)]], TINTA.a, { recorte: g1 });
    punto(ctx, a1.X(r.f0 / 1e14), a1.Y(0), TINTA.c, 4);
    rotulo(ctx, "f₀", a1.X(r.f0 / 1e14) + 6, a1.Y(0) - 9, { color: TINTA.c, tam: 11 });
    punto(ctx, a1.X(r.f / 1e14), a1.Y(r.Vfrenado), color, 5);

    // Gráfica 2: corriente frente al potencial aplicado
    const g2 = { x: izq, y: yG + hG + 62, ancho: w, alto: hG };
    const vLim = Math.max(3, Math.ceil(r.Vfrenado + 1.5));
    const a2 = ejes(ctx, { ...g2, xr: [-vLim, vLim], yr: [0, 110], xlab: "V aplicado (V)", ylab: "I (%)", titulo: "Corriente frente al potencial aplicado" });
    if (r.hay) {
      const curva = [];
      for (let i = 0; i <= 160; i++) {
        const v = -vLim + (2 * vLim * i) / 160;
        const I = v <= -r.Vfrenado ? 0 : intensidad * (1 - Math.exp(-(v + r.Vfrenado) / (0.45 * r.Vfrenado + 0.25)));
        curva.push([a2.X(v), a2.Y(I)]);
      }
      trazar(ctx, curva, TINTA.b, { recorte: g2 });
      punto(ctx, a2.X(-r.Vfrenado), a2.Y(0), TINTA.c, 4);
      rotulo(ctx, `−${num(r.Vfrenado, 2)} V`, a2.X(-r.Vfrenado), a2.Y(0) - 10, { color: TINTA.c, tam: 11, alinear: "center" });
    } else {
      rotulo(ctx, "Sin emisión no hay corriente", g2.x + w / 2, g2.y + hG / 2, { alinear: "center", color: TINTA.suave });
    }
  }
  lienzo.alRedimensionar = () => dibujar();

  const animacion = bucle((dt) => { reloj += dt; dibujar(); });
  recalcular();
  if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) animacion.arrancar();
  return { get resultado() { return r; } };
}
