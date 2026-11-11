// Simulación: focos sonoros puntuales. Cada foco se define por su potencia o
// por el nivel que produce a cierta distancia; se mide la intensidad y el nivel
// en la posición del observador. La física está en fisica-ondas.js.

import * as F from "./fisica-ondas.js";
import {
  TINTA, arrastre, campoNumero, corto, crearLienzo, estructura, grupo, lecturas, marcas,
  medida, nota, num, parametroTexto, parametrosURL, punto, rotulo, selector, trazar,
} from "./kit.js";

const COLORES = [TINTA.c, TINTA.d, TINTA.e];

export function montar(contenedor) {
  const { marco, estado, panel } = estructura(contenedor);
  const lienzo = crearLienzo(marco, { aspecto: 1.22, descripcion: "Plano con los focos sonoros, el observador y el nivel de intensidad en cada zona" });
  const { ctx } = lienzo;

  // ---- Estado: por defecto, los dos focos de la extraordinaria de 2024 ----
  const url = parametrosURL();
  let n = Math.min(3, Math.max(1, url.n ?? 2));
  const predeterminados = [
    { dato: "nivel", P: 1e-4, dB: 55, r: 2, veces: 1, x: 0, y: 3 },
    { dato: "nivel", P: 1e-4, dB: 65, r: 2, veces: 1, x: 4, y: 0 },
    { dato: "potencia", P: 1e-4, dB: 60, r: 1, veces: 1, x: 4, y: 3 },
  ];
  const focos = predeterminados.map((d, i) => {
    const k = i + 1;
    const dato = parametroTexto(`d${k}`) === "potencia" || url[`P${k}`] !== undefined ? "potencia" : url[`dB${k}`] !== undefined ? "nivel" : d.dato;
    return {
      dato, P: url[`P${k}`] ?? d.P, dB: url[`dB${k}`] ?? d.dB, r: url[`r${k}`] ?? d.r,
      veces: url[`n${k}`] ?? d.veces, x: url[`x${k}`] ?? d.x, y: url[`y${k}`] ?? d.y,
    };
  });
  const obs = { x: url.ox ?? 0, y: url.oy ?? 0 };
  let vista = null;
  let congelada = null;
  let calculo = null;

  // ---- Controles ----
  const gFocos = grupo(panel, "Focos");
  selector(gFocos, {
    etiqueta: "Número de focos",
    opciones: [1, 2, 3].map((v) => ({ valor: String(v), texto: String(v) })),
    valor: String(n),
    alCambiar: (v) => { n = Number(v); mostrar(); recalcular(); },
  });
  const campos = focos.map((f, i) => {
    const caja = document.createElement("div");
    caja.className = "sim__fuente";
    const titulo = document.createElement("h3");
    titulo.textContent = `Foco ${i + 1}`;
    caja.append(titulo);
    gFocos.append(caja);
    selector(caja, {
      etiqueta: "Dato del enunciado",
      opciones: [{ valor: "nivel", texto: "Nivel (dB) a una distancia" }, { valor: "potencia", texto: "Potencia (W)" }],
      valor: f.dato,
      alCambiar: (v) => { f.dato = v; mostrar(); recalcular(); },
    });
    const cP = campoNumero(caja, { etiqueta: "Potencia", valor: f.P, unidad: "W", min: 0, alCambiar: (v) => { f.P = v; recalcular(); } });
    const parN = document.createElement("div");
    parN.className = "sim__par";
    caja.append(parN);
    campoNumero(parN, { etiqueta: "Nivel", valor: f.dB, unidad: "dB", alCambiar: (v) => { f.dB = v; recalcular(); } });
    campoNumero(parN, { etiqueta: "medido a", valor: f.r, unidad: "m", min: 0, alCambiar: (v) => { f.r = v; recalcular(); } });
    campoNumero(caja, { etiqueta: "Fuentes iguales en ese punto", valor: f.veces, unidad: "", min: 1, paso: 1, alCambiar: (v) => { f.veces = Math.max(1, Math.round(v)); recalcular(); } });
    const par = document.createElement("div");
    par.className = "sim__par";
    caja.append(par);
    const cx = campoNumero(par, { etiqueta: "x", valor: f.x, unidad: "m", alCambiar: (v) => { f.x = v; recalcular(); } });
    const cy = campoNumero(par, { etiqueta: "y", valor: f.y, unidad: "m", alCambiar: (v) => { f.y = v; recalcular(); } });
    return { caja, cP, parN, cx, cy };
  });

  const gObs = grupo(panel, "Observador");
  const parO = document.createElement("div");
  parO.className = "sim__par";
  gObs.append(parO);
  const cOx = campoNumero(parO, { etiqueta: "x", valor: obs.x, unidad: "m", alCambiar: (v) => { obs.x = v; recalcular(); } });
  const cOy = campoNumero(parO, { etiqueta: "y", valor: obs.y, unidad: "m", alCambiar: (v) => { obs.y = v; recalcular(); } });
  nota(gObs, "También puedes arrastrar al observador y los focos sobre el dibujo.");

  const gRes = grupo(panel, "Lo que recibe el observador");
  const filas = [];
  for (let i = 0; i < 3; i++) filas.push([`f${i}`, `Del foco ${i + 1}`]);
  filas.push(["I", "Intensidad total"], ["dB", "Nivel de intensidad"]);
  const poner = lecturas(gRes, filas);
  const celdas = [...gRes.querySelectorAll("dt")].slice(0, 3).map((dt) => [dt, dt.nextElementSibling]);
  nota(gRes, "Se suman las intensidades, no los decibelios.");

  const gPot = grupo(panel, "Potencia de cada foco");
  const ponerP = lecturas(gPot, [0, 1, 2].map((i) => [`p${i}`, `Foco ${i + 1}`]));
  const celdasP = [...gPot.querySelectorAll("dt")].map((dt) => [dt, dt.nextElementSibling]);
  const gIgual = grupo(panel, "Igual intensidad de los focos 1 y 2");
  const ponerI = lecturas(gIgual, [["x", "Distancia al foco 1, sobre el segmento"]]);

  function mostrar() {
    campos.forEach((c, i) => {
      c.caja.hidden = i >= n;
      c.cP.caja.hidden = focos[i].dato !== "potencia";
      c.parN.hidden = focos[i].dato !== "nivel";
    });
    for (const lista of [celdas, celdasP]) lista.forEach(([dt, dd], i) => { dt.hidden = dd.hidden = i >= n; });
    gIgual.hidden = n < 2;
  }

  // ---- Cálculo ----
  const potencia = (f) => f.veces * (f.dato === "potencia" ? f.P : F.potenciaDeNivel(f.dB, f.r));
  function recalcular() {
    const lista = focos.slice(0, n).map((f) => ({ P: potencia(f), x: f.x, y: f.y }));
    calculo = { lista };
    let total = 0;
    lista.forEach((f, i) => {
      const d = Math.hypot(obs.x - f.x, obs.y - f.y);
      const I = F.intensidad(f.P, d);
      total += I;
      poner(`f${i}`, d > 0 ? `${medida(I, "W/m²")}<br>${num(F.nivel(I), 1)} dB a ${num(d, 2)} m` : "—");
      ponerP(`p${i}`, medida(f.P, "W"));
    });
    poner("I", Number.isFinite(total) ? medida(total, "W/m²") : "—");
    poner("dB", Number.isFinite(total) ? `${num(F.nivel(total), 1)} dB` : "—");
    estado.innerHTML = Number.isFinite(total) ? `Nivel en el observador: ${num(F.nivel(total), 1)} dB` : "El observador está sobre un foco: muévelo.";
    if (n >= 2) {
      const d = Math.hypot(lista[0].x - lista[1].x, lista[0].y - lista[1].y);
      ponerI("x", d > 0 ? `${num(F.puntoIgualIntensidad(lista[0].P, lista[1].P, d), 2)} m (de ${num(d, 2)} m)` : "—");
    }
    dibujar();
  }

  // ---- Dibujo ----
  function dibujar() {
    const { ancho, alto } = lienzo;
    ctx.fillStyle = TINTA.fondo;
    ctx.fillRect(0, 0, ancho, alto);
    if (!calculo) return;
    const pts = [...focos.slice(0, n), obs];
    let x0 = Math.min(...pts.map((p) => p.x));
    let y0 = Math.min(...pts.map((p) => p.y));
    const x1 = Math.max(...pts.map((p) => p.x));
    const y1 = Math.max(...pts.map((p) => p.y));
    let lado = Math.max(x1 - x0, y1 - y0, 1) * 1.5;
    x0 = (x0 + x1) / 2 - lado / 2; y0 = (y0 + y1) / 2 - lado / 2;
    if (congelada) ({ x0, y0, lado } = congelada);
    const m = 30;
    const tam = Math.min(ancho - 2 * m, alto - 92);
    const izq = (ancho - tam) / 2 + 6;
    const sup = 56;
    const X = (v) => izq + ((v - x0) / lado) * tam;
    const Y = (v) => sup + tam - ((v - y0) / lado) * tam;
    vista = { X, Y, x0, y0, lado, tam, izq, sup };

    // Mapa del nivel sonoro (más claro = más decibelios)
    const N = 36;
    const celda = tam / N;
    for (let i = 0; i < N; i++) {
      for (let j = 0; j < N; j++) {
        const p = { x: x0 + ((i + 0.5) / N) * lado, y: y0 + ((j + 0.5) / N) * lado };
        const dB = F.nivel(F.intensidadTotal(calculo.lista, p));
        const k = Math.max(0, Math.min(1, (dB - 20) / 90));
        ctx.fillStyle = `rgba(255, 209, 102, ${(0.04 + 0.5 * k).toFixed(3)})`;
        const cx0 = Math.round(izq + i * celda);
        const cy0 = Math.round(sup + tam - (j + 1) * celda);
        ctx.fillRect(cx0, cy0, Math.round(izq + (i + 1) * celda) - cx0, Math.round(sup + tam - j * celda) - cy0);
      }
    }
    for (const v of marcas(x0, x0 + lado, 6)) {
      trazar(ctx, [[X(v), sup], [X(v), sup + tam]], v === 0 ? TINTA.eje : TINTA.rejilla, { grosor: 1 });
      rotulo(ctx, corto(v), X(v), sup + tam + 11, { alinear: "center", color: TINTA.suave, tam: 11 });
    }
    for (const v of marcas(y0, y0 + lado, 6)) {
      trazar(ctx, [[izq, Y(v)], [izq + tam, Y(v)]], v === 0 ? TINTA.eje : TINTA.rejilla, { grosor: 1 });
      rotulo(ctx, corto(v), izq - 4, Y(v), { alinear: "right", color: TINTA.suave, tam: 11 });
    }
    rotulo(ctx, "x (m)", izq + tam, sup + tam + 24, { alinear: "right", tam: 11 });
    rotulo(ctx, "y (m)", izq, sup - 10, { tam: 11 });

    focos.slice(0, n).forEach((f, i) => {
      trazar(ctx, [[X(f.x), Y(f.y)], [X(obs.x), Y(obs.y)]], COLORES[i], { grosor: 1, discontinua: true });
      for (const radio of [16, 24]) {
        ctx.beginPath(); ctx.arc(X(f.x), Y(f.y), radio, 0, 2 * Math.PI);
        ctx.strokeStyle = COLORES[i]; ctx.globalAlpha = 0.35; ctx.lineWidth = 1.5; ctx.stroke(); ctx.globalAlpha = 1;
      }
      punto(ctx, X(f.x), Y(f.y), COLORES[i], 9);
      rotulo(ctx, `${i + 1}`, X(f.x), Y(f.y) + 1, { color: "#0e1320", alinear: "center", negrita: true });
    });
    punto(ctx, X(obs.x), Y(obs.y), "#ffffff", 6);
    rotulo(ctx, "observador", X(obs.x) + 10, Y(obs.y) - 10, { negrita: true, tam: 11 });
  }
  lienzo.alRedimensionar = () => dibujar();

  arrastre(lienzo.canvas, {
    buscar: (pt) => {
      if (!vista) return null;
      const objetos = [{ p: obs, c: [cOx, cOy] }, ...focos.slice(0, n).map((f, i) => ({ p: f, c: [campos[i].cx, campos[i].cy] }))];
      let mejor = null;
      let dMin = 26;
      for (const o of objetos) {
        const d = Math.hypot(pt.x - vista.X(o.p.x), pt.y - vista.Y(o.p.y));
        if (d < dMin) { dMin = d; mejor = o; }
      }
      if (!mejor) return null;
      congelada = { x0: vista.x0, y0: vista.y0, lado: vista.lado };
      return { ...mejor, v: { ...vista } };
    },
    mover: (o, pt) => {
      const paso = 10 ** Math.floor(Math.log10(o.v.lado / 20));
      const redondo = (valor) => Number((Math.round(valor / paso) * paso).toPrecision(6));
      o.p.x = redondo(o.v.x0 + ((pt.x - o.v.izq) / o.v.tam) * o.v.lado);
      o.p.y = redondo(o.v.y0 + ((o.v.sup + o.v.tam - pt.y) / o.v.tam) * o.v.lado);
      o.c[0].valor = o.p.x;
      o.c[1].valor = o.p.y;
      recalcular();
    },
    soltar: () => { congelada = null; dibujar(); },
  });

  mostrar();
  recalcular();
  return { get calculo() { return calculo; } };
}
