// Simulación: refracción. Dos montajes: capas planas y paralelas (lámina,
// estanque, cristales con aire en medio) y prisma. Física en fisica-optica.js.

import * as F from "./fisica-optica.js";
import {
  TINTA, campoNumero, crearLienzo, deslizador, estructura, flecha, grupo, lecturas, medida,
  nota, num, parametroTexto, parametrosURL, rotulo, selector, trazar,
} from "./kit.js";

const grados = (rad) => (rad * 180) / Math.PI;
const rad = (g) => (g * Math.PI) / 180;
const tono = (n) => `rgba(122, 170, 255, ${Math.min(0.5, 0.16 * (n - 1) + (n > 1 ? 0.08 : 0)).toFixed(3)})`;

export function montar(contenedor) {
  const { marco, estado, panel } = estructura(contenedor);
  const lienzo = crearLienzo(marco, { aspecto: 0.95, descripcion: "Marcha del rayo de luz a través de los medios, con las normales y los ángulos" });
  const { ctx } = lienzo;

  // ---- Estado: por defecto, la lámina de la ordinaria de 2026 ----
  const url = parametrosURL();
  let modo = parametroTexto("modo") === "prisma" ? "prisma" : "capas";
  let incidencia = url.i ?? (modo === "prisma" ? 50 : 48);
  let nCapas = Math.min(3, Math.max(1, url.capas ?? 1));
  const d = {
    n0: url.n0 ?? 1, nF: url.nF ?? 1,
    capas: [
      { n: url.n1 ?? 1.7, e: url.e1 ?? 3 },
      { n: url.n2 ?? 1, e: url.e2 ?? 4 },
      { n: url.n3 ?? 1.5, e: url.e3 ?? 10 },
    ],
    nPrisma: url.np ?? 1.66, A: url.A ?? 60,
  };
  let res = null;

  // ---- Controles ----
  const gMontaje = grupo(panel, "Montaje");
  selector(gMontaje, {
    etiqueta: "Qué atraviesa el rayo",
    opciones: [{ valor: "capas", texto: "Capas planas y paralelas" }, { valor: "prisma", texto: "Un prisma" }],
    valor: modo,
    alCambiar: (v) => { modo = v; incidencia = v === "prisma" ? 50 : 48; dI.valor = incidencia; mostrar(); recalcular(); },
  });
  const dI = deslizador(gMontaje, {
    etiqueta: "Ángulo de incidencia", min: 0, max: 89, paso: 0.5, valor: incidencia,
    formato: (v) => `${num(v, 1)}°`,
    alCambiar: (v) => { incidencia = v; recalcular(); },
  });

  const gCapas = grupo(panel, "Medios, en el orden en que los recorre la luz");
  campoNumero(gCapas, { etiqueta: "Índice del medio de entrada", valor: d.n0, min: 1, alCambiar: (v) => { d.n0 = v; recalcular(); } });
  selector(gCapas, {
    etiqueta: "Número de capas intermedias",
    opciones: [1, 2, 3].map((v) => ({ valor: String(v), texto: String(v) })),
    valor: String(nCapas),
    alCambiar: (v) => { nCapas = Number(v); mostrar(); recalcular(); },
  });
  const filasCapa = d.capas.map((capa, i) => {
    const par = document.createElement("div");
    par.className = "sim__par";
    gCapas.append(par);
    campoNumero(par, { etiqueta: `Capa ${i + 1}: n`, valor: capa.n, min: 1, alCambiar: (v) => { capa.n = v; recalcular(); } });
    campoNumero(par, { etiqueta: "espesor", valor: capa.e, unidad: "cm", min: 0, alCambiar: (v) => { capa.e = v; recalcular(); } });
    return par;
  });
  campoNumero(gCapas, { etiqueta: "Índice del medio de salida", valor: d.nF, min: 1, alCambiar: (v) => { d.nF = v; recalcular(); } });

  const gPrisma = grupo(panel, "Prisma");
  campoNumero(gPrisma, { etiqueta: "Índice de refracción del prisma", valor: d.nPrisma, min: 1, alCambiar: (v) => { d.nPrisma = v; recalcular(); } });
  campoNumero(gPrisma, { etiqueta: "Ángulo del prisma (en el vértice)", valor: d.A, unidad: "°", min: 1, max: 120, alCambiar: (v) => { d.A = v; recalcular(); } });
  nota(gPrisma, "El prisma está en el aire (n = 1) y el rayo entra por la cara izquierda.");

  const gRes = grupo(panel, "Marcha del rayo");
  const filas = [["t0", "Ángulo en el medio de entrada"]];
  for (let i = 0; i < 3; i++) filas.push([`c${i}`, `Capa ${i + 1}`]);
  filas.push(["sal", "Ángulo de salida"], ["av", "Avance lateral total"], ["tt", "Tiempo en las capas"], ["lim", "Ángulos límite"]);
  const poner = lecturas(gRes, filas);
  const celdasCapa = [...gRes.querySelectorAll("dt")].slice(1, 4).map((dt) => [dt, dt.nextElementSibling]);
  const gResP = grupo(panel, "Marcha del rayo en el prisma");
  const ponerP = lecturas(gResP, [
    ["alfa", "Refracción en la 1.ª cara, α"],
    ["gamma", "Incidencia en la 2.ª cara"],
    ["lim", "Ángulo límite prisma-aire"],
    ["beta", "Refracción a la salida, β"],
    ["desv", "Desviación total del rayo"],
    ["min", "Reflexión total en la 2.ª cara si"],
  ]);

  function mostrar() {
    const capas = modo === "capas";
    gCapas.hidden = gRes.hidden = !capas;
    gPrisma.hidden = gResP.hidden = capas;
    filasCapa.forEach((f, i) => { f.hidden = i >= nCapas; });
    celdasCapa.forEach(([dt, dd], i) => { dt.hidden = dd.hidden = i >= nCapas; });
  }

  // ---- Cálculo ----
  function recalcular() {
    if (modo === "capas") {
      const medios = [d.n0, ...d.capas.slice(0, nCapas).map((c) => c.n), d.nF];
      const espesores = d.capas.slice(0, nCapas).map((c) => c.e / 100);
      if (medios.some((n) => !(n >= 1)) || espesores.some((e) => !(e > 0))) { res = null; estado.textContent = "Los índices deben ser al menos 1 y los espesores positivos."; dibujar(); return; }
      res = { tipo: "capas", medios, ...F.capasPlanas(medios, espesores, rad(incidencia)) };
      poner("t0", `${num(incidencia, 1)}°`);
      for (let i = 0; i < nCapas; i++) {
        const tr = res.tramos[i];
        poner(`c${i}`, tr ? `${num(grados(tr.angulo), 1)}° · avanza ${num(tr.avance * 100, 2)} cm<br>camino ${num(tr.camino * 100, 2)} cm · ${medida(tr.tiempo, "s")}` : "no llega");
      }
      poner("sal", res.anguloSalida !== null ? `${num(grados(res.anguloSalida), 1)}°` : "no sale");
      poner("av", `${num(res.avanceTotal * 100, 2)} cm`);
      poner("tt", medida(res.tiempoTotal, "s"));
      const limites = [];
      for (let i = 0; i < medios.length - 1; i++) {
        const l = F.anguloLimite(medios[i], medios[i + 1]);
        if (l !== null) limites.push(`${num(grados(l), 1)}° (de n = ${num(medios[i], 2)} a ${num(medios[i + 1], 2)})`);
      }
      poner("lim", limites.length ? limites.join("<br>") : "no hay: la luz nunca pasa a un medio de menor índice");
      estado.textContent = res.reflexionEn !== null ? "Reflexión total: el rayo no pasa al medio siguiente" : `El rayo sale con ${num(grados(res.anguloSalida), 1)}°`;
    } else {
      if (!(d.nPrisma > 1) || !(d.A > 0)) { res = null; estado.textContent = "El índice del prisma debe ser mayor que 1."; dibujar(); return; }
      res = { tipo: "prisma", ...F.prisma({ n: d.nPrisma, A: rad(d.A), incidencia: rad(incidencia) }) };
      ponerP("alfa", `${num(grados(res.alfa), 1)}°`);
      ponerP("gamma", `${num(grados(res.gamma), 1)}°`);
      ponerP("lim", `${num(grados(res.limite), 1)}°`);
      ponerP("beta", res.sale ? `${num(grados(res.beta), 1)}°` : "no sale: reflexión total");
      ponerP("desv", res.sale ? `${num(grados(res.desviacion), 1)}°` : "—");
      ponerP("min", res.incidenciaMinima === null ? "siempre (para cualquier incidencia)" : res.incidenciaMinima === 0 ? "nunca: siempre sale" : `la incidencia es menor de ${num(grados(res.incidenciaMinima), 1)}°`);
      estado.textContent = res.sale ? `Sale del prisma con β = ${num(grados(res.beta), 1)}°` : "Reflexión total en la segunda cara";
    }
    dibujar();
  }

  // ---- Dibujo ----
  function arco(x, y, desde, hasta, texto) {
    ctx.beginPath();
    ctx.arc(x, y, 26, Math.min(desde, hasta), Math.max(desde, hasta));
    ctx.strokeStyle = TINTA.a; ctx.lineWidth = 1.5; ctx.stroke();
    const medio = (desde + hasta) / 2;
    rotulo(ctx, texto, x + 42 * Math.cos(medio), y + 42 * Math.sin(medio), { color: TINTA.a, alinear: "center", tam: 11 });
  }

  function dibujarCapas() {
    const { ancho, alto } = lienzo;
    const sup = 86;
    const inf = alto - 70;
    const total = res.tramos.reduce((s, x) => s + x.espesor, 0) || d.capas.slice(0, nCapas).reduce((s, c) => s + c.e / 100, 0);
    const espesores = d.capas.slice(0, nCapas).map((c) => c.e / 100);
    const escala = (inf - sup) / espesores.reduce((s, e) => s + e, 0);
    // Franjas
    ctx.fillStyle = tono(res.medios[0]); ctx.fillRect(0, 0, ancho, sup);
    let y = sup;
    espesores.forEach((e, i) => {
      ctx.fillStyle = tono(res.medios[i + 1]); ctx.fillRect(0, y, ancho, e * escala);
      rotulo(ctx, `n = ${num(res.medios[i + 1], 2)}`, ancho - 10, y + 12, { alinear: "right", tam: 11, color: TINTA.suave });
      y += e * escala;
      trazar(ctx, [[0, y], [ancho, y]], TINTA.eje, { grosor: 1 });
    });
    ctx.fillStyle = tono(res.medios[res.medios.length - 1]); ctx.fillRect(0, inf, ancho, alto - inf);
    trazar(ctx, [[0, sup], [ancho, sup]], TINTA.eje, { grosor: 1 });
    rotulo(ctx, `n = ${num(res.medios[0], 2)}`, ancho - 10, sup - 12, { alinear: "right", tam: 11, color: TINTA.suave });
    rotulo(ctx, `n = ${num(res.medios[res.medios.length - 1], 2)}`, ancho - 10, inf + 14, { alinear: "right", tam: 11, color: TINTA.suave });

    // Rayo: el dibujo se centra según el avance lateral total.
    const avancePx = res.avanceTotal * escala;
    let x = Math.max(60, Math.min(ancho - 60 - avancePx, ancho / 2 - avancePx / 2));
    const i0 = rad(incidencia);
    const L = 64;
    flecha(ctx, x - L * Math.sin(i0), sup - L * Math.cos(i0), L * Math.sin(i0), L * Math.cos(i0), TINTA.c, 2.5);
    trazar(ctx, [[x, sup - 46], [x, sup + 40]], TINTA.suave, { grosor: 1, discontinua: true });
    arco(x, sup, -Math.PI / 2 - i0, -Math.PI / 2, `${num(incidencia, 0)}°`);
    y = sup;
    res.tramos.forEach((tr) => {
      const x2 = x + tr.avance * escala;
      const y2 = y + tr.espesor * escala;
      trazar(ctx, [[x, y], [x2, y2]], TINTA.c, { grosor: 2.5 });
      arco(x, y, Math.PI / 2 - tr.angulo, Math.PI / 2, `${num(grados(tr.angulo), 0)}°`);
      x = x2; y = y2;
      trazar(ctx, [[x, y - 30], [x, y + 30]], TINTA.suave, { grosor: 1, discontinua: true });
    });
    if (res.reflexionEn !== null) {
      // Reflexión total: el rayo vuelve con el mismo ángulo.
      const ang = res.angulos[res.angulos.length - 1];
      flecha(ctx, x, y, 60 * Math.sin(ang), -60 * Math.cos(ang), TINTA.e, 2.5);
      rotulo(ctx, "reflexión total", x + 10, y + 16, { color: TINTA.e, negrita: true, tam: 11 });
    } else {
      const s = res.anguloSalida;
      flecha(ctx, x, y, 60 * Math.sin(s), 60 * Math.cos(s), TINTA.c, 2.5);
    }
    void total;
  }

  function dibujarPrisma() {
    const { ancho, alto } = lienzo;
    const A = rad(d.A);
    const lado = Math.min((alto - 150) / Math.cos(A / 2), (ancho - 150) / (2 * Math.sin(A / 2)));
    const apice = { x: ancho / 2, y: 78 };
    const P = (x, y) => [apice.x + x, apice.y - y];                 // coordenadas con y hacia arriba
    const uL = { x: -Math.sin(A / 2), y: -Math.cos(A / 2) };
    const uR = { x: Math.sin(A / 2), y: -Math.cos(A / 2) };
    const bL = P(uL.x * lado, uL.y * lado);
    const bR = P(uR.x * lado, uR.y * lado);
    ctx.beginPath(); ctx.moveTo(apice.x, apice.y); ctx.lineTo(...bL); ctx.lineTo(...bR); ctx.closePath();
    ctx.fillStyle = tono(d.nPrisma); ctx.fill();
    ctx.strokeStyle = TINTA.eje; ctx.lineWidth = 1.5; ctx.stroke();
    rotulo(ctx, `${num(d.A, 0)}°`, apice.x, apice.y + 26, { alinear: "center", tam: 11 });

    const dir = (angulo) => ({ x: Math.cos(angulo), y: Math.sin(angulo) });
    const E = { x: uL.x * lado * 0.5, y: uL.y * lado * 0.5 };
    const dIn = dir(-A / 2 + rad(incidencia));
    const dDentro = dir(-A / 2 + res.alfa);
    const nL = dir(Math.PI - A / 2);                                 // normal exterior de la cara izquierda
    const nR = dir(A / 2);
    const [ex, ey] = P(E.x, E.y);
    flecha(ctx, ex - 80 * dIn.x, ey + 80 * dIn.y, 80 * dIn.x, -80 * dIn.y, TINTA.c, 2.5);
    trazar(ctx, [[ex + 46 * nL.x, ey - 46 * nL.y], [ex - 40 * nL.x, ey + 40 * nL.y]], TINTA.suave, { grosor: 1, discontinua: true });
    // Corte con la cara derecha: E + k·dDentro = m·uR
    const det = dDentro.x * -uR.y - dDentro.y * -uR.x;
    const k = (-E.x * -uR.y - -E.y * -uR.x) / det;
    const S = { x: E.x + k * dDentro.x, y: E.y + k * dDentro.y };
    const [sx, sy] = P(S.x, S.y);
    trazar(ctx, [[ex, ey], [sx, sy]], TINTA.c, { grosor: 2.5 });
    trazar(ctx, [[sx - 40 * nR.x, sy + 40 * nR.y], [sx + 46 * nR.x, sy - 46 * nR.y]], TINTA.suave, { grosor: 1, discontinua: true });
    rotulo(ctx, `α = ${num(grados(res.alfa), 0)}°`, ex + 14, ey + 18, { color: TINTA.a, tam: 11 });
    if (res.sale) {
      const dOut = dir(A / 2 - res.beta);
      flecha(ctx, sx, sy, 80 * dOut.x, -80 * dOut.y, TINTA.c, 2.5);
      rotulo(ctx, `β = ${num(grados(res.beta), 0)}°`, sx + 16, sy - 16, { color: TINTA.a, tam: 11 });
    } else {
      // Reflexión total: se refleja respecto a la cara derecha.
      const pe = dDentro.x * nR.x + dDentro.y * nR.y;
      const r = { x: dDentro.x - 2 * pe * nR.x, y: dDentro.y - 2 * pe * nR.y };
      flecha(ctx, sx, sy, 70 * r.x, -70 * r.y, TINTA.e, 2.5);
      rotulo(ctx, "reflexión total", sx + 12, sy - 14, { color: TINTA.e, negrita: true, tam: 11 });
    }
  }

  function dibujar() {
    const { ancho, alto } = lienzo;
    ctx.fillStyle = TINTA.fondo;
    ctx.fillRect(0, 0, ancho, alto);
    if (!res) return;
    if (res.tipo === "capas") dibujarCapas(); else dibujarPrisma();
    rotulo(ctx, "Líneas discontinuas: normales. Los ángulos se miden desde ellas.", 12, alto - 12, { color: TINTA.suave, tam: 11 });
  }
  lienzo.alRedimensionar = () => dibujar();

  mostrar();
  recalcular();
  return { get resultado() { return res; } };
}
