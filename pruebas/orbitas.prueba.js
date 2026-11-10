// Compara la física de las simulaciones de órbitas con la referencia de Python.

import * as F from "../static/js/sim/fisica-orbitas.js";

const cerca = (a, b, tol) => Math.abs(a - b) <= tol * Math.max(Math.abs(a), Math.abs(b), 1e-300);

export async function probar() {
  const ref = await (await fetch("orbitas.ref.json")).json();
  const res = [];
  const anotar = (nombre, ok, detalle = "") => res.push({ nombre, ok, detalle });
  const comparar = (nombre, sim, esperado, tol) =>
    anotar(nombre, cerca(sim, esperado, tol), `sim ${sim}, ref ${esperado}`);

  anotar("constante G igual a la referencia", F.G === ref.G);

  // ---- Órbitas circulares ----
  for (const c of ref.circulares) {
    const id = `circular M=${c.M.toExponential(2)}, r=${c.r.toExponential(3)}`;
    const o = F.orbitaCircular(c);
    for (const clave of ["v", "T", "g", "Ec", "Ep", "Em", "vEscape", "L"]) {
      comparar(`${id}: ${clave}`, o[clave], c[clave], 1e-10);
    }
    comparar(`${id}: energía para escapar`, o.energiaEscape, -c.Em, 1e-10);
    comparar(`${id}: radio a partir del periodo`, F.radioDesdePeriodo(c.M, c.T), c.r, 1e-10);
    comparar(`${id}: Ec = −Ep/2`, o.Ec, -o.Ep / 2, 1e-12);
  }

  // Superficie y puesta en órbita, con la Tierra.
  {
    const { M, R } = F.ASTROS.tierra;
    const s = F.superficie({ M, R, m: 1000 });
    comparar("Tierra: g en la superficie", s.g, (ref.G * M) / R ** 2, 1e-12);
    comparar("Tierra: velocidad de escape", s.vEscape, Math.sqrt((2 * ref.G * M) / R), 1e-12);
    anotar("Tierra: g cerca de 9,8 m/s²", Math.abs(s.g - 9.81) < 0.05, `g = ${s.g}`);
    anotar("Tierra: escape cerca de 11,2 km/s", Math.abs(s.vEscape - 11.2e3) < 100, `v = ${s.vEscape}`);
    const r = R + 600e3;
    const directa = ref.G * M * 1000 * (1 / R - 1 / (2 * r));
    comparar("Tierra: energía para poner en órbita", F.energiaPuestaEnOrbita({ M, R, r, m: 1000 }), directa, 1e-10);
  }

  // ---- Órbitas elípticas ----
  for (const c of ref.elipticas) {
    const id = `elipse a=${c.a.toExponential(3)}, e=${c.e}`;
    const el = F.elipse(c);
    for (const clave of ["rp", "ra", "vp", "va", "T"]) comparar(`${id}: ${clave}`, el[clave], c[clave], 1e-10);
    comparar(`${id}: energía por kg`, el.Em, c.Em_por_kg, 1e-9);
    comparar(`${id}: rp·vp = ra·va`, el.rp * el.vp, el.ra * el.va, 1e-12);

    let tPrevio = 0;
    let areaPrevia = 0;
    for (const s of c.estados) {
      const e = F.estadoEliptico(c, s.t);
      const fraccion = (s.t / c.T).toFixed(2);
      const errPos = Math.hypot(e.x - s.x, e.y - s.y) / Math.hypot(s.x, s.y);
      const errVel = Math.hypot(e.vx - s.vx, e.vy - s.vy) / Math.hypot(s.vx, s.vy);
      anotar(`${id}: posición en t = ${fraccion} T`, errPos < 1e-7, `error relativo ${errPos.toExponential(2)}`);
      anotar(`${id}: velocidad en t = ${fraccion} T`, errVel < 1e-7, `error relativo ${errVel.toExponential(2)}`);
      // Momento angular: r·v·sen(fi) es el mismo en todos los puntos.
      comparar(`${id}: r·v·sen φ en t = ${fraccion} T`, e.r * e.v * e.senFi, el.h, 1e-10);
      // Área barrida en el tramo, medida sobre la trayectoria.
      const area = F.areaBarrida(c, tPrevio, s.t, 2000);
      comparar(`${id}: área barrida hasta t = ${fraccion} T`, area, s.area - areaPrevia, 2e-5);
      // Ley de las áreas: el área es proporcional al tiempo empleado.
      comparar(`${id}: área / tiempo en ese tramo`, area / (s.t - tPrevio), el.velocidadAreolar, 2e-5);
      tPrevio = s.t;
      areaPrevia = s.area;
    }
    // Muchos triángulos: en órbitas muy excéntricas el cuerpo pasa el
    // pericentro tan rápido que con pocos el polígono se queda corto.
    comparar(`${id}: área de una vuelta completa`, F.areaBarrida(c, 0, c.T, 40000), el.area, 2e-5);
  }

  // ---- Resultados del modelo oficial 2026-2027 (tres cifras) ----
  {
    const of = ref.oficial["2A"];
    const o = F.orbitaCircular(of);
    comparar("modelo 2027, 2.A: velocidad orbital", o.v, of.v, 5e-3);
    comparar("modelo 2027, 2.A: periodo", o.T, of.T, 5e-3);
    comparar("modelo 2027, 2.A: energía mecánica", o.Em, of.Em, 5e-3);
  }
  {
    const of = ref.oficial["2B"];
    const a = F.radioDesdePeriodo(of.M, of.T);
    const el = F.elipse({ M: of.M, a, e: of.e });
    comparar("modelo 2027, 2.B: semieje mayor", a, of.a, 1e-2);
    comparar("modelo 2027, 2.B: perihelio", el.rp, of.rp, 5e-3);
    comparar("modelo 2027, 2.B: afelio", el.ra, of.ra, 5e-3);
    comparar("modelo 2027, 2.B: velocidad en el afelio", el.va, of.va, 5e-3);
    comparar("modelo 2027, 2.B: velocidad en el perihelio", el.vp, of.vp, 5e-3);
  }
  return res;
}
