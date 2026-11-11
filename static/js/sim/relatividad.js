// Simulación: partícula relativista. Calculadora de γ, masa, energías y
// momento, con la comparación entre la energía cinética clásica y la
// relativista. La física está en fisica-moderna.js.

import * as F from "./fisica-moderna.js";
import {
  TINTA, campoCientifico, crearLienzo, deslizador, ejes, estructura, grupo, lecturas,
  medida, nota, num, parametroTexto, parametrosURL, punto, rotulo, selector, trazar,
} from "./kit.js";

const PARTICULAS = { proton: { nombre: "Protón", m: 1.67e-27 }, electron: { nombre: "Electrón", m: 9.1e-31 }, neutron: { nombre: "Neutrón", m: 1.67e-27 } };
const MeV = 1e6 * F.E;

export function montar(contenedor) {
  const { marco, estado, panel } = estructura(contenedor);
  const lienzo = crearLienzo(marco, { aspecto: 0.8, descripcion: "Energía cinética frente a la velocidad: fórmula clásica y fórmula relativista" });
  const { ctx } = lienzo;

  // ---- Estado: por defecto, protón con 1,4 GeV (modelo 2027) ----
  const url = parametrosURL();
  let m0 = url.m ?? PARTICULAS.proton.m;
  let dato = parametroTexto("dato") === "v" || url.beta !== undefined ? "v" : "Ec";
  let Ec = url.Ec ?? 1.4e9 * F.E;
  let beta = url.beta ?? F.betaDeEnergiaCinetica(m0, Ec);
  let r = F.relativista(m0, beta);

  // ---- Controles ----
  const gPart = grupo(panel, "Partícula");
  const sPart = selector(gPart, {
    etiqueta: "Tipo",
    opciones: [...Object.entries(PARTICULAS).map(([valor, p]) => ({ valor, texto: p.nombre })), { valor: "otra", texto: "Otra (escribe su masa en reposo)" }],
    valor: Object.keys(PARTICULAS).find((k) => PARTICULAS[k].m === m0) ?? "otra",
    alCambiar: (k) => { if (k !== "otra") { m0 = PARTICULAS[k].m; cM.valor = m0; recalcular(); } },
  });
  const cM = campoCientifico(gPart, { etiqueta: "Masa en reposo, m₀", valor: m0, unidades: [{ texto: "kg", factor: 1 }], alCambiar: (v) => { m0 = v; sPart.valor = "otra"; recalcular(); } });

  const gDato = grupo(panel, "Dato del enunciado");
  selector(gDato, {
    etiqueta: "Qué se conoce",
    opciones: [{ valor: "Ec", texto: "La energía cinética" }, { valor: "v", texto: "La velocidad (como fracción de c)" }],
    valor: dato,
    alCambiar: (v) => { dato = v; mostrar(); recalcular(); },
  });
  const cEc = campoCientifico(gDato, {
    etiqueta: "Energía cinética", valor: Ec,
    unidades: [{ texto: "J", factor: 1 }, { texto: "eV", factor: F.E }, { texto: "MeV", factor: MeV }, { texto: "GeV", factor: 1e3 * MeV }],
    alCambiar: (v) => { Ec = v; recalcular(); },
  });
  if (url.Ec === undefined) cEc.ponerUnidad(3, Ec);
  const dBeta = deslizador(gDato, {
    etiqueta: "Velocidad, v/c", min: 0.01, max: 0.999, paso: 0.001, valor: beta,
    formato: (v) => `${num(v, 3)} c`,
    marcas: [{ texto: "0,6 c", valor: 0.6 }, { texto: "0,75 c", valor: 0.75 }, { texto: "0,8 c", valor: 0.8 }, { texto: "0,99 c", valor: 0.99 }],
    alCambiar: (v) => { beta = v; recalcular(); },
  });

  const gRes = grupo(panel, "Resultados");
  const poner = lecturas(gRes, [
    ["gamma", "Factor de Lorentz, γ"],
    ["v", "Velocidad"],
    ["m", "Masa relativista, γ·m₀"],
    ["E0", "Energía en reposo, m₀c²"],
    ["Ec", "Energía cinética"],
    ["Et", "Energía total"],
    ["p", "Cantidad de movimiento"],
  ]);
  const gComp = grupo(panel, "Si se usara la fórmula clásica");
  const ponerC = lecturas(gComp, [["Ec", "½·m₀·v² daría"], ["error", "Se quedaría corta en un"], ["vc", "Con esa Ec, la velocidad clásica sería"]]);
  const gTiempo = grupo(panel, "Tiempo y longitud");
  const ponerT = lecturas(gTiempo, [["t", "Un intervalo propio de 1 s dura"], ["L", "Una longitud propia de 1 m mide"]]);
  nota(gTiempo, "Medidos por un observador respecto al que la partícula se mueve.");

  function mostrar() {
    cEc.caja.hidden = dato !== "Ec";
    dBeta.refrescar();
    gDato.querySelector(".sim__control").hidden = dato !== "v";
  }

  // ---- Cálculo ----
  const energia = (J) => `${medida(J, "J")} = ${medida(J / MeV, "MeV")}`;
  function recalcular() {
    if (!(m0 > 0)) { estado.textContent = "La masa en reposo debe ser positiva."; return; }
    if (dato === "Ec") {
      if (!(Ec > 0)) { estado.textContent = "La energía cinética debe ser positiva."; return; }
      beta = F.betaDeEnergiaCinetica(m0, Ec);
    }
    r = F.relativista(m0, beta);
    poner("gamma", num(r.gamma, 3));
    poner("v", `${num(beta, 3)} c = ${medida(r.v, "m/s")}`);
    poner("m", medida(r.m, "kg"));
    poner("E0", energia(r.E0));
    poner("Ec", energia(r.Ec));
    poner("Et", energia(r.Etotal));
    poner("p", medida(r.p, "kg·m/s"));
    ponerC("Ec", energia(r.EcClasica));
    ponerC("error", `${num((1 - r.EcClasica / r.Ec) * 100, 1)} %`);
    const vClasica = Math.sqrt((2 * r.Ec) / m0);
    ponerC("vc", `${medida(vClasica, "m/s")}${vClasica > F.C ? " (¡mayor que c!)" : ""}`);
    ponerT("t", `${num(r.gamma, 3)} s`);
    ponerT("L", `${num(1 / r.gamma, 3)} m`);
    estado.textContent = `γ = ${num(r.gamma, 2)} · va al ${num(beta * 100, 1)} % de la velocidad de la luz`;
    dibujar();
  }

  // ---- Dibujo ----
  function dibujar() {
    const { ancho, alto } = lienzo;
    ctx.fillStyle = TINTA.fondo;
    ctx.fillRect(0, 0, ancho, alto);
    const g = { x: 46, y: 56, ancho: ancho - 62, alto: alto - 130 };
    const yMax = Math.max(2, Math.min(8, Math.ceil((r.gamma - 1) * 1.3)));
    const a = ejes(ctx, { ...g, xr: [0, 1], yr: [0, yMax], xlab: "v / c", ylab: "Ec / (m₀c²)", titulo: "Energía cinética frente a velocidad" });
    const rel = [];
    const cla = [];
    for (let i = 0; i <= 300; i++) {
      const b = Math.min(0.9995, i / 300);
      rel.push([a.X(b), a.Y(F.gamma(b) - 1)]);
      cla.push([a.X(b), a.Y(0.5 * b * b)]);
    }
    trazar(ctx, cla, TINTA.d, { recorte: g, discontinua: true });
    trazar(ctx, rel, TINTA.a, { recorte: g });
    trazar(ctx, [[a.X(1), g.y], [a.X(1), g.y + g.alto]], TINTA.e, { grosor: 1.5 });
    rotulo(ctx, "v = c", a.X(1) - 6, g.y + g.alto - 10, { alinear: "right", color: TINTA.e, tam: 11 });
    const yPunto = Math.min(yMax, r.gamma - 1);
    punto(ctx, a.X(beta), a.Y(yPunto), TINTA.b, 6);
    punto(ctx, a.X(beta), a.Y(0.5 * beta * beta), TINTA.d, 4);
    rotulo(ctx, "— relativista", g.x, alto - 30, { color: TINTA.a, tam: 11 });
    rotulo(ctx, "- - clásica, ½·m₀·v²", g.x, alto - 14, { color: TINTA.d, tam: 11 });
    rotulo(ctx, "Ninguna partícula con masa alcanza v = c", ancho - 14, alto - 14, { alinear: "right", color: TINTA.suave, tam: 11 });
  }
  lienzo.alRedimensionar = () => dibujar();

  mostrar();
  recalcular();
  return { get resultado() { return r; } };
}
