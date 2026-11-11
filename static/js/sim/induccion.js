// Simulación: inducción electromagnética. Cuatro montajes de examen, con las
// gráficas del flujo y de la fem frente al tiempo. Física en fisica-induccion.js.

import * as F from "./fisica-induccion.js";
import {
  TINTA, botones, bucle, campoNumero, crearLienzo, deslizador, ejes, estructura, grupo,
  lecturas, medida, nota, num, parametroTexto, parametrosURL, punto, rotulo, selector, trazar,
} from "./kit.js";

const MODOS = [
  { valor: "entra", texto: "Espira que entra en un campo" },
  { valor: "tramos", texto: "Campo variable dado por una gráfica" },
  { valor: "gira", texto: "Espira que gira (alternador)" },
  { valor: "seno", texto: "Campo que varía como B₀·sen(ωt)" },
];

export function montar(contenedor) {
  const { marco, estado, panel } = estructura(contenedor);
  const lienzo = crearLienzo(marco, { aspecto: 1.25, descripcion: "Esquema de la espira en el campo magnético y gráficas del flujo y de la fem frente al tiempo" });
  const { ctx } = lienzo;

  // ---- Estado ----
  const url = parametrosURL();
  let modo = MODOS.some((m) => m.valor === parametroTexto("modo")) ? parametroTexto("modo") : "entra";
  const d = {
    B: url.B ?? 0.2, L: url.L ?? 20, a: url.a ?? 20, v: url.v ?? 2,          // entra (cm, m/s, T)
    S: url.S ?? 10, N: url.N ?? 1, R: url.R ?? 15,                             // S en cm²
    w: url.w ?? 50, B0: url.B0 ?? 0.2,
    vertices: [[0, 0], [5, 60], [20, 60], [30, 0]],                            // (ms, mT)
    entra: parametroTexto("campo") !== "sale",
  };
  let montaje = null;
  let t = 0;

  // ---- Controles ----
  const gMontaje = grupo(panel, "Montaje");
  selector(gMontaje, {
    etiqueta: "Situación", opciones: MODOS, valor: modo,
    alCambiar: (v) => {
      modo = v;
      // Valores de partida de un problema de examen para cada situación.
      if (modo === "entra") Object.assign(d, { B: 0.2, L: 20, a: 20, v: 2, R: 15, N: 1 });
      if (modo === "tramos") Object.assign(d, { S: 10, R: 2, N: 1 });
      if (modo === "gira") Object.assign(d, { S: 1257, B: 0.15, w: 50, R: 40, N: 1 });
      if (modo === "seno") Object.assign(d, { S: 1257, B0: 0.2, w: 75, R: 40, N: 1 });
      for (const [clave, c] of Object.entries(campos)) c.valor = d[clave];
      t = 0;
      mostrar();
      recalcular();
    },
  });
  const campos = {
    B: campoNumero(gMontaje, { etiqueta: "Campo magnético, B", valor: d.B, unidad: "T", alCambiar: (v) => { d.B = v; recalcular(); } }),
    B0: campoNumero(gMontaje, { etiqueta: "Amplitud del campo, B₀", valor: d.B0, unidad: "T", alCambiar: (v) => { d.B0 = v; recalcular(); } }),
    L: campoNumero(gMontaje, { etiqueta: "Lado perpendicular al avance, L", valor: d.L, unidad: "cm", min: 0, alCambiar: (v) => { d.L = v; recalcular(); } }),
    a: campoNumero(gMontaje, { etiqueta: "Lado en la dirección del avance", valor: d.a, unidad: "cm", min: 0, alCambiar: (v) => { d.a = v; recalcular(); } }),
    v: campoNumero(gMontaje, { etiqueta: "Velocidad, v", valor: d.v, unidad: "m/s", min: 0, alCambiar: (v) => { d.v = v; recalcular(); } }),
    S: campoNumero(gMontaje, { etiqueta: "Superficie de la espira, S", valor: d.S, unidad: "cm²", min: 0, alCambiar: (v) => { d.S = v; recalcular(); } }),
    w: campoNumero(gMontaje, { etiqueta: "Velocidad angular, ω", valor: d.w, unidad: "rad/s", min: 0, alCambiar: (v) => { d.w = v; recalcular(); } }),
    N: campoNumero(gMontaje, { etiqueta: "Número de espiras, N", valor: d.N, unidad: "", min: 1, paso: 1, alCambiar: (v) => { d.N = Math.max(1, Math.round(v)); recalcular(); } }),
    R: campoNumero(gMontaje, { etiqueta: "Resistencia, R", valor: d.R, unidad: "Ω", min: 0, alCambiar: (v) => { d.R = v; recalcular(); } }),
  };
  const sCampo = selector(gMontaje, {
    etiqueta: "Sentido del campo",
    opciones: [{ valor: "entra", texto: "Entra en el papel (⊗)" }, { valor: "sale", texto: "Sale del papel (⊙)" }],
    valor: d.entra ? "entra" : "sale",
    alCambiar: (v) => { d.entra = v === "entra"; recalcular(); },
  });

  const gTramos = grupo(panel, "Gráfica B(t): vértices");
  d.vertices.forEach((vert, i) => {
    const par = document.createElement("div");
    par.className = "sim__par";
    gTramos.append(par);
    campoNumero(par, { etiqueta: `t${"₁₂₃₄"[i]}`, valor: vert[0], unidad: "ms", min: 0, alCambiar: (v) => { vert[0] = v; recalcular(); } });
    campoNumero(par, { etiqueta: `B${"₁₂₃₄"[i]}`, valor: vert[1], unidad: "mT", alCambiar: (v) => { vert[1] = v; recalcular(); } });
  });
  nota(gTramos, "Los instantes deben ir en orden creciente.");

  const gTiempo = grupo(panel, "Tiempo");
  const dT = deslizador(gTiempo, {
    etiqueta: "Instante, t", min: 0, max: 1000, paso: 1, valor: 0,
    formato: (v) => (montaje ? textoTiempo((v / 1000) * montaje.tMax) : ""),
    alCambiar: (v) => { t = (v / 1000) * montaje.tMax; actualizar(); },
  });
  const boton = botones(gTiempo);
  const bPausa = boton("Reproducir", () => (animacion.activo ? pausar() : seguir()), { suave: true });

  const gAhora = grupo(panel, "En ese instante");
  const poner = lecturas(gAhora, [
    ["flujo", "Flujo, Φ"],
    ["fem", "Fem inducida, ε"],
    ["I", "Intensidad, I"],
    ["sentido", "Sentido de la corriente"],
  ]);
  const gMax = grupo(panel, "Valores máximos");
  const ponerM = lecturas(gMax, [["fem", "Fem máxima"], ["I", "Intensidad máxima"], ["extra", "Dato del montaje"]]);
  nota(gMax, "El signo de la fem depende del sentido que se elija para la normal; aquí va en el sentido del campo.");

  const textoTiempo = (s) => (s < 1 ? `${num(s * 1000, s < 0.01 ? 2 : 1)} ms` : `${num(s, 2)} s`);
  const visibles = { entra: ["B", "L", "a", "v", "N", "R"], tramos: ["S", "N", "R"], gira: ["B", "S", "w", "N", "R"], seno: ["B0", "S", "w", "N", "R"] };
  function mostrar() {
    for (const [clave, c] of Object.entries(campos)) c.caja.hidden = !visibles[modo].includes(clave);
    gTramos.hidden = modo !== "tramos";
    sCampo.caja.hidden = modo === "gira" || modo === "seno";
  }

  // ---- Cálculo ----
  function recalcular() {
    const S = d.S * 1e-4;
    try {
      if (modo === "entra") montaje = F.espiraEntrando({ B: d.B, L: d.L / 100, a: d.a / 100, v: d.v, N: d.N });
      else if (modo === "tramos") montaje = F.campoPorTramos({ S, N: d.N }, d.vertices.map(([ms, mT]) => [ms / 1000, mT / 1000]));
      else if (modo === "gira") montaje = F.espiraGirando({ N: d.N, S, B: d.B, w: d.w });
      else montaje = F.campoSenoidal({ N: d.N, S, B0: d.B0, w: d.w });
    } catch { montaje = null; }
    if (!montaje || !(montaje.tMax > 0) || !Number.isFinite(montaje.tMax) || !(d.R > 0)) {
      montaje = null;
      estado.textContent = "Revisa los datos: hay alguno nulo o fuera de orden.";
      dibujar();
      return;
    }
    t = Math.min(t, montaje.tMax);
    ponerM("fem", medida(montaje.femMax, "V"));
    ponerM("I", medida(montaje.femMax / d.R, "A"));
    ponerM("extra", modo === "entra" ? `Tarda ${textoTiempo(montaje.tEntrada)} en entrar del todo`
      : modo === "tramos" ? "Hay fem solo en los tramos inclinados"
        : `Periodo: ${textoTiempo((2 * Math.PI) / d.w)}`);
    actualizar();
  }

  function actualizar() {
    if (!montaje) return;
    dT.valor = Math.round((t / montaje.tMax) * 1000);
    dT.refrescar();
    const flujo = montaje.flujo(t);
    const fem = montaje.fem(t);
    poner("flujo", medida(flujo, "Wb"));
    poner("fem", medida(fem, "V"));
    poner("I", medida(Math.abs(fem) / d.R, "A"));
    let sentido;
    if (modo === "gira" || modo === "seno") sentido = fem === 0 ? "no hay corriente" : "alterna: cambia cada medio periodo";
    else {
      const h = montaje.tMax * 1e-6;
      const variacion = Math.sign(Math.abs(montaje.flujo(t + h)) - Math.abs(montaje.flujo(Math.max(0, t - h))));
      sentido = fem === 0 ? "no hay corriente" : F.sentidoCorriente(variacion, d.entra);
    }
    poner("sentido", sentido);
    estado.innerHTML = fem === 0 ? "El flujo no cambia: no hay fem" : `Fem inducida: ${medida(Math.abs(fem), "V")}`;
    dibujar();
  }

  // ---- Dibujo ----
  function simbolos(x, y, w, h, entra, alfa = 0.8) {
    ctx.save();
    ctx.globalAlpha = alfa;
    ctx.strokeStyle = ctx.fillStyle = TINTA.d;
    ctx.lineWidth = 1.2;
    for (let px = x + 12; px < x + w; px += 24) {
      for (let py = y + 12; py < y + h; py += 24) {
        if (entra) { ctx.beginPath(); ctx.moveTo(px - 4, py - 4); ctx.lineTo(px + 4, py + 4); ctx.moveTo(px - 4, py + 4); ctx.lineTo(px + 4, py - 4); ctx.stroke(); }
        else { ctx.beginPath(); ctx.arc(px, py, 2.2, 0, 2 * Math.PI); ctx.fill(); }
      }
    }
    ctx.restore();
  }

  function dibujar() {
    const { ancho, alto } = lienzo;
    ctx.fillStyle = TINTA.fondo;
    ctx.fillRect(0, 0, ancho, alto);
    if (!montaje) return;

    // Esquema
    const ex = 14, ey = 44, ew = ancho - 28, eh = Math.max(110, alto * 0.24);
    const cy = ey + eh / 2;
    ctx.strokeStyle = TINTA.c; ctx.lineWidth = 3;
    if (modo === "entra") {
      const borde = ex + ew * 0.5;
      simbolos(borde, ey, ew * 0.5, eh, d.entra);
      trazar(ctx, [[borde, ey], [borde, ey + eh]], TINTA.suave, { grosor: 1, discontinua: true });
      const lado = Math.min(eh * 0.6, ew * 0.3);
      const avance = (Math.min(t, montaje.tMax) / montaje.tEntrada) * lado;
      ctx.strokeRect(borde - lado + avance, cy - lado / 2, lado, lado);
      rotulo(ctx, "v →", borde - lado + avance + lado / 2, cy - lado / 2 - 10, { alinear: "center", color: TINTA.b, negrita: true });
    } else if (modo === "tramos" || modo === "seno") {
      const campoRel = modo === "tramos"
        ? montaje.campo(t) / (Math.max(...d.vertices.map((v) => Math.abs(v[1]))) / 1000 || 1)
        : Math.sin(d.w * t);
      simbolos(ex, ey, ew, eh, modo === "tramos" ? d.entra : campoRel >= 0, 0.12 + 0.75 * Math.abs(campoRel));
      ctx.beginPath(); ctx.arc(ex + ew / 2, cy, eh * 0.36, 0, 2 * Math.PI); ctx.stroke();
      rotulo(ctx, "Más símbolos visibles = campo más intenso", ex + ew, ey + eh + 10, { alinear: "right", color: TINTA.suave, tam: 11 });
    } else {
      simbolos(ex, ey, ew, eh, true, 0.6);
      const anchura = Math.abs(Math.cos(d.w * t));
      ctx.beginPath(); ctx.ellipse(ex + ew / 2, cy, Math.max(1.5, eh * 0.38 * anchura), eh * 0.38, 0, 0, 2 * Math.PI); ctx.stroke();
      trazar(ctx, [[ex + ew / 2, ey + 2], [ex + ew / 2, ey + eh - 2]], TINTA.suave, { grosor: 1, discontinua: true });
      rotulo(ctx, "eje de giro", ex + ew / 2 + 6, ey + 8, { color: TINTA.suave, tam: 11 });
    }

    // Gráficas
    const izq = 52;
    const w = ancho - izq - 14;
    const yG = ey + eh + 44;
    const hG = (alto - yG - 92) / 2;
    const muestras = 300;
    const tiempos = Array.from({ length: muestras + 1 }, (_, i) => (montaje.tMax * i) / muestras);
    const enMs = montaje.tMax < 1;
    const kT = enMs ? 1000 : 1;
    const dibujarSerie = (y, f, color, titulo, ylab) => {
      const valores = tiempos.map(f);
      const tope = Math.max(...valores.map(Math.abs)) || 1;
      const g = { x: izq, y, ancho: w, alto: hG };
      const min = Math.min(...valores) < -1e-12 * tope ? -1.2 * tope : 0;
      const a = ejes(ctx, { ...g, xr: [0, montaje.tMax * kT], yr: [min, 1.2 * tope], xlab: enMs ? "t (ms)" : "t (s)", ylab, titulo });
      // La fem tiene saltos: se pinta punto a punto con tramos verticales.
      trazar(ctx, tiempos.map((tt, i) => [a.X(tt * kT), a.Y(valores[i])]), color, { recorte: g });
      trazar(ctx, [[a.X(t * kT), y], [a.X(t * kT), y + hG]], TINTA.suave, { grosor: 1, discontinua: true });
      punto(ctx, a.X(t * kT), a.Y(f(t)), color, 5);
    };
    dibujarSerie(yG, montaje.flujo, TINTA.a, "Flujo magnético", "Φ (Wb)");
    dibujarSerie(yG + hG + 62, montaje.fem, TINTA.b, "Fem inducida", "ε (V)");
  }
  lienzo.alRedimensionar = () => dibujar();

  // ---- Animación: todo el intervalo en unos 8 segundos ----
  const animacion = bucle((dt) => {
    if (!montaje) return;
    t += (dt * montaje.tMax) / 8;
    if (t >= montaje.tMax) { t = montaje.tMax; pausar(); }
    actualizar();
  });
  function pausar() { animacion.parar(); bPausa.textContent = "Reproducir"; }
  function seguir() { if (montaje && t >= montaje.tMax) t = 0; animacion.arrancar(); bPausa.textContent = "Pausa"; }

  mostrar();
  recalcular();
  return { get montaje() { return montaje; } };
}
