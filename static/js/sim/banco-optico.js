// Simulación: banco óptico. Una lente, dos lentes o un espejo esférico, con el
// trazado de los rayos principales y los resultados con el criterio DIN.
// La física está en fisica-optica.js.

import * as F from "./fisica-optica.js";
import {
  TINTA, arrastre, campoNumero, crearLienzo, estructura, flecha, grupo, lecturas, nota,
  num, parametroTexto, parametrosURL, punto, rotulo, selector, trazar,
} from "./kit.js";

const COLOR = { objeto: "#ffffff", imagen: TINTA.a, intermedia: TINTA.suave, rayos: [TINTA.b, TINTA.c, TINTA.d], elemento: TINTA.d };

export function montar(contenedor) {
  const { marco, estado, panel } = estructura(contenedor);
  const lienzo = crearLienzo(marco, { aspecto: 0.8, descripcion: "Eje óptico con el objeto, la lente o el espejo, los rayos principales y la imagen" });
  const { ctx } = lienzo;

  // ---- Estado: por defecto, lente de 8 cm con el objeto a 10 cm (modelo 2027) ----
  const url = parametrosURL();
  let tipo = ["lente", "dos", "espejo"].includes(parametroTexto("tipo")) ? parametroTexto("tipo") : "lente";
  let f1 = url.f ?? (tipo === "espejo" ? -30 : tipo === "dos" ? 15 : 8);
  let d = url.s !== undefined ? Math.abs(url.s) : tipo === "espejo" ? 80 : tipo === "dos" ? 30 : 10;
  let y = url.y ?? (tipo === "dos" ? 10 : 5);
  let sep = url.d ?? 60;
  let f2 = url.f2 ?? -20;
  let vista = null; // escala del dibujo, para el arrastre

  // ---- Controles ----
  const gMontaje = grupo(panel, "Montaje");
  selector(gMontaje, {
    etiqueta: "Sistema óptico",
    opciones: [
      { valor: "lente", texto: "Una lente delgada" },
      { valor: "dos", texto: "Dos lentes delgadas" },
      { valor: "espejo", texto: "Un espejo esférico" },
    ],
    valor: tipo,
    alCambiar: (v) => {
      tipo = v;
      // Cada sistema arranca con un montaje de examen.
      [f1, d, y] = { lente: [8, 10, 5], dos: [15, 30, 10], espejo: [-30, 80, 5] }[tipo];
      cF1.valor = f1; cD.valor = d; cY.valor = y;
      mostrar();
      recalcular();
    },
  });
  const cF1 = campoNumero(gMontaje, { etiqueta: "Distancia focal, f′", valor: f1, unidad: "cm", alCambiar: (v) => { f1 = v; recalcular(); } });
  const ayudaF = nota(gMontaje, "");
  const cD = campoNumero(gMontaje, { etiqueta: "Distancia del objeto (valor positivo)", valor: d, unidad: "cm", min: 0, alCambiar: (v) => { d = v; recalcular(); } });
  const cY = campoNumero(gMontaje, { etiqueta: "Altura del objeto, y", valor: y, unidad: "cm", alCambiar: (v) => { y = v; recalcular(); } });
  const cSep = campoNumero(gMontaje, { etiqueta: "Separación entre las lentes", valor: sep, unidad: "cm", min: 0, alCambiar: (v) => { sep = v; recalcular(); } });
  const cF2 = campoNumero(gMontaje, { etiqueta: "Focal de la segunda lente, f′₂", valor: f2, unidad: "cm", alCambiar: (v) => { f2 = v; recalcular(); } });
  nota(gMontaje, "También puedes arrastrar el objeto sobre el dibujo.");

  const gRes = grupo(panel, "Imagen");
  const poner = lecturas(gRes, [
    ["s", "Posición del objeto, s"],
    ["sIm", "Posición de la imagen, s′"],
    ["M", "Aumento lateral, M"],
    ["yIm", "Tamaño de la imagen, y′"],
    ["como", "Es"],
  ]);
  const gDos = grupo(panel, "Paso intermedio (dos lentes)");
  const ponerDos = lecturas(gDos, [
    ["s1", "Imagen de la lente 1, s′₁"],
    ["s2", "Objeto para la lente 2, s₂"],
    ["m1", "Aumento de la lente 1"],
    ["m2", "Aumento de la lente 2"],
  ]);

  function mostrar() {
    cSep.caja.hidden = cF2.caja.hidden = gDos.hidden = tipo !== "dos";
    cF1.caja.querySelector("label").textContent = tipo === "espejo" ? "Distancia focal, f = R/2" : tipo === "dos" ? "Focal de la primera lente, f′₁" : "Distancia focal, f′";
    ayudaF.textContent = tipo === "espejo"
      ? "Negativa: espejo cóncavo. Positiva: convexo."
      : "Positiva: lente convergente. Negativa: divergente.";
  }

  // ---- Cálculo ----
  let res = null;
  function recalcular() {
    const s = -d;
    if (!(d > 0) || !f1 || (tipo === "dos" && (!f2 || !(sep > 0)))) {
      res = null;
      estado.innerHTML = "Revisa los datos: las focales no pueden ser cero y las distancias deben ser positivas.";
      dibujar();
      return;
    }
    if (tipo === "lente") {
      const r = F.lente(s, f1);
      res = { final: { x: r.sIm, M: r.M }, texto: F.naturaleza(r.sIm, r.M) };
    } else if (tipo === "espejo") {
      const r = F.espejo(s, f1);
      res = { final: { x: r.sIm, M: r.M }, texto: F.naturaleza(r.sIm, r.M, true) };
    } else {
      const r = F.dosLentes(s, f1, sep, f2);
      res = {
        intermedia: r.primera.enInfinito ? null : { x: r.primera.sIm, M: r.primera.M },
        final: { x: Number.isFinite(r.segunda.sIm) ? sep + r.segunda.sIm : Infinity, M: r.M, s2Im: r.segunda.sIm },
        texto: F.naturaleza(r.segunda.sIm, r.M),
        r,
      };
      ponerDos("s1", r.primera.enInfinito ? "∞" : `${num(r.primera.sIm, 2)} cm`);
      ponerDos("s2", Number.isFinite(r.s2) ? `${num(r.s2, 2)} cm` : "−∞");
      ponerDos("m1", r.primera.enInfinito ? "—" : num(r.primera.M, 3));
      ponerDos("m2", Number.isFinite(r.segunda.M) ? num(r.segunda.M, 3) : "—");
    }
    const sIm = tipo === "dos" ? res.final.s2Im : res.final.x;
    poner("s", `${num(s, 2)} cm`);
    poner("sIm", Number.isFinite(sIm) ? `${num(sIm, 2)} cm${tipo === "dos" ? " (desde la lente 2)" : ""}` : "∞");
    poner("M", Number.isFinite(res.final.M) ? num(res.final.M, 3) : "∞");
    poner("yIm", Number.isFinite(res.final.M) ? `${num(res.final.M * y, 2)} cm` : "—");
    poner("como", res.texto);
    estado.innerHTML = `Imagen ${res.texto}`;
    dibujar();
  }

  // ---- Dibujo ----
  function dibujar() {
    const { ancho, alto } = lienzo;
    ctx.fillStyle = TINTA.fondo;
    ctx.fillRect(0, 0, ancho, alto);
    if (!res) return;
    const s = -d;
    const esEspejo = tipo === "espejo";
    const xElem2 = tipo === "dos" ? sep : null;

    // Encuadre horizontal: objeto, focos, elementos e imágenes que no se vayan muy lejos.
    const base = Math.max(d, Math.abs(f1) * 2, tipo === "dos" ? sep + Math.abs(f2) : 0);
    const limite = 3 * base;
    const xs = [s, -Math.abs(f1), Math.abs(f1), 0];
    if (esEspejo) xs.push(2 * f1);
    if (tipo === "dos") xs.push(sep, sep - Math.abs(f2), sep + Math.abs(f2));
    for (const im of [res.intermedia, res.final]) if (im && Number.isFinite(im.x) && Math.abs(im.x) <= limite) xs.push(im.x);
    let xMin = Math.min(...xs);
    let xMax = Math.max(...xs);
    if (esEspejo) xMax = Math.max(xMax, 0.25 * base);
    const holgura = 0.08 * (xMax - xMin);
    xMin -= holgura; xMax += holgura;

    // Encuadre vertical: objeto e imágenes visibles.
    const alturas = [Math.abs(y)];
    for (const im of [res.intermedia, res.final]) {
      if (im && Number.isFinite(im.M) && Number.isFinite(im.x) && Math.abs(im.x) <= limite) alturas.push(Math.abs(im.M * y));
    }
    const yMax = Math.min(Math.max(...alturas), 8 * Math.abs(y)) * 1.35 || 1;

    const izq = 12, der = ancho - 12, sup = 62, inf = alto - 34;
    const eje = (sup + inf) / 2;
    const X = (v) => izq + ((v - xMin) / (xMax - xMin)) * (der - izq);
    const Y = (v) => eje - (v / yMax) * ((inf - sup) / 2);
    vista = { X, xMin, xMax, izq, der, eje };
    const marcoRecorte = { x: 0, y: sup - 8, ancho, alto: inf - sup + 16 };

    trazar(ctx, [[izq, eje], [der, eje]], TINTA.eje, { grosor: 1 });

    // Elementos
    const dibujarLente = (x, f, nombre) => {
      const convergente = f > 0;
      flechaDoble(X(x), sup + 6, inf - 6, convergente);
      rotulo(ctx, nombre, X(x), sup - 12, { color: COLOR.elemento, alinear: "center", tam: 11 });
      for (const [xf, t] of [[x - f, "F"], [x + f, "F′"]]) {
        punto(ctx, X(xf), eje, TINTA.texto, 2.5);
        rotulo(ctx, t, X(xf), eje + 12, { alinear: "center", tam: 11, color: TINTA.suave });
      }
    };
    const flechaDoble = (px, y1, y2, convergente) => {
      trazar(ctx, [[px, y1], [px, y2]], COLOR.elemento, { grosor: 2.5 });
      const k = convergente ? 1 : -1;
      trazar(ctx, [[px - 6, y1 + 8 * k], [px, y1], [px + 6, y1 + 8 * k]], COLOR.elemento, { grosor: 2.5 });
      trazar(ctx, [[px - 6, y2 - 8 * k], [px, y2], [px + 6, y2 - 8 * k]], COLOR.elemento, { grosor: 2.5 });
    };
    if (esEspejo) {
      const comba = f1 < 0 ? 10 : -10; // cóncavo: los extremos se adelantan hacia el objeto
      ctx.beginPath();
      ctx.moveTo(X(0) - comba, sup + 6);
      ctx.quadraticCurveTo(X(0) + comba, eje, X(0) - comba, inf - 6);
      ctx.strokeStyle = COLOR.elemento; ctx.lineWidth = 3; ctx.stroke();
      for (const [xf, t] of [[f1, "F"], [2 * f1, "C"]]) {
        punto(ctx, X(xf), eje, TINTA.texto, 2.5);
        rotulo(ctx, t, X(xf), eje + 12, { alinear: "center", tam: 11, color: TINTA.suave });
      }
    } else {
      dibujarLente(0, f1, tipo === "dos" ? "lente 1" : f1 > 0 ? "convergente" : "divergente");
      if (tipo === "dos") dibujarLente(sep, f2, "lente 2");
    }

    // Rayos
    const principales = esEspejo ? F.rayosPrincipalesEspejo(s, y, f1) : F.rayosPrincipalesLente(s, y, f1);
    principales.forEach((rayo, i) => {
      const color = COLOR.rayos[i % 3];
      const h = F.alturaEnElemento(s, y, rayo.p);
      if (Math.abs(h) > 3 * yMax) return; // el rayo no pasa por el elemento en el dibujo
      trazar(ctx, [[X(s), Y(y)], [X(0), Y(h)]], color, { grosor: 1.6, recorte: marcoRecorte });
      if (esEspejo) {
        const q = F.tras_espejo(h, rayo.p, f1);
        trazar(ctx, [[X(0), Y(h)], [X(xMin), Y(h + q * xMin)]], color, { grosor: 1.6, recorte: marcoRecorte });
        if (res.final.x > 0 && Number.isFinite(res.final.x)) {
          trazar(ctx, [[X(0), Y(h)], [X(res.final.x), Y(h + q * res.final.x)]], color, { grosor: 1.2, discontinua: true, recorte: marcoRecorte });
        }
        return;
      }
      const p1 = F.tras_lente(h, rayo.p, f1);
      const fin1 = xElem2 ?? xMax;
      trazar(ctx, [[X(0), Y(h)], [X(fin1), Y(h + p1 * fin1)]], color, { grosor: 1.6, recorte: marcoRecorte });
      const primera = tipo === "dos" ? res.intermedia : res.final;
      if (primera && primera.x < 0 && Math.abs(primera.x) <= limite) {
        trazar(ctx, [[X(0), Y(h)], [X(primera.x), Y(h + p1 * primera.x)]], color, { grosor: 1.2, discontinua: true, recorte: marcoRecorte });
      }
      if (tipo === "dos") {
        const h2 = h + p1 * sep;
        const p2 = F.tras_lente(h2, p1, f2);
        trazar(ctx, [[X(sep), Y(h2)], [X(xMax), Y(h2 + p2 * (xMax - sep))]], color, { grosor: 1.6, recorte: marcoRecorte });
        if (Number.isFinite(res.final.x) && res.final.x < sep && Math.abs(res.final.x) <= limite) {
          trazar(ctx, [[X(sep), Y(h2)], [X(res.final.x), Y(h2 + p2 * (res.final.x - sep))]], color, { grosor: 1.2, discontinua: true, recorte: marcoRecorte });
        }
      }
    });

    // Objeto e imágenes
    const flechaVertical = (x, altura, color, texto, grosor = 3) => {
      if (!Number.isFinite(x) || x < xMin || x > xMax) return;
      const tope = Math.max(sup, Math.min(inf, Y(altura)));
      flecha(ctx, X(x), eje, 0, tope - eje, color, grosor);
      rotulo(ctx, texto, X(x), altura >= 0 ? tope - 10 : tope + 12, { color, alinear: "center", tam: 11, negrita: true });
    };
    flechaVertical(s, y, COLOR.objeto, "objeto");
    if (res.intermedia && Math.abs(res.intermedia.x) <= limite) flechaVertical(res.intermedia.x, res.intermedia.M * y, COLOR.intermedia, "imagen 1", 2);
    if (Number.isFinite(res.final.x) && Number.isFinite(res.final.M) && Math.abs(res.final.x) <= limite) {
      flechaVertical(res.final.x, res.final.M * y, COLOR.imagen, "imagen");
    } else {
      rotulo(ctx, Number.isFinite(res.final.x) ? "La imagen queda fuera del dibujo" : "Imagen en el infinito: los rayos salen paralelos", der, inf + 18, { alinear: "right", color: COLOR.imagen, tam: 11 });
    }
    rotulo(ctx, "Línea continua: rayos · discontinua: prolongaciones", izq, inf + 18, { color: TINTA.suave, tam: 11 });
  }
  lienzo.alRedimensionar = () => dibujar();

  // ---- Arrastre del objeto ----
  arrastre(lienzo.canvas, {
    buscar: (pt) => (vista && Math.abs(pt.x - vista.X(-d)) < 28 ? "objeto" : null),
    mover: (_, pt) => {
      const x = vista.xMin + ((pt.x - vista.izq) / (vista.der - vista.izq)) * (vista.xMax - vista.xMin);
      const nuevo = Math.max(0.5, -x);
      d = Number(nuevo.toPrecision(3));
      cD.valor = d;
      recalcular();
    },
  });
  lienzo.canvas.style.touchAction = "pan-y"; // el arrastre es horizontal: se conserva el desplazamiento de la página

  mostrar();
  recalcular();
  return { get resultado() { return res; } };
}
