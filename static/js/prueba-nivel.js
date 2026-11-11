// Prueba de nivel. Enseña al alumno en qué falla (no por qué ni la respuesta
// correcta) y envía el resultado, con su correo, a la hoja de cálculo del
// profesor. El envío se hace una sola vez, al terminar la prueba.

/** Resumen FNV-1a de 32 bits, igual que el de herramientas/build.py. */
export function huella(texto) {
  let h = 0x811c9dc5;
  for (let i = 0; i < texto.length; i++) h = Math.imul(h ^ texto.charCodeAt(i), 0x01000193) >>> 0;
  return h.toString(16).padStart(8, "0");
}

/** Estado de una respuesta: "bien", "mal" o "nose". */
export function corregir(id, valor, clave) {
  if (valor === "x" || valor === null) return "nose";
  return huella(`${id}|${valor}|nivel`) === clave ? "bien" : "mal";
}

/** Valoración de un bloque a partir de aciertos y total. */
export function valorar(aciertos, total) {
  const f = total ? aciertos / total : 0;
  if (f >= 0.8) return { clave: "bien", texto: "Lo llevas bien" };
  if (f >= 0.5) return { clave: "regular", texto: "Tienes lagunas" };
  return { clave: "mal", texto: "Hay que trabajarlo" };
}

/**
 * Elige una variante por pregunta. `grupos` es una lista de listas (las
 * variantes de cada pregunta, en orden) y `azar` devuelve un número en [0, 1).
 */
export function sortear(grupos, azar = Math.random) {
  return grupos.map((variantes) => variantes[Math.min(variantes.length - 1, Math.floor(azar() * variantes.length))]);
}

/** Datos que se envían al profesor. `bloques`: [{nombre, aciertos, items:[{id, mide, estado}]}]. */
export function informe({ correo, nombre, publicidad, asignatura, bloques }) {
  const items = bloques.flatMap((b) => b.items);
  return {
    correo,
    nombre,
    publicidad: Boolean(publicidad),
    asignatura,
    aciertos: bloques.reduce((s, b) => s + b.aciertos, 0),
    total: items.length,
    bloques: bloques.map((b) => ({
      nombre: b.nombre,
      aciertos: b.aciertos,
      total: b.items.length,
      valoracion: valorar(b.aciertos, b.items.length).texto,
      falla: b.items.filter((i) => i.estado === "mal").map((i) => i.mide),
      no_sabe: b.items.filter((i) => i.estado === "nose").map((i) => i.mide),
    })),
    variantes: items.map((i) => i.id).join(" "),
  };
}

/**
 * Envía el informe. La aplicación de Google no permite leer la respuesta desde
 * otra web, así que solo se puede saber si la petición ha salido.
 */
export async function enviar(url, datos) {
  if (!url) return "sin-destino";
  const peticion = () => fetch(url, {
    method: "POST",
    mode: "no-cors",
    keepalive: true,
    headers: { "Content-Type": "text/plain;charset=utf-8" },
    body: JSON.stringify(datos),
  });
  try {
    await peticion();
    return "enviado";
  } catch {
    try { await peticion(); return "enviado"; } catch { return "fallo"; }
  }
}

function crear(etiqueta, clase, padre, texto) {
  const el = document.createElement(etiqueta);
  if (clase) el.className = clase;
  if (texto !== undefined) el.textContent = texto;
  padre?.append(el);
  return el;
}

function montar(raiz) {
  const paso = (nombre) => raiz.querySelector(`[data-paso="${nombre}"]`);
  const pasos = { inicio: paso("inicio"), preguntas: paso("preguntas"), resultado: paso("resultado") };
  const inicio = raiz.querySelector("[data-inicio]");
  const todas = [...raiz.querySelectorAll(".prueba__pregunta")];
  const progreso = raiz.querySelector("[data-progreso]");
  const barra = raiz.querySelector("[data-barra]");
  const bAnterior = raiz.querySelector("[data-anterior]");
  const bSiguiente = raiz.querySelector("[data-siguiente]");
  const titular = raiz.querySelector("[data-titular]");
  const cajaBloques = raiz.querySelector("[data-bloques]");
  const notaEnvio = raiz.querySelector("[data-envio]");

  // Variantes agrupadas por pregunta, en el orden de la página.
  const grupos = [];
  for (const q of todas) {
    const ultimo = grupos[grupos.length - 1];
    if (ultimo && ultimo[0].dataset.ranura === q.dataset.ranura) ultimo.push(q);
    else grupos.push([q]);
  }

  let alumno = { correo: "", nombre: "", publicidad: false, trampa: "" };
  let elegidas = [];
  let actual = 0;
  let resumen = [];
  let ultimoInforme = null;

  function mostrar(nombre) {
    for (const [clave, el] of Object.entries(pasos)) el.hidden = clave !== nombre;
    window.scrollTo({ top: 0 });
  }

  const marcada = (pregunta) => pregunta.querySelector("input:checked")?.value ?? null;

  function pintarPregunta() {
    for (const q of todas) q.hidden = q !== elegidas[actual];
    progreso.textContent = `Pregunta ${actual + 1} de ${elegidas.length}`;
    barra.value = actual / elegidas.length;
    bAnterior.disabled = actual === 0;
    bSiguiente.disabled = marcada(elegidas[actual]) === null;
    bSiguiente.textContent = actual === elegidas.length - 1 ? "Ver mi resultado" : "Siguiente";
    window.scrollTo({ top: 0 });
  }

  inicio.addEventListener("submit", (ev) => {
    ev.preventDefault();
    const datos = new FormData(inicio);
    alumno = {
      correo: String(datos.get("correo") ?? "").trim(),
      nombre: String(datos.get("nombre") ?? "").trim(),
      publicidad: datos.get("publicidad") === "si",
      trampa: String(datos.get("web") ?? ""),
    };
    for (const q of todas) for (const r of q.querySelectorAll("input")) r.checked = false;
    elegidas = sortear(grupos);
    actual = 0;
    mostrar("preguntas");
    pintarPregunta();
  });

  pasos.preguntas.addEventListener("change", () => { bSiguiente.disabled = marcada(elegidas[actual]) === null; });
  bAnterior.addEventListener("click", () => { if (actual > 0) { actual--; pintarPregunta(); } });
  bSiguiente.addEventListener("click", () => {
    if (actual < elegidas.length - 1) { actual++; pintarPregunta(); } else terminar();
  });

  async function terminar() {
    const porBloque = new Map();
    for (const q of elegidas) {
      const estado = corregir(q.dataset.id, marcada(q), q.dataset.clave);
      if (!porBloque.has(q.dataset.bloque)) porBloque.set(q.dataset.bloque, { nombre: q.dataset.bloqueNombre, items: [] });
      porBloque.get(q.dataset.bloque).items.push({ id: q.dataset.id, mide: q.dataset.mide, estado });
    }
    resumen = [...porBloque.values()].map((b) => ({ ...b, aciertos: b.items.filter((i) => i.estado === "bien").length }));
    const aciertos = resumen.reduce((s, b) => s + b.aciertos, 0);
    titular.textContent = `${aciertos} de ${elegidas.length} preguntas bien`;

    cajaBloques.replaceChildren();
    for (const b of resumen) {
      const nota = valorar(b.aciertos, b.items.length);
      const caja = crear("section", `tarjeta prueba__bloque prueba__bloque--${nota.clave}`, cajaBloques);
      const cabecera = crear("div", "prueba__cabecera", caja);
      crear("h2", "", cabecera, b.nombre);
      crear("span", "prueba__nota", cabecera, `${b.aciertos}/${b.items.length} · ${nota.texto}`);
      const medidor = crear("div", "prueba__medidor", caja);
      medidor.setAttribute("aria-hidden", "true");
      crear("i", "", medidor).style.width = `${(100 * b.aciertos) / b.items.length}%`;
      const lista = crear("ul", "prueba__items", caja);
      const marcas = { bien: ["✓", "Bien"], mal: ["✗", "Fallo"], nose: ["?", "No lo sabías"] };
      for (const it of b.items) {
        const li = crear("li", `prueba__item prueba__item--${it.estado}`, lista);
        const [signo, lectura] = marcas[it.estado];
        crear("span", "prueba__signo", li, signo).setAttribute("aria-hidden", "true");
        crear("span", "", li, it.mide);
        crear("span", "oculto-visual", li, ` (${lectura})`);
      }
    }
    notaEnvio.hidden = true;
    mostrar("resultado");
    titular.focus({ preventScroll: true });

    ultimoInforme = informe({ ...alumno, asignatura: raiz.dataset.asignatura, bloques: resumen });
    // Un programa automático habrá rellenado el campo trampa: no se envía nada.
    const estado = alumno.trampa ? "descartado" : await enviar(raiz.dataset.informes, ultimoInforme);
    if (estado === "fallo") {
      notaEnvio.textContent = "No se ha podido enviar tu resultado (¿sin conexión?). Si quieres que lo vea, escríbeme.";
      notaEnvio.hidden = false;
    }
    raiz.dataset.envio = estado;
  }

  raiz.querySelector("[data-repetir]").addEventListener("click", () => mostrar("inicio"));

  // Acceso para pruebas automáticas.
  raiz.pruebaNivel = { get resumen() { return resumen; }, get informe() { return ultimoInforme; }, get elegidas() { return elegidas.map((q) => q.dataset.id); } };
  document.documentElement.dataset.prueba = "ok";
}

const raiz = typeof document === "undefined" ? null : document.querySelector("[data-prueba]");
if (raiz) {
  try { montar(raiz); } catch (e) { document.documentElement.dataset.error = String(e?.message ?? e); }
}
