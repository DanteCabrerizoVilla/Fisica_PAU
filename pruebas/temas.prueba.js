// Compara la física de las simulaciones de ondas, campos, óptica, inducción y
// física moderna con la referencia de Python (referencia_temas.py).

import * as O from "../static/js/sim/fisica-ondas.js";
import * as Ca from "../static/js/sim/fisica-campos.js";
import * as Op from "../static/js/sim/fisica-optica.js";
import * as In from "../static/js/sim/fisica-induccion.js";
import * as Mo from "../static/js/sim/fisica-moderna.js";
import * as Lo from "../static/js/sim/fisica-lorentz.js";
import * as Or from "../static/js/sim/fisica-orbitas.js";

const cerca = (a, b, tol, abs = 0) => Math.abs(a - b) <= Math.max(abs, tol * Math.max(Math.abs(a), Math.abs(b)));

export async function probar() {
  const ref = await (await fetch("temas.ref.json")).json();
  const res = [];
  const anotar = (nombre, ok, detalle = "") => res.push({ nombre, ok, detalle });
  const comparar = (nombre, sim, esperado, tol, abs = 0) =>
    anotar(nombre, cerca(sim, esperado, tol, abs), `sim ${sim}, ref ${esperado}`);

  // ---- Onda armónica ----
  ref.ondas.forEach((c, i) => {
    const o = O.onda(c);
    comparar(`onda ${i}: velocidad de propagación`, o.v, c.v, 1e-12);
    comparar(`onda ${i}: v = ω/k`, o.w / o.k, c.v, 1e-12);
    for (const p of c.puntos) {
      const id = `onda ${i} en x=${p.x.toFixed(3)}, t=${p.t.toFixed(4)}`;
      comparar(`${id}: y`, o.y(p.x, p.t), p.y, 1e-9, 1e-12 * c.A);
      comparar(`${id}: velocidad de oscilación`, o.vy(p.x, p.t), p.vy, 1e-6, 1e-7 * o.vMax);
      comparar(`${id}: aceleración`, o.ay(p.x, p.t), p.ay, 1e-4, 1e-4 * o.aMax);
      // Las dos fases compatibles con esa elongación reproducen y; una de ellas es la original.
      const fases = O.fasesPosibles(c, p.x, p.t, p.y);
      anotar(`${id}: las fases posibles dan la misma y`, fases.every((f) => cerca(O.onda({ ...c, fase: f.fase }).y(p.x, p.t), p.y, 1e-7, 1e-9 * c.A)));
    }
    // Sentido de propagación: un punto de fase constante avanza con v·sentido.
    const dt = c.T / 50;
    comparar(`onda ${i}: la onda se desplaza en su sentido`, o.y(0.1 + c.sentido * c.v * dt, dt), o.y(0.1, 0), 1e-9, 1e-12 * c.A);
  });

  // ---- Sonido ----
  ref.sonido.forEach((c, i) => {
    const I = O.intensidadTotal(c.focos, c.p);
    comparar(`sonido ${i}: intensidad total`, I, c.I, 1e-12);
    comparar(`sonido ${i}: nivel`, O.nivel(I), c.dB, 1e-12);
    comparar(`sonido ${i}: nivel → intensidad`, O.intensidadDeNivel(c.dB), c.I, 1e-10);
  });
  comparar("sonido: potencia a partir del nivel", O.intensidad(O.potenciaDeNivel(73, 2.5), 2.5), O.intensidadDeNivel(73), 1e-12);
  comparar("sonido: dos focos iguales suman 3,01 dB", O.nivel(2e-6) - O.nivel(1e-6), 10 * Math.log10(2), 1e-12);
  comparar("sonido: doble distancia, −6,02 dB", O.nivel(O.intensidad(1, 2)) - O.nivel(O.intensidad(1, 4)), 20 * Math.log10(2), 1e-12);
  for (const c of ref.igual) comparar(`sonido: igual intensidad P1=${c.P1}, P2=${c.P2}`, O.puntoIgualIntensidad(c.P1, c.P2, c.d), c.x, 1e-9);

  // ---- Cargas y masas ----
  ref.radiales.forEach((c, i) => {
    const campo = Ca.campoRadial(c.fuentes, c.a, c.k);
    const modulo = Math.hypot(c.Ex, c.Ey);
    comparar(`campo radial ${i}: componente x`, campo.x, c.Ex, 1e-11, 1e-12 * modulo);
    comparar(`campo radial ${i}: componente y`, campo.y, c.Ey, 1e-11, 1e-12 * modulo);
    comparar(`campo radial ${i}: x = −dV/dx`, campo.x, c.gradX, 1e-5, 1e-6 * modulo);
    comparar(`campo radial ${i}: y = −dV/dy`, campo.y, c.gradY, 1e-5, 1e-6 * modulo);
    comparar(`campo radial ${i}: potencial`, Ca.potencial(c.fuentes, c.a, c.k), c.Va, 1e-12);
    comparar(`campo radial ${i}: trabajo de A a B`, Ca.trabajo(c.fuentes, c.a, c.b, c.k, c.prueba), c.W, 1e-10);
    comparar(`campo radial ${i}: trabajo de ida y vuelta nulo`,
      Ca.trabajo(c.fuentes, c.a, c.b, c.k, c.prueba) + Ca.trabajo(c.fuentes, c.b, c.a, c.k, c.prueba), 0, 0, 1e-12 * Math.abs(c.W));
  });
  ref.nulos.forEach((c, i) => {
    const fuentes = [{ valor: c.q1, x: 0, y: 0 }, { valor: c.q2, x: c.d, y: 0 }];
    const hallados = Ca.puntosNulos((p) => Ca.campoRadial(fuentes, p, Ca.K), fuentes[0], fuentes[1]);
    anotar(`campo nulo ${i}: se encuentra un único punto`, hallados.length === 1, `hallados ${hallados.length}`);
    if (hallados.length) comparar(`campo nulo ${i}: posición`, hallados[0].x, c.x, 1e-8);
  });

  // ---- Hilos ----
  ref.hilos.forEach((c, i) => {
    const B = Ca.campoHilos(c.hilos, c.p);
    const modulo = Math.hypot(c.Bx, c.By);
    comparar(`hilos ${i}: Bx frente a Biot-Savart`, B.x, c.Bx, 1e-7, 1e-8 * modulo);
    comparar(`hilos ${i}: By frente a Biot-Savart`, B.y, c.By, 1e-7, 1e-8 * modulo);
  });
  {
    const F12 = Ca.fuerzaEntreHilos(5, 2.5, 0.06);
    // Fuerza sobre el hilo 2 calculada como I2·B1.
    const B1 = Ca.campoHilos([{ valor: 5, x: 0, y: 0 }], { x: 0.06, y: 0 });
    comparar("hilos: F/L = I₂·B₁", F12.modulo, 2.5 * Math.hypot(B1.x, B1.y), 1e-12);
    anotar("hilos: corrientes del mismo sentido se atraen", F12.atractiva === true);
    anotar("hilos: corrientes opuestas se repelen", Ca.fuerzaEntreHilos(5, -2.5, 0.06).atractiva === false);
    // Campo nulo entre dos hilos del mismo sentido: I1/x = I2/(d−x)
    const hilos = [{ valor: 5, x: 0, y: 0 }, { valor: 2.5, x: 0.06, y: 0 }];
    const nulos = Ca.puntosNulos((p) => Ca.campoHilos(hilos, p), hilos[0], hilos[1], { transversal: true });
    anotar("hilos: un punto de campo nulo", nulos.length === 1, `hallados ${nulos.length}`);
    if (nulos.length) comparar("hilos: posición del campo nulo", nulos[0].x, 0.04, 1e-8);
  }

  // ---- Óptica geométrica ----
  for (const c of ref.lentes) {
    const l = Op.lente(c.s, c.f);
    comparar(`lente s=${c.s}, f'=${c.f}: posición`, l.sIm, c.sIm, 1e-12);
    comparar(`lente s=${c.s}, f'=${c.f}: aumento`, l.M, c.M, 1e-12);
    // Trazado de rayos: todos los rayos principales pasan por el extremo de la imagen.
    for (const r of Op.rayosPrincipalesLente(c.s, 1, c.f)) {
      const h = Op.alturaEnElemento(c.s, 1, r.p);
      const q = Op.tras_lente(h, r.p, c.f);
      comparar(`lente s=${c.s}, f'=${c.f}: rayo ${r.nombre}`, h + q * c.sIm, c.M, 1e-10, 1e-12);
    }
  }
  for (const c of ref.espejos) {
    const e = Op.espejo(c.s, c.f);
    comparar(`espejo s=${c.s}, f=${c.f}: posición`, e.sIm, c.sIm, 1e-12);
    comparar(`espejo s=${c.s}, f=${c.f}: aumento`, e.M, c.M, 1e-12);
    for (const r of Op.rayosPrincipalesEspejo(c.s, 1, c.f)) {
      const h = Op.alturaEnElemento(c.s, 1, r.p);
      const q = Op.tras_espejo(h, r.p, c.f);
      comparar(`espejo s=${c.s}, f=${c.f}: rayo ${r.nombre}`, h + q * c.sIm, c.M, 1e-10, 1e-12);
    }
  }
  {
    // Dos lentes: la imagen de la primera es el objeto de la segunda.
    const d = Op.dosLentes(-15, 10, 40, 5);
    const l1 = Op.lente(-15, 10);
    const l2 = Op.lente(l1.sIm - 40, 5);
    comparar("dos lentes: posición final", d.segunda.sIm, l2.sIm, 1e-12);
    comparar("dos lentes: aumento total", d.M, l1.M * l2.M, 1e-12);
    anotar("naturaleza: lente con s' > 0 y M < 0", Op.naturaleza(24, -2) === "real, invertida y mayor");
    anotar("naturaleza: espejo con s' > 0 es virtual", Op.naturaleza(10, 2, true).startsWith("virtual, derecha"));
  }

  // ---- Refracción ----
  ref.capas.forEach((c, i) => {
    const r = Op.capasPlanas(c.medios, c.espesores, c.incidencia);
    anotar(`capas ${i}: reflexión total donde corresponde`, r.reflexionEn === c.reflexionEn, `sim ${r.reflexionEn}, ref ${c.reflexionEn}`);
    if (c.reflexionEn === null) {
      comparar(`capas ${i}: ángulo de salida`, r.anguloSalida, c.salida, 1e-10, 1e-12);
      comparar(`capas ${i}: avance lateral`, r.avanceTotal, c.avance, 1e-10, 1e-15);
      comparar(`capas ${i}: tiempo de recorrido`, r.tiempoTotal, c.tiempo, 1e-10);
    }
  });
  ref.prismas.forEach((c, i) => {
    const p = Op.prisma(c);
    comparar(`prisma ${i}: refracción en la primera cara`, p.alfa, c.alfa, 1e-9, 1e-9);
    comparar(`prisma ${i}: incidencia en la segunda cara`, Math.abs(p.gamma), c.gamma, 1e-9, 1e-7);
    anotar(`prisma ${i}: sale o no sale`, p.sale === c.sale);
    if (c.sale) {
      comparar(`prisma ${i}: ángulo de salida`, Math.abs(p.beta), c.beta, 1e-9, 1e-7);
      comparar(`prisma ${i}: desviación`, Math.abs(p.desviacion), c.desviacion, 1e-8, 1e-7);
    }
    if (p.incidenciaMinima) {
      const justoEncima = Op.prisma({ ...c, incidencia: p.incidenciaMinima + 1e-6 });
      const justoDebajo = Op.prisma({ ...c, incidencia: p.incidenciaMinima - 1e-6 });
      anotar(`prisma ${i}: la incidencia mínima separa salida de reflexión total`, justoEncima.sale && !justoDebajo.sale);
    }
  });
  comparar("ángulo límite vidrio-aire", Op.anguloLimite(1.5, 1), Math.asin(1 / 1.5), 1e-14);
  anotar("no hay ángulo límite al pasar a un medio más denso", Op.anguloLimite(1, 1.5) === null);

  // ---- Inducción: la fem es −dΦ/dt ----
  const montajes = {
    "espira entrando": In.espiraEntrando({ B: 0.2, L: 0.2, a: 0.2, v: 2, N: 3 }),
    "campo por tramos": In.campoPorTramos({ S: 1e-3, N: 50 }, [[0, 0], [0.005, 0.06], [0.02, 0.06], [0.03, 0]]),
    "espira girando": In.espiraGirando({ N: 100, S: 1e-3, B: 0.2, w: 50 }),
    "campo senoidal": In.campoSenoidal({ N: 20, S: 4e-3, B0: 0.5, w: 120 }),
  };
  for (const [nombre, m] of Object.entries(montajes)) {
    let peor = 0;
    let maximo = 0;
    for (let i = 0; i < 97; i++) {
      const t = ((i + 0.37) / 97) * m.tMax;
      const h = m.tMax * 1e-7;
      const derivada = -(m.flujo(t + h) - m.flujo(t - h)) / (2 * h);
      peor = Math.max(peor, Math.abs(derivada - m.fem(t)));
      maximo = Math.max(maximo, Math.abs(m.fem(t)));
    }
    anotar(`inducción, ${nombre}: fem = −dΦ/dt`, peor <= 1e-5 * m.femMax, `error ${peor}`);
    anotar(`inducción, ${nombre}: la fem no supera la máxima`, maximo <= m.femMax * (1 + 1e-12) && maximo > 0.5 * m.femMax, `máx ${maximo}, femMax ${m.femMax}`);
  }
  comparar("inducción: fem de la espira que entra, N·B·L·v", montajes["espira entrando"].femMax, 3 * 0.2 * 0.2 * 2, 1e-12);
  comparar("inducción: fem máxima del alternador, N·B·S·ω", montajes["espira girando"].femMax, 100 * 0.2 * 1e-3 * 50, 1e-12);
  anotar("Lenz: flujo entrante que crece → corriente antihoraria", In.sentidoCorriente(1, true) === "antihorario");
  anotar("Lenz: flujo entrante que decrece → corriente horaria", In.sentidoCorriente(-1, true) === "horario");
  anotar("Lenz: flujo saliente que crece → corriente horaria", In.sentidoCorriente(1, false) === "horario");

  // ---- Efecto fotoeléctrico ----
  for (const c of ref.fotoelectrico) {
    const f = Mo.fotoelectrico(c.lambda, c.W);
    const id = `fotoeléctrico λ=${(c.lambda * 1e9).toFixed(0)} nm, W=${c.W} eV`;
    comparar(`${id}: energía del fotón`, f.fotonJ, c.fotonJ, 1e-12);
    anotar(`${id}: hay o no emisión`, f.hay === c.hay);
    comparar(`${id}: energía cinética`, f.EcJ, c.EcJ, 1e-9, 1e-30);
    comparar(`${id}: longitud de onda umbral`, f.lambda0, c.lambda0, 1e-12);
    comparar(`${id}: frecuencia umbral`, f.f0, c.f0, 1e-12);
    comparar(`${id}: velocidad máxima`, f.vMax, c.vMax, 1e-9, 1e-12);
  }
  {
    // Dos medidas generadas con h y W conocidos devuelven esos mismos valores.
    const a = Mo.fotoelectrico(300e-9, 2.3);
    const b = Mo.fotoelectrico(400e-9, 2.3);
    const r = Mo.planckDeDosMedidas(300e-9, a.Vfrenado, 400e-9, b.Vfrenado);
    comparar("Planck a partir de dos medidas: h", r.h, Mo.H, 1e-10);
    comparar("Planck a partir de dos medidas: W", r.W, 2.3 * Mo.E, 1e-9);
  }

  // ---- Desintegración ----
  for (const c of ref.desintegracion) {
    comparar(`desintegración λ=${c.lambda.toExponential(2)}: fracción restante`, Mo.fraccionRestante(c.lambda, c.t), c.fraccion, 1e-8);
    comparar(`desintegración λ=${c.lambda.toExponential(2)}: tiempo hasta esa fracción`, Mo.tiempoHastaFraccion(c.lambda, c.fraccion), c.t, 1e-7);
  }
  comparar("desintegración: tras un periodo queda la mitad", Mo.fraccionRestante(Mo.constante({ tipo: "T", valor: 5730 }), 5730), 0.5, 1e-14);
  comparar("desintegración: vida media = 1/λ", Mo.constante({ tipo: "tau", valor: 40 }), 1 / 40, 1e-14);
  {
    const lambda = Mo.constante({ tipo: "T", valor: 8.02 * 86400 });
    const m = Mo.muestra({ tipo: "masa", valor: 2, masaMolar: 131 }, lambda);
    comparar("muestra: núcleos a partir de la masa", m.N0, (2 / 131) * 6.02e23, 1e-12);
    comparar("muestra: actividad = λ·N", m.A0, lambda * m.N0, 1e-14);
    comparar("muestra: de actividad a masa y vuelta", Mo.muestra({ tipo: "actividad", valor: m.A0, masaMolar: 131 }, lambda).m0, 2, 1e-12);
  }

  // ---- Relatividad ----
  for (const c of ref.relatividad) {
    const id = `relatividad m₀=${c.m0.toExponential(2)}, Ec=${c.Ec.toExponential(2)}`;
    const beta = Mo.betaDeEnergiaCinetica(c.m0, c.Ec);
    comparar(`${id}: velocidad`, beta, c.beta, 1e-9);
    const r = Mo.relativista(c.m0, beta);
    comparar(`${id}: γ`, r.gamma, c.gamma, 1e-9);
    comparar(`${id}: energía total`, r.Etotal, c.Etotal, 1e-9);
    comparar(`${id}: momento, de E² = (pc)² + (m₀c²)²`, r.p, c.p, 1e-7);
    comparar(`${id}: Ec = E − E₀`, r.Ec, c.Ec, 1e-7);
  }
  {
    const lento = Mo.relativista(9.1e-31, 1e-3);
    comparar("relatividad: a baja velocidad coincide con ½mv²", lento.Ec, lento.EcClasica, 1e-5);
  }

  // ---- Carga en campos ----
  ref.lorentz.forEach((c, i) => {
    const g = Lo.giro({ m: c.m, q: c.q, v: c.v, B: c.Bz });
    comparar(`carga ${i}: radio`, g.radio, c.radio, 1e-12);
    comparar(`carga ${i}: periodo`, g.periodo, c.periodo, 1e-12);
    comparar(`carga ${i}: fuerza = m·v²/R`, g.fuerza, (c.m * c.v ** 2) / g.radio, 1e-12);
    const campos = { qm: c.q / c.m, Ey: c.Ey, Bz: c.Bz };
    const puntos = Lo.trayectoria({ x: 0, y: 0, vx: c.v, vy: 0 }, campos, c.tiempo, 1500);
    const [x, y] = puntos[puntos.length - 1];
    const error = Math.hypot(x - c.x, y - c.y);
    anotar(`carga ${i}: posición final frente a la integración de SciPy`, error < 1e-3 * c.radio, `error ${error}, radio ${c.radio}`);
    if (!c.Ey) {
      // Solo campo magnético: la rapidez se conserva.
      const s = { x: 0, y: 0, vx: c.v, vy: 0, t: 0 };
      for (let k = 0; k < 1500; k++) Lo.paso(s, campos, c.tiempo / 1500);
      comparar(`carga ${i}: la rapidez no cambia`, Math.hypot(s.vx, s.vy), c.v, 1e-12);
      comparar(`carga ${i}: velocidad final, x`, s.vx, c.vx, 1e-3, 1e-4 * c.v);
      comparar(`carga ${i}: velocidad final, y`, s.vy, c.vy, 1e-3, 1e-4 * c.v);
    }
  });
  {
    const f = Lo.fuerza(1.6e-19, { vx: 5e4, vy: 0 }, { Ey: -1e4, Bz: -0.2 });
    comparar("selector de velocidades: fuerza nula si v = E/B", f.y, 0, 0, 1e-30);
    comparar("selector de velocidades: v = E/B", Lo.velocidadSelector(1e4, 0.2), 5e4, 1e-12);
    // Regla de la mano derecha: carga positiva hacia +x con B saliente se desvía hacia −y.
    anotar("Lorentz: +q hacia la derecha con B saliente va hacia abajo", Lo.fuerza(1, { vx: 1, vy: 0 }, { Bz: 1 }).y < 0);
    anotar("Lorentz: −q hacia la derecha con B saliente va hacia arriba", Lo.fuerza(-1, { vx: 1, vy: 0 }, { Bz: 1 }).y > 0);
    const v = Lo.velocidadTrasPotencial(9.1e-31, -1.6e-19, 1000);
    comparar("aceleración por potencial: ½mv² = |q|ΔV", 0.5 * 9.1e-31 * v * v, 1.6e-16, 1e-12);
    comparar("De Broglie: λ = h/(m·v)", Lo.longitudDeBroglie(9.1e-31, v) * 9.1e-31 * v, 6.63e-34, 1e-12);
  }

  // ---- Cambio de órbita (elíptica → circular) ----
  for (const orbita of [{ M: 5.97e24, a: 2.66e7, e: 0.74, m: 1500 }, { M: 1.99e30, a: 1.496e11, e: 0.3, m: 1 }]) {
    const mu = Or.G * orbita.M;
    for (const donde of ["lejano", "cercano"]) {
      const c = Or.cambioACircular(orbita, donde);
      const id = `cambio de órbita e=${orbita.e}, punto ${donde}`;
      // Energía aportada = variación de energía cinética (la potencial no cambia en el impulso).
      comparar(`${id}: energía = ΔEc`, c.energia, 0.5 * orbita.m * (c.vCircular ** 2 - c.vAntes ** 2), 1e-10);
      comparar(`${id}: v circular cumple G·M/r² = v²/r`, c.vCircular ** 2 / c.r, mu / c.r ** 2, 1e-12);
      anotar(`${id}: se acelera en el lejano y se frena en el cercano`, donde === "lejano" ? c.deltaV > 0 : c.deltaV < 0);
    }
  }

  // ---- Resultados de problemas de examen ----
  {
    const o = ref.oficiales;
    const f = Mo.fotoelectrico(o.fotoelectrico_2026_ext.lambda, o.fotoelectrico_2026_ext.W);
    comparar("extraordinaria 2026: energía cinética de los electrones (eV)", f.Ec, o.fotoelectrico_2026_ext.Ec_eV, 5e-3);
    const l = o.lamina_2026_ord;
    const r = Op.capasPlanas([1, l.n, 1], [l.e], (l.incidencia_grados * Math.PI) / 180);
    comparar("ordinaria 2026: ángulo de refracción en la lámina (°)", (r.angulos[1] * 180) / Math.PI, l.refraccion_grados, 5e-3);
    const e = o.espectrometro_2025_ext;
    comparar("extraordinaria 2025: radio en el espectrómetro", Lo.giro(e).radio, e.radio, 5e-3);
  }

  return res;
}
