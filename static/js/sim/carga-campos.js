// Simulación: carga que se mueve en un campo magnético uniforme, con o sin
// campo eléctrico perpendicular (selector de velocidades, espectrómetro).
// La física está en fisica-lorentz.js.

import * as F from "./fisica-lorentz.js";
import {
  TINTA, bucle, campoCientifico, campoNumero, crearLienzo, estructura, flecha, grupo,
  lecturas, medida, nota, num, parametrosURL, punto, rotulo, selector, trazar,
} from "./kit.js";

export function montar(contenedor) {
  const { marco, estado, panel } = estructura(contenedor);
  const lienzo = crearLienzo(marco, { aspecto: 0.9, descripcion: "Trayectoria de la carga vista desde arriba, con los campos y las fuerzas que actúan sobre ella" });
  const { ctx } = lienzo;

  // ---- Estado: por defecto, el ion Ca²⁺ del espectrómetro (extraordinaria 2025) ----
  const url = parametrosURL();
  let m = url.m ?? 40 * F.U;
  let cargas = url.q ?? 2;              // en unidades de e, con signo
  let v = url.v ?? 2.4e5;
  let B = url.B ?? 1.5;
  let entra = url.entra !== 0;
  let E = url.E ?? 0;                   // V/m, hacia +y si es positivo
  let dV = url.dV ?? 1000;
  let puntos = [];
  let caja = null;
  let reloj = 0;
  let datos = null;

  // ---- Controles ----
  const gPart = grupo(panel, "Partícula");
  const sPart = selector(gPart, {
    etiqueta: "Tipo",
    opciones: [
      ...Object.entries(F.PARTICULAS).map(([valor, p]) => ({ valor, texto: p.nombre })),
      { valor: "otra", texto: "Otra (masa en u y carga en e)" },
    ],
    valor: "otra",
    alCambiar: (clave) => {
      if (clave === "otra") return;
      m = F.PARTICULAS[clave].m;
      cargas = F.PARTICULAS[clave].q / F.E_CARGA;
      cM.valor = m / F.U;
      cQ.valor = cargas;
      recalcular();
    },
  });
  const cM = campoNumero(gPart, { etiqueta: "Masa", valor: m / F.U, unidad: "u", min: 0, alCambiar: (x) => { m = x * F.U; sPart.valor = "otra"; recalcular(); } });
  const cQ = campoNumero(gPart, { etiqueta: "Carga (con signo)", valor: cargas, unidad: "e", alCambiar: (x) => { cargas = x; sPart.valor = "otra"; recalcular(); } });
  campoCientifico(gPart, { etiqueta: "Velocidad, v", valor: v, unidades: [{ texto: "m/s", factor: 1 }, { texto: "km/s", factor: 1e3 }], alCambiar: (x) => { v = x; recalcular(); } });

  const gCampos = grupo(panel, "Campos");
  campoCientifico(gCampos, { etiqueta: "Campo magnético, B", valor: B, unidades: [{ texto: "T", factor: 1 }, { texto: "mT", factor: 1e-3 }], alCambiar: (x) => { B = x; recalcular(); } });
  selector(gCampos, {
    etiqueta: "Sentido de B",
    opciones: [{ valor: "1", texto: "Entra en el papel (⊗)" }, { valor: "0", texto: "Sale del papel (⊙)" }],
    valor: entra ? "1" : "0",
    alCambiar: (x) => { entra = x === "1"; recalcular(); },
  });
  campoCientifico(gCampos, { etiqueta: "Campo eléctrico, E (hacia arriba si es positivo)", valor: E, unidades: [{ texto: "V/m", factor: 1 }], alCambiar: (x) => { E = x; recalcular(); } });
  nota(gCampos, "La carga entra moviéndose hacia la derecha. Con E = 0 solo actúa el campo magnético.");

  const gRes = grupo(panel, "Con el campo magnético");
  const poner = lecturas(gRes, [
    ["Fm", "Fuerza magnética"],
    ["R", "Radio de la trayectoria"],
    ["T", "Periodo de giro"],
    ["f", "Frecuencia"],
    ["giro", "Se desvía hacia"],
  ]);
  const gSel = grupo(panel, "Con los dos campos");
  const ponerS = lecturas(gSel, [
    ["Fe", "Fuerza eléctrica"],
    ["vsel", "Velocidad que no se desvía, E/B"],
    ["recta", "¿Sigue recta?"],
  ]);
  const gOtros = grupo(panel, "Energía y onda asociada");
  const ponerO = lecturas(gOtros, [["Ec", "Energía cinética"], ["lambda", "Longitud de onda de De Broglie"]]);
  campoCientifico(gOtros, { etiqueta: "Si parte del reposo y se acelera con ΔV", valor: dV, unidades: [{ texto: "V", factor: 1 }, { texto: "kV", factor: 1e3 }], alCambiar: (x) => { dV = x; recalcular(); } });
  const ponerV = lecturas(gOtros, [["v", "Velocidad que alcanza"]]);

  // ---- Cálculo ----
  function recalcular() {
    const q = cargas * F.E_CARGA;
    if (!(m > 0) || !q || !(v > 0)) { datos = null; estado.textContent = "La masa y la velocidad deben ser positivas y la carga no puede ser nula."; dibujar(); return; }
    const Bz = entra ? -B : B;
    const hayB = Math.abs(B) > 0;
    const g = hayB ? F.giro({ m, q, v, B }) : null;
    const f0 = F.fuerza(q, { vx: v, vy: 0 }, { Ey: E, Bz });
    datos = { q, Bz, g, f0 };
    poner("Fm", hayB ? medida(g.fuerza, "N") : "—");
    poner("R", hayB ? medida(g.radio, "m") : "—");
    poner("T", hayB ? medida(g.periodo, "s") : "—");
    poner("f", hayB ? medida(g.frecuencia, "Hz") : "—");
    const magnetica = F.fuerza(q, { vx: v, vy: 0 }, { Bz });
    poner("giro", !hayB ? "—" : magnetica.y > 0 ? "arriba al entrar (gira en sentido antihorario)" : "abajo al entrar (gira en sentido horario)");
    ponerS("Fe", E ? `${medida(Math.abs(q * E), "N")} hacia ${q * E > 0 ? "arriba" : "abajo"}` : "no hay campo eléctrico");
    ponerS("vsel", E && hayB ? medida(F.velocidadSelector(E, B), "m/s") : "—");
    const recta = Math.abs(f0.y) < 1e-6 * Math.max(Math.abs(q * E), Math.abs(q * v * B), 1e-300);
    ponerS("recta", !E ? "—" : recta ? "Sí: las dos fuerzas se compensan" : "No: una fuerza es mayor que la otra");
    ponerO("Ec", `${medida(0.5 * m * v * v, "J")} = ${medida((0.5 * m * v * v) / F.E_CARGA, "eV")}`);
    ponerO("lambda", medida(F.longitudDeBroglie(m, v), "m"));
    ponerV("v", medida(F.velocidadTrasPotencial(m, q, dV), "m/s"));
    estado.innerHTML = recta && E ? "Selector de velocidades: pasa sin desviarse" : hayB ? `Radio de giro: ${medida(g.radio, "m")}` : "Sin campo magnético";

    // Trayectoria: vuelta y media si hay giro; si no, el tramo equivalente.
    const tiempo = hayB ? 1.5 * g.periodo : 3e-6;
    puntos = F.trayectoria({ x: 0, y: 0, vx: v, vy: 0 }, { qm: q / m, Ey: E, Bz }, tiempo, 1500);
    const xs = puntos.map((p) => p[0]);
    const ys = puntos.map((p) => p[1]);
    caja = { x0: Math.min(...xs), x1: Math.max(...xs), y0: Math.min(...ys), y1: Math.max(...ys) };
    reloj = 0;
    dibujar();
  }

  // ---- Dibujo ----
  function dibujar() {
    const { ancho, alto } = lienzo;
    ctx.fillStyle = TINTA.fondo;
    ctx.fillRect(0, 0, ancho, alto);
    if (!datos) return;

    // Campo magnético de fondo
    ctx.strokeStyle = ctx.fillStyle = "rgba(122,170,255,0.45)";
    ctx.lineWidth = 1.2;
    if (B) {
      for (let px = 20; px < ancho; px += 32) {
        for (let py = 52; py < alto - 30; py += 32) {
          if (entra) { ctx.beginPath(); ctx.moveTo(px - 4, py - 4); ctx.lineTo(px + 4, py + 4); ctx.moveTo(px - 4, py + 4); ctx.lineTo(px + 4, py - 4); ctx.stroke(); }
          else { ctx.beginPath(); ctx.arc(px, py, 2.2, 0, 2 * Math.PI); ctx.fill(); }
        }
      }
    }
    if (E) {
      for (let px = 36; px < ancho; px += 64) flecha(ctx, px, E > 0 ? alto - 44 : 60, 0, E > 0 ? -22 : 22, "rgba(255,159,107,0.55)", 1.5);
    }

    // Encuadre con la misma escala en los dos ejes
    const margen = 46;
    const w = Math.max(caja.x1 - caja.x0, 1e-30);
    const h = Math.max(caja.y1 - caja.y0, 1e-30);
    const esc = Math.min((ancho - 2 * margen) / w, (alto - 2 * margen - 30) / h);
    const cx = (caja.x0 + caja.x1) / 2;
    const cy = (caja.y0 + caja.y1) / 2;
    const X = (x) => ancho / 2 + (x - cx) * esc;
    const Y = (y) => alto / 2 + 10 - (y - cy) * esc;

    trazar(ctx, puntos.map(([x, y]) => [X(x), Y(y)]), "rgba(255,209,102,0.35)", { grosor: 1.5 });
    const fase = Number.isFinite(reloj) ? ((reloj % 1) + 1) % 1 : 0;
    const hasta = Math.min(puntos.length - 1, Math.floor(fase * (puntos.length - 1)));
    trazar(ctx, puntos.slice(0, hasta + 1).map(([x, y]) => [X(x), Y(y)]), TINTA.a, { grosor: 2.5 });
    const [px, py] = puntos[hasta];
    const [qx, qy] = puntos[Math.min(puntos.length - 1, hasta + 1)];
    const vel = { vx: (qx - px), vy: (qy - py) };
    const modV = Math.hypot(vel.vx, vel.vy) || 1;
    const u = { x: vel.vx / modV, y: vel.vy / modV };
    flecha(ctx, X(px), Y(py), u.x * 44, -u.y * 44, TINTA.b);
    // Fuerza total en ese punto (dirección)
    const fz = F.fuerza(datos.q, { vx: u.x * v, vy: u.y * v }, { Ey: E, Bz: datos.Bz });
    const modF = Math.hypot(fz.x, fz.y);
    if (modF > 0) flecha(ctx, X(px), Y(py), (fz.x / modF) * 36, -(fz.y / modF) * 36, TINTA.c);
    punto(ctx, X(px), Y(py), "#ffffff", 5.5);
    punto(ctx, X(0), Y(0), TINTA.suave, 3);
    rotulo(ctx, "entrada", X(0) - 6, Y(0) + 14, { color: TINTA.suave, tam: 11, alinear: "right" });

    rotulo(ctx, "— velocidad", 12, alto - 30, { color: TINTA.b, tam: 11 });
    rotulo(ctx, "— fuerza", 12, alto - 14, { color: TINTA.c, tam: 11 });
    rotulo(ctx, `B ${entra ? "entra ⊗" : "sale ⊙"}${E ? " · E en naranja" : ""}`, ancho - 12, alto - 14, { alinear: "right", color: TINTA.d, tam: 11 });
  }
  lienzo.alRedimensionar = () => dibujar();

  const animacion = bucle((dt) => { if (dt > 0) reloj += dt / 6; dibujar(); });
  recalcular();
  if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) animacion.arrancar();
  return { get datos() { return datos; } };
}
