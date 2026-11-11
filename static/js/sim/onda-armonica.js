// Simulación: onda armónica. Se escriben A, T, λ, la fase y el sentido y se ven
// las dos gráficas de los problemas de examen: el perfil y(x) en un instante y
// la oscilación y(t) (o su velocidad) de un punto. Física en fisica-ondas.js.

import * as F from "./fisica-ondas.js";
import {
  TINTA, botones, bucle, campoNumero, casilla, crearLienzo, deslizador, ejes, estructura,
  fraccionPi, grupo, lecturas, medida, nota, num, parametroTexto, parametrosURL, punto,
  rotulo, selector, trazar,
} from "./kit.js";

const DOCEAVO = Math.PI / 12;

export function montar(contenedor) {
  const { marco, estado, panel } = estructura(contenedor);
  const lienzo = crearLienzo(marco, {
    aspecto: 1.12,
    descripcion: "Arriba, perfil de la onda en el instante actual; abajo, oscilación del punto elegido frente al tiempo",
  });
  const { ctx } = lienzo;

  // ---- Estado (por defecto, la onda de la extraordinaria de 2026) ----
  const url = parametrosURL();
  const p = {
    A: url.A ?? 3,
    T: url.T ?? 1,
    lambda: url.L ?? 4,
    fase: url.fase ?? (3 * Math.PI) / 2,
    sentido: url.sentido === -1 ? -1 : 1,
    coseno: parametroTexto("f") === "cos",
  };
  let x0 = url.x0 ?? 1;
  let t = 0;
  let verVelocidad = parametroTexto("ver") === "v";
  let o = F.onda(p);

  // ---- Controles ----
  const gOnda = grupo(panel, "Tu onda");
  const ecuacion = document.createElement("p");
  ecuacion.className = "sim__ecuacion";
  gOnda.append(ecuacion);
  campoNumero(gOnda, { etiqueta: "Amplitud, A", valor: p.A, unidad: "(la unidad del enunciado)", min: 0, alCambiar: (v) => { p.A = v; recalcular(); } });
  campoNumero(gOnda, { etiqueta: "Periodo, T", valor: p.T, unidad: "s", min: 0, alCambiar: (v) => { p.T = v; recalcular(); } });
  campoNumero(gOnda, { etiqueta: "Longitud de onda, λ", valor: p.lambda, unidad: "m", min: 0, alCambiar: (v) => { p.lambda = v; recalcular(); } });
  deslizador(gOnda, {
    etiqueta: "Fase inicial, φ₀",
    min: 0, max: 24, paso: 1, valor: Math.round((((p.fase % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI)) / DOCEAVO),
    formato: (n) => `${fraccionPi(n * DOCEAVO)} rad`,
    alCambiar: (n) => { p.fase = n * DOCEAVO; recalcular(); },
  });
  selector(gOnda, {
    etiqueta: "Sentido de propagación",
    opciones: [{ valor: "1", texto: "Hacia las x positivas (ωt − kx)" }, { valor: "-1", texto: "Hacia las x negativas (ωt + kx)" }],
    valor: String(p.sentido),
    alCambiar: (v) => { p.sentido = Number(v); recalcular(); },
  });
  selector(gOnda, {
    etiqueta: "Función",
    opciones: [{ valor: "sen", texto: "Seno" }, { valor: "cos", texto: "Coseno" }],
    valor: p.coseno ? "cos" : "sen",
    alCambiar: (v) => { p.coseno = v === "cos"; recalcular(); },
  });

  const gPunto = grupo(panel, "Punto que se observa");
  campoNumero(gPunto, { etiqueta: "Posición del punto, x", valor: x0, unidad: "m", alCambiar: (v) => { x0 = v; actualizar(); } });
  casilla(gPunto, {
    etiqueta: "Ver su velocidad de oscilación en vez de su elongación",
    valor: verVelocidad,
    alCambiar: (v) => { verVelocidad = v; dibujar(); },
  });
  const boton = botones(gPunto);
  const bPausa = boton("Pausa", () => (animacion.activo ? pausar() : seguir()), { suave: true });
  boton("Volver a t = 0", () => { t = 0; actualizar(); }, { suave: true });

  const gAhora = grupo(panel, "En ese punto, ahora");
  const ponerAhora = lecturas(gAhora, [
    ["t", "Instante, t"],
    ["y", "Elongación, y"],
    ["v", "Velocidad de oscilación"],
  ]);
  nota(gAhora, "Pon t = 0 y la posición del dato del enunciado: la elongación y el signo de la velocidad deben coincidir con los que te dan.");

  const gMagnitudes = grupo(panel, "Magnitudes de la onda");
  const poner = lecturas(gMagnitudes, [
    ["w", "Frecuencia angular, ω"],
    ["k", "Número de onda, k"],
    ["f", "Frecuencia, f"],
    ["v", "Velocidad de propagación"],
    ["vmax", "Velocidad máxima de oscilación"],
    ["amax", "Aceleración máxima"],
  ]);

  // ---- Cálculo ----
  const valido = () => p.A > 0 && p.T > 0 && p.lambda > 0;

  function textoEcuacion() {
    const fase = fraccionPi(p.fase) ?? num(p.fase, 2);
    const mas = fase === "0" ? "" : ` + ${fase}`;
    return `y(x, t) = ${num(p.A, p.A < 10 ? 2 : 0)} · ${p.coseno ? "cos" : "sen"}(${medida(o.w, "")}·t ${p.sentido > 0 ? "−" : "+"} ${medida(o.k, "")}·x${mas})`;
  }

  function recalcular() {
    if (!valido()) {
      estado.innerHTML = "La amplitud, el periodo y la longitud de onda deben ser positivos.";
      return;
    }
    o = F.onda(p);
    ecuacion.textContent = textoEcuacion();
    estado.innerHTML = `Avanza hacia las x ${p.sentido > 0 ? "positivas" : "negativas"} a ${medida(o.v, "m/s")}`;
    poner("w", `${medida(o.w, "rad/s")}`);
    poner("k", `${medida(o.k, "rad/m")}`);
    poner("f", medida(o.f, "Hz"));
    poner("v", medida(o.v, "m/s"));
    poner("vmax", `${medida(o.vMax, "")} (unidad de A)/s`);
    poner("amax", `${medida(o.aMax, "")} (unidad de A)/s²`);
    actualizar();
  }

  function actualizar() {
    if (!valido()) return;
    const y = o.y(x0, t);
    const v = o.vy(x0, t);
    ponerAhora("t", `${num(t, 3)} s`);
    ponerAhora("y", medida(Math.abs(y) < 1e-9 * p.A ? 0 : y, ""));
    const quieto = Math.abs(v) < 1e-9 * o.vMax;
    ponerAhora("v", quieto ? "0 (en un extremo)" : `${medida(v, "")} · ${v > 0 ? "sube" : "baja"}`);
    dibujar();
  }

  // ---- Dibujo ----
  function dibujar() {
    const { ancho, alto } = lienzo;
    ctx.fillStyle = TINTA.fondo;
    ctx.fillRect(0, 0, ancho, alto);
    if (!valido()) return;

    const izq = 44;
    const w = ancho - izq - 14;
    const h = (alto - 150) / 2;
    const yr = [-1.25 * p.A, 1.25 * p.A];

    // Arriba: perfil y(x) en el instante actual
    const xMax = Math.max(1.75 * p.lambda, x0 * 1.15);
    const sup = { x: izq, y: 48, ancho: w, alto: h };
    const a1 = ejes(ctx, { ...sup, xr: [0, xMax], yr, xlab: "x (m)", ylab: "y", titulo: `Perfil en t = ${num(t, 3)} s` });
    const perfil = [];
    for (let i = 0; i <= 240; i++) {
      const x = (xMax * i) / 240;
      perfil.push([a1.X(x), a1.Y(o.y(x, t))]);
    }
    trazar(ctx, perfil, TINTA.a, { recorte: sup });
    if (x0 >= 0 && x0 <= xMax) {
      trazar(ctx, [[a1.X(x0), sup.y], [a1.X(x0), sup.y + h]], TINTA.suave, { grosor: 1, discontinua: true });
      punto(ctx, a1.X(x0), a1.Y(o.y(x0, t)), TINTA.b);
    }

    // Abajo: oscilación del punto elegido frente al tiempo
    const tMax = 2.5 * p.T;
    const inf = { x: izq, y: sup.y + h + 62, ancho: w, alto: h };
    const escala = verVelocidad ? o.vMax : p.A;
    const a2 = ejes(ctx, {
      ...inf, xr: [0, tMax], yr: [-1.25 * escala, 1.25 * escala], xlab: "t (s)",
      ylab: verVelocidad ? "v" : "y",
      titulo: `${verVelocidad ? "Velocidad" : "Elongación"} del punto x = ${num(x0, 2)} m`,
    });
    const serie = [];
    for (let i = 0; i <= 240; i++) {
      const tt = (tMax * i) / 240;
      serie.push([a2.X(tt), a2.Y(verVelocidad ? o.vy(x0, tt) : o.y(x0, tt))]);
    }
    trazar(ctx, serie, verVelocidad ? TINTA.c : TINTA.b, { recorte: inf });
    const tVisible = t % tMax;
    trazar(ctx, [[a2.X(tVisible), inf.y], [a2.X(tVisible), inf.y + h]], TINTA.suave, { grosor: 1, discontinua: true });
    punto(ctx, a2.X(tVisible), a2.Y(verVelocidad ? o.vy(x0, t) : o.y(x0, t)), verVelocidad ? TINTA.c : TINTA.b);
    rotulo(ctx, "El punto verde es el mismo en las dos gráficas", izq, alto - 12, { color: TINTA.suave, tam: 11 });
  }
  lienzo.alRedimensionar = () => dibujar();

  // ---- Animación: un periodo dura unos 5 segundos en pantalla ----
  const animacion = bucle((dt) => {
    t += (dt * p.T) / 5;
    actualizar();
  });
  function pausar() { animacion.parar(); bPausa.textContent = "Seguir"; }
  function seguir() { animacion.arrancar(); bPausa.textContent = "Pausa"; }

  recalcular();
  // Empieza en pausa en t = 0, que es la «foto» que dan los enunciados.
  pausar();

  return { get onda() { return o; }, get tiempo() { return t; }, pausar, seguir };
}
