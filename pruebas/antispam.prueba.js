// Protección contra spam del receptor de la prueba de nivel.
// Carga herramientas/informes-prueba-nivel.gs tal cual, con sustitutos de los
// servicios de Google, y comprueba que acepta un envío legítimo y rechaza los demás.

import { informe, sellar, sha256 as sha256Web, textoSello } from "../static/js/prueba-nivel.js";

// SHA-256 síncrono (el de Apps Script lo es); así además se compara con el del navegador.
function sha256Bytes(texto) {
  const K = new Uint32Array([
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]);
  const datos = new TextEncoder().encode(texto);
  const largo = Math.ceil((datos.length + 9) / 64) * 64;
  const m = new Uint8Array(largo);
  m.set(datos);
  m[datos.length] = 0x80;
  new DataView(m.buffer).setUint32(largo - 4, datos.length * 8);
  const H = new Uint32Array([0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]);
  const W = new Uint32Array(64);
  const rot = (x, n) => (x >>> n) | (x << (32 - n));
  const vista = new DataView(m.buffer);
  for (let i = 0; i < largo; i += 64) {
    for (let j = 0; j < 16; j++) W[j] = vista.getUint32(i + 4 * j);
    for (let j = 16; j < 64; j++) {
      const s0 = rot(W[j - 15], 7) ^ rot(W[j - 15], 18) ^ (W[j - 15] >>> 3);
      const s1 = rot(W[j - 2], 17) ^ rot(W[j - 2], 19) ^ (W[j - 2] >>> 10);
      W[j] = W[j - 16] + s0 + W[j - 7] + s1;
    }
    let [a, b, c, d, e, f, g, h] = H;
    for (let j = 0; j < 64; j++) {
      const t1 = (h + (rot(e, 6) ^ rot(e, 11) ^ rot(e, 25)) + ((e & f) ^ (~e & g)) + K[j] + W[j]) >>> 0;
      const t2 = ((rot(a, 2) ^ rot(a, 13) ^ rot(a, 22)) + ((a & b) ^ (a & c) ^ (b & c))) >>> 0;
      [h, g, f, e, d, c, b, a] = [g, f, e, (d + t1) >>> 0, c, b, a, (t1 + t2) >>> 0];
    }
    [a, b, c, d, e, f, g, h].forEach((x, k) => { H[k] = (H[k] + x) >>> 0; });
  }
  const salida = new Uint8Array(32);
  H.forEach((x, k) => new DataView(salida.buffer).setUint32(4 * k, x));
  return salida;
}

function cargarReceptor(fuente) {
  const cache = new Map();
  const Utilities = {
    DigestAlgorithm: { SHA_256: "SHA_256" },
    Charset: { UTF_8: "UTF_8" },
    computeDigest: (_alg, texto) => [...sha256Bytes(texto)].map((b) => (b > 127 ? b - 256 : b)),   // bytes con signo, como Java
    formatDate: () => "2026111412",
  };
  const CacheService = { getScriptCache: () => ({ get: (k) => cache.get(k) ?? null, put: (k, v) => cache.set(k, v) }) };
  const f = new Function("Utilities", "CacheService", `${fuente}\nreturn { revisar, validar, sha256, POR_CORREO_Y_HORA };`);
  return f(Utilities, CacheService);
}

function bloquesDePrueba(desfase = 0) {
  const nombres = [["grav", "Gravitación"], ["elec", "Electromagnetismo"], ["onda", "Ondas"], ["opt", "Óptica"], ["mod", "Física moderna"]];
  return nombres.map(([pref, nombre], k) => {
    const items = [1, 2, 3, 4, 5, 6].map((i) => ({
      id: `${pref}-${i}${"abc"[(i + k + desfase) % 3]}`, mide: `Idea ${i} de ${nombre}`,
      estado: ["bien", "mal", "nose"][(i + k) % 3],
    }));
    return { nombre, items, aciertos: items.filter((x) => x.estado === "bien").length };
  });
}

export async function probar() {
  const res = [];
  const anotar = (nombre, ok, detalle = "") => res.push({ nombre: `antispam: ${nombre}`, ok, detalle });
  const fuente = await (await fetch("../herramientas/informes-prueba-nivel.gs")).text();
  const rx = cargarReceptor(fuente);
  const ahora = Date.now();

  // El SHA-256 del navegador y el del receptor coinciden, también con tildes.
  for (const texto of ["", "abc", "ana@ejemplo.com|12|30|grav-1a|ñ€"]) {
    anotar(`mismo SHA-256 en web y receptor («${texto}»)`, (await sha256Web(texto)) === rx.sha256(texto));
  }

  const nuevo = async (cambios = {}, desfase = 0) => {
    const d = informe({ correo: "Ana@Ejemplo.com", nombre: "Ana", publicidad: false, asignatura: "Física",
      bloques: bloquesDePrueba(desfase), t: ahora - 1000 * desfase, duracion: 1200, ...cambios });
    d.sello = await sellar(d);
    return d;
  };
  const rechaza = (d, ahoraRx = ahora) => { try { rx.revisar(d, ahoraRx); return ""; } catch (e) { return e.message; } };

  const bueno = await nuevo();
  anotar("el sello cumple la dificultad", (await sha256Web(textoSello(bueno, bueno.sello))).startsWith("000"));
  anotar("acepta un envío legítimo", rechaza(bueno) === "", rechaza(bueno));
  anotar("rechaza el mismo envío repetido", rechaza(bueno) === "envío repetido", rechaza(bueno));

  const conTrampa = { ...(await nuevo({}, 1)), web: "http://spam.example" };
  anotar("rechaza si el campo trampa viene relleno", rechaza(conTrampa) === "campo trampa relleno", rechaza(conTrampa));

  const rapido = await nuevo({ duracion: 20 }, 2);
  anotar("rechaza una prueba hecha en 20 s", rechaza(rapido) === "duración no válida", rechaza(rapido));

  const viejo = await nuevo({ t: ahora - 2 * 3600 * 1000 }, 3);
  anotar("rechaza un envío con la hora de hace 2 h", rechaza(viejo) === "hora no válida", rechaza(viejo));

  const sinSello = { ...(await nuevo({}, 4)) };
  sinSello.sello = "";
  const huellaSinSello = rx.sha256([sinSello.correo.toLowerCase(), sinSello.aciertos, sinSello.total, sinSello.variantes, sinSello.t, sinSello.duracion, ""].join("|"));
  if (!huellaSinSello.startsWith("000")) anotar("rechaza un envío sin sello", rechaza(sinSello) === "sello no válido", rechaza(sinSello));

  const retocado = await nuevo({}, 5);
  retocado.duracion += 1;                              // cambiar un dato después de sellar
  anotar("rechaza datos cambiados después de sellar", rechaza(retocado) === "sello no válido", rechaza(retocado));

  const descuadre = await nuevo({}, 6);
  descuadre.bloques[0].aciertos += 1;
  anotar("rechaza bloques que no cuadran con el total", rechaza(descuadre) === "los bloques no cuadran", rechaza(descuadre));

  const corto = await nuevo({}, 7);
  corto.total = 29;
  anotar("rechaza una prueba que no tiene 30 preguntas", rechaza(corto) === "resultado no válido", rechaza(corto));

  const raro = await nuevo({}, 8);
  raro.variantes = raro.variantes.replace("grav-1", "<script>");
  anotar("rechaza identificadores de pregunta inventados", rechaza(raro) === "variantes no válidas", rechaza(raro));

  // Límite por correo: ya se aceptó uno; se aceptan hasta POR_CORREO_Y_HORA en total.
  const aceptados = [rechaza(await nuevo({}, 9)), rechaza(await nuevo({}, 10))];
  const sobra = rechaza(await nuevo({}, 11));
  anotar("acepta varios intentos del mismo alumno", aceptados.every((x) => x === ""), aceptados.join(","));
  anotar(`rechaza el envío ${rx.POR_CORREO_Y_HORA + 1}.º del mismo correo en una hora`, sobra === "demasiados envíos de este correo", sobra);

  // Lo que llega se apunta sin fórmulas.
  const malicioso = await nuevo({ correo: "otra@ejemplo.com", nombre: "=IMPORTXML(\"http://x\")" }, 12);
  const fila = rx.validar(malicioso);
  anotar("neutraliza fórmulas en la hoja", fila[2].startsWith("'="), fila[2]);
  anotar("apunta la duración en minutos", fila[10] === 20, String(fila[10]));
  return res;
}
