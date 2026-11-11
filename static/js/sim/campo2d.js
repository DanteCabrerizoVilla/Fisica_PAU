// Motor común de tres simulaciones: cargas puntuales, masas puntuales e hilos
// con corriente. Se colocan las fuentes y un punto A, y se obtienen el campo de
// cada fuente, el total y, donde lo hay, el potencial y el trabajo de A a B.
// La física está en fisica-campos.js.

import * as F from "./fisica-campos.js";
import {
  TINTA, arrastre, campoNumero, crearLienzo, estructura, flecha, grupo, lecturas, marcas,
  corto, medida, nota, parametroTexto, parametrosURL, punto, rotulo, selector, trazar,
} from "./kit.js";

const LONGITUDES = { m: 1, cm: 1e-2, mm: 1e-3, nm: 1e-9 };
const COLORES = [TINTA.c, TINTA.d, TINTA.b, TINTA.e];

const MODOS = {
  cargas: {
    fuente: "Carga", simbolo: "q", unidadValor: "nC", factor: 1e-9, k: F.K,
    campo: "E", unidadCampo: "N/C", unidadPot: "V", prueba: "Carga que se traslada, q′", unidadTrabajo: "J",
    porDefecto: { u: "m", fuentes: [[-2, -5, 0], [2, 5, 0]], A: [5, 4], B: [0, 4], prueba: 3 },
  },
  masas: {
    fuente: "Masa", simbolo: "m", unidadValor: "kg", factor: 1, k: -F.G,
    campo: "g", unidadCampo: "N/kg", unidadPot: "J/kg", prueba: "Masa que se traslada, m′", unidadTrabajo: "J",
    porDefecto: { u: "m", fuentes: [[2, 0, 0], [4, 4, 0]], A: [0, 2], B: [2, 0], prueba: 1 },
  },
  hilos: {
    fuente: "Hilo", simbolo: "I", unidadValor: "A", factor: 1, k: null,
    campo: "B", unidadCampo: "T",
    porDefecto: { u: "cm", fuentes: [[5, 0, 6], [2.5, 6, 0]], A: [4, 2], B: null, prueba: 0 },
  },
};

export function montarCampo(contenedor, modo) {
  const M = MODOS[modo];
  const esHilos = modo === "hilos";
  const { marco, estado, panel } = estructura(contenedor);
  const lienzo = crearLienzo(marco, { aspecto: 1.22, descripcion: `Plano con las fuentes, el punto A y los vectores del campo ${M.campo}` });
  const { ctx } = lienzo;

  // ---- Estado ----
  const url = parametrosURL();
  const def = M.porDefecto;
  let unidad = LONGITUDES[parametroTexto("u")] ? parametroTexto("u") : def.u;
  let n = Math.min(4, Math.max(1, url.n ?? def.fuentes.length));
  const fuentes = [0, 1, 2, 3].map((i) => {
    const d = def.fuentes[i] ?? [i % 2 ? -1 : 1, i === 2 ? 0 : 2, i === 2 ? 4 : -3];
    return { valor: url[`q${i + 1}`] ?? d[0], x: url[`x${i + 1}`] ?? d[1], y: url[`y${i + 1}`] ?? d[2] };
  });
  const A = { x: url.ax ?? def.A[0], y: url.ay ?? def.A[1] };
  const B = { x: url.bx ?? (def.B ? def.B[0] : 0), y: url.by ?? (def.B ? def.B[1] : 0) };
  let prueba = url.qp ?? def.prueba;
  let vista = null;
  let congelada = null;

  // ---- Controles ----
  const gFuentes = grupo(panel, esHilos ? "Hilos (perpendiculares al dibujo)" : `${M.fuente}s`);
  selector(gFuentes, {
    etiqueta: `Número de ${M.fuente.toLowerCase()}s`,
    opciones: [1, 2, 3, 4].map((v) => ({ valor: String(v), texto: String(v) })),
    valor: String(n),
    alCambiar: (v) => { n = Number(v); mostrar(); recalcular(); },
  });
  selector(gFuentes, {
    etiqueta: "Unidad de las posiciones",
    opciones: Object.keys(LONGITUDES).map((v) => ({ valor: v, texto: v })),
    valor: unidad,
    alCambiar: (v) => { unidad = v; rotulosUnidad(); recalcular(); },
  });
  if (esHilos) nota(gFuentes, "Intensidad positiva: la corriente sale del dibujo (⊙). Negativa: entra (⊗).");

  const campos = fuentes.map((f, i) => {
    const caja = document.createElement("div");
    caja.className = "sim__fuente";
    const titulo = document.createElement("h3");
    titulo.textContent = `${M.fuente} ${i + 1}`;
    titulo.style.color = "inherit";
    caja.append(titulo);
    gFuentes.append(caja);
    const cValor = campoNumero(caja, { etiqueta: `${M.simbolo}${"₁₂₃₄"[i]}`, valor: f.valor, unidad: M.unidadValor, alCambiar: (v) => { f.valor = v; recalcular(); } });
    const par = document.createElement("div");
    par.className = "sim__par";
    caja.append(par);
    const cx = campoNumero(par, { etiqueta: "x", valor: f.x, unidad, alCambiar: (v) => { f.x = v; recalcular(); } });
    const cy = campoNumero(par, { etiqueta: "y", valor: f.y, unidad, alCambiar: (v) => { f.y = v; recalcular(); } });
    return { caja, cValor, cx, cy };
  });

  const gPuntos = grupo(panel, esHilos ? "Punto donde se calcula el campo" : "Puntos");
  const parA = document.createElement("div");
  parA.className = "sim__par";
  gPuntos.append(parA);
  const cAx = campoNumero(parA, { etiqueta: "A: x", valor: A.x, unidad, alCambiar: (v) => { A.x = v; recalcular(); } });
  const cAy = campoNumero(parA, { etiqueta: "A: y", valor: A.y, unidad, alCambiar: (v) => { A.y = v; recalcular(); } });
  let cBx = null;
  let cBy = null;
  if (!esHilos) {
    const parB = document.createElement("div");
    parB.className = "sim__par";
    gPuntos.append(parB);
    cBx = campoNumero(parB, { etiqueta: "B: x", valor: B.x, unidad, alCambiar: (v) => { B.x = v; recalcular(); } });
    cBy = campoNumero(parB, { etiqueta: "B: y", valor: B.y, unidad, alCambiar: (v) => { B.y = v; recalcular(); } });
    campoNumero(gPuntos, { etiqueta: M.prueba, valor: prueba, unidad: M.unidadValor, alCambiar: (v) => { prueba = v; recalcular(); } });
  }
  nota(gPuntos, "Los puntos y las fuentes también se pueden arrastrar sobre el dibujo.");

  const gA = grupo(panel, `Campo en A`);
  const filasA = [];
  for (let i = 0; i < 4; i++) filasA.push([`f${i}`, `${M.campo}${"₁₂₃₄"[i]} (de ${M.fuente.toLowerCase()} ${i + 1})`]);
  filasA.push(["total", `${M.campo} total`], ["modulo", `Módulo de ${M.campo}`]);
  if (!esHilos) filasA.push(["VA", "Potencial en A"]);
  const ponerA = lecturas(gA, filasA);
  const celdasFuente = [...gA.querySelectorAll("dt")].slice(0, 4).map((dt) => [dt, dt.nextElementSibling]);

  const gExtra = grupo(panel, esHilos ? "Entre los hilos 1 y 2" : "De A a B");
  const ponerX = lecturas(gExtra, esHilos
    ? [["fuerza", "Fuerza por unidad de longitud"], ["tipo", "Los hilos"]]
    : [["VB", "Potencial en B"], ["W", "Trabajo del campo, W(A→B)"], ["signo", "El traslado"]]);

  const gNulo = grupo(panel, "Dónde se anula el campo");
  const ponerN = lecturas(gNulo, [["n1", "En la recta que une 1 y 2"], ["n2", "Otro punto de esa recta"]]);

  function rotulosUnidad() {
    for (const c of [...campos.flatMap((f) => [f.cx, f.cy]), cAx, cAy, cBx, cBy]) {
      if (c) c.caja.querySelector(".sim__unidad").textContent = unidad;
    }
  }
  function mostrar() {
    campos.forEach((c, i) => { c.caja.hidden = i >= n; });
    celdasFuente.forEach(([dt, dd], i) => { dt.hidden = dd.hidden = i >= n; });
    gNulo.hidden = n < 2;
    if (esHilos) gExtra.hidden = n < 2;
  }

  // ---- Cálculo (todo en SI) ----
  const escala = () => LONGITUDES[unidad];
  const activas = () => fuentes.slice(0, n).map((f) => ({ valor: f.valor * M.factor, x: f.x * escala(), y: f.y * escala() }));
  const enSI = (p) => ({ x: p.x * escala(), y: p.y * escala() });
  const campoDe = (lista, p) => (esHilos ? F.campoHilos(lista, p) : F.campoRadial(lista, p, M.k));
  const vector = (v) => `(${medida(v.x, "")}; ${medida(v.y, "")}) ${M.unidadCampo}`;

  let calculo = null;
  function recalcular() {
    const lista = activas();
    const a = enSI(A);
    const partes = lista.map((f) => campoDe([f], a));
    const total = campoDe(lista, a);
    // Si las contribuciones se anulan, queda ruido de redondeo: se muestra como cero.
    const sumaModulos = partes.reduce((s, v) => s + Math.hypot(v.x, v.y), 0);
    if (Number.isFinite(sumaModulos)) for (const eje of ["x", "y"]) if (Math.abs(total[eje]) < 1e-9 * sumaModulos) total[eje] = 0;
    calculo = { lista, partes, total };
    if (!Number.isFinite(total.x)) {
      estado.innerHTML = "El punto A coincide con una fuente: muévelo.";
      dibujar();
      return;
    }
    partes.forEach((v, i) => ponerA(`f${i}`, vector(v)));
    ponerA("total", vector(total));
    const modulo = Math.hypot(total.x, total.y);
    ponerA("modulo", medida(modulo, M.unidadCampo));
    estado.innerHTML = `${M.campo} en A = ${medida(modulo, M.unidadCampo)}`;

    if (esHilos) {
      if (n >= 2) {
        const d = Math.hypot(lista[0].x - lista[1].x, lista[0].y - lista[1].y);
        const fz = F.fuerzaEntreHilos(lista[0].valor, lista[1].valor, d);
        ponerX("fuerza", d > 0 ? medida(fz.modulo, "N/m") : "—");
        ponerX("tipo", lista[0].valor * lista[1].valor === 0 ? "no se ejercen fuerza" : fz.atractiva ? "se atraen (corrientes del mismo sentido)" : "se repelen (corrientes opuestas)");
      }
    } else {
      const VA = F.potencial(lista, a, M.k);
      const VB = F.potencial(lista, enSI(B), M.k);
      const W = prueba * M.factor * (VA - VB);
      ponerA("VA", medida(VA, M.unidadPot));
      ponerX("VB", medida(VB, M.unidadPot));
      ponerX("W", medida(W, M.unidadTrabajo));
      ponerX("signo", Math.abs(W) < 1e-30 ? "no cuesta ni cede energía" : W > 0 ? "lo hace el campo por sí solo (W > 0)" : "necesita una fuerza externa (W < 0)");
    }

    if (n >= 2) {
      const nulos = F.puntosNulos((p) => campoDe(lista, p), lista[0], lista[1], { transversal: esHilos });
      calculo.nulos = nulos;
      const texto = (p) => `(${medida(p.x / escala(), "")}; ${medida(p.y / escala(), "")}) ${unidad} · ${p.t > 0 && p.t < 1 ? "entre las dos" : "fuera del segmento"}`;
      ponerN("n1", nulos[0] ? texto(nulos[0]) : "no se anula");
      ponerN("n2", nulos[1] ? texto(nulos[1]) : "—");
    }
    dibujar();
  }

  // ---- Dibujo ----
  function dibujar() {
    const { ancho, alto } = lienzo;
    ctx.fillStyle = TINTA.fondo;
    ctx.fillRect(0, 0, ancho, alto);
    if (!calculo) return;

    // Encuadre: todas las fuentes y los puntos, con la misma escala en x e y.
    const pts = [...fuentes.slice(0, n), A, ...(esHilos ? [] : [B]), { x: 0, y: 0 }];
    let x0 = Math.min(...pts.map((p) => p.x));
    let x1 = Math.max(...pts.map((p) => p.x));
    let y0 = Math.min(...pts.map((p) => p.y));
    let y1 = Math.max(...pts.map((p) => p.y));
    let lado = Math.max(x1 - x0, y1 - y0, 1e-9) * 1.45;
    const cx = (x0 + x1) / 2;
    const cy = (y0 + y1) / 2;
    x0 = cx - lado / 2; y0 = cy - lado / 2;
    // Mientras se arrastra algo, el encuadre no cambia: así el objeto sigue al dedo.
    if (congelada) ({ x0, y0, lado } = congelada);
    x1 = x0 + lado; y1 = y0 + lado;
    const m = 30;
    const tam = Math.min(ancho - 2 * m, alto - 92);
    const izq = (ancho - tam) / 2 + 6;
    const sup = 56;
    const X = (v) => izq + ((v - x0) / lado) * tam;
    const Y = (v) => sup + tam - ((v - y0) / lado) * tam;
    vista = { X, Y, x0, y0, lado, tam, izq, sup };

    // Rejilla y ejes
    ctx.font = "11px system-ui, sans-serif";
    for (const v of marcas(x0, x1, 6)) {
      trazar(ctx, [[X(v), sup], [X(v), sup + tam]], v === 0 ? TINTA.eje : TINTA.rejilla, { grosor: 1 });
      rotulo(ctx, corto(v), X(v), sup + tam + 11, { alinear: "center", color: TINTA.suave, tam: 11 });
    }
    for (const v of marcas(y0, y1, 6)) {
      trazar(ctx, [[izq, Y(v)], [izq + tam, Y(v)]], v === 0 ? TINTA.eje : TINTA.rejilla, { grosor: 1 });
      rotulo(ctx, corto(v), izq - 4, Y(v), { alinear: "right", color: TINTA.suave, tam: 11 });
    }
    rotulo(ctx, `x (${unidad})`, izq + tam, sup + tam + 27, { alinear: "right", tam: 11 });
    rotulo(ctx, `y (${unidad})`, izq, sup - 10, { tam: 11 });

    // Mapa de direcciones del campo total
    const e = escala();
    const N = 13;
    for (let i = 0; i < N; i++) {
      for (let j = 0; j < N; j++) {
        const px = x0 + ((i + 0.5) / N) * lado;
        const py = y0 + ((j + 0.5) / N) * lado;
        const c = campoDe(calculo.lista, { x: px * e, y: py * e });
        const mod = Math.hypot(c.x, c.y);
        if (!(mod > 0) || !Number.isFinite(mod)) continue;
        flecha(ctx, X(px) - (c.x / mod) * 6, Y(py) + (c.y / mod) * 6, (c.x / mod) * 12, -(c.y / mod) * 12, "rgba(255,255,255,0.22)", 1.2);
      }
    }

    // Vectores en A: cada fuente y el total, con una escala común.
    if (Number.isFinite(calculo.total.x)) {
      const mayor = Math.max(...calculo.partes.map((v) => Math.hypot(v.x, v.y)), Math.hypot(calculo.total.x, calculo.total.y)) || 1;
      const k = 70 / mayor;
      if (n > 1) calculo.partes.forEach((v, i) => flecha(ctx, X(A.x), Y(A.y), v.x * k, -v.y * k, COLORES[i], 2));
      flecha(ctx, X(A.x), Y(A.y), calculo.total.x * k, -calculo.total.y * k, TINTA.a, 3.5);
    }

    // Puntos donde se anula el campo
    for (const p of calculo.nulos ?? []) {
      const px = X(p.x / e);
      const py = Y(p.y / e);
      if (px < izq || px > izq + tam || py < sup || py > sup + tam) continue;
      ctx.strokeStyle = TINTA.b; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.arc(px, py, 7, 0, 2 * Math.PI); ctx.stroke();
      rotulo(ctx, `${M.campo} = 0`, px + 10, py - 10, { color: TINTA.b, tam: 11 });
    }

    // Fuentes
    fuentes.slice(0, n).forEach((f, i) => {
      const px = X(f.x);
      const py = Y(f.y);
      ctx.beginPath(); ctx.arc(px, py, 10, 0, 2 * Math.PI);
      ctx.fillStyle = esHilos ? TINTA.fondo : COLORES[i]; ctx.fill();
      ctx.strokeStyle = COLORES[i]; ctx.lineWidth = 2.5; ctx.stroke();
      if (esHilos) {
        if (f.valor > 0) punto(ctx, px, py, COLORES[i], 3.5);
        else if (f.valor < 0) {
          trazar(ctx, [[px - 5, py - 5], [px + 5, py + 5]], COLORES[i]);
          trazar(ctx, [[px - 5, py + 5], [px + 5, py - 5]], COLORES[i]);
        }
      } else {
        rotulo(ctx, modo === "masas" ? "" : f.valor > 0 ? "+" : f.valor < 0 ? "−" : "", px, py + 1, { color: "#0e1320", alinear: "center", negrita: true, tam: 14 });
      }
      rotulo(ctx, `${i + 1}`, px + 13, py + 13, { color: COLORES[i], negrita: true });
    });

    // Puntos A y B
    punto(ctx, X(A.x), Y(A.y), "#ffffff", 5);
    rotulo(ctx, "A", X(A.x) - 12, Y(A.y) + 12, { negrita: true, alinear: "center" });
    if (!esHilos) {
      punto(ctx, X(B.x), Y(B.y), TINTA.suave, 5);
      rotulo(ctx, "B", X(B.x) - 12, Y(B.y) + 12, { negrita: true, alinear: "center", color: TINTA.suave });
    }
    rotulo(ctx, `Flecha amarilla: ${M.campo} total en A`, izq, sup + tam + 27, { color: TINTA.a, tam: 11 });
  }
  lienzo.alRedimensionar = () => dibujar();

  // ---- Arrastre de puntos y fuentes ----
  const objetos = () => [
    { p: A, campos: [cAx, cAy] },
    ...(esHilos ? [] : [{ p: B, campos: [cBx, cBy] }]),
    ...fuentes.slice(0, n).map((f, i) => ({ p: f, campos: [campos[i].cx, campos[i].cy] })),
  ];
  arrastre(lienzo.canvas, {
    buscar: (pt) => {
      if (!vista) return null;
      let mejor = null;
      let dMin = 26;
      for (const o of objetos()) {
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
      o.campos[0].valor = o.p.x;
      o.campos[1].valor = o.p.y;
      recalcular();
    },
    soltar: () => { congelada = null; dibujar(); },
  });

  mostrar();
  recalcular();
  return { get calculo() { return calculo; } };
}
