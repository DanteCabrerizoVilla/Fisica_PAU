// Prueba de nivel. Enseña al alumno en qué falla (no por qué ni la respuesta
// correcta) y prepara un mensaje de WhatsApp con el resultado para el profesor.
// Todo ocurre en el navegador: no se envía ni se guarda nada por su cuenta.

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

/** Texto del mensaje que se envía al profesor. */
export function redactar({ profesor, asignatura, nombre, modo, bloques, final }) {
  const aciertos = bloques.reduce((s, b) => s + b.aciertos, 0);
  const total = bloques.reduce((s, b) => s + b.items.length, 0);
  const lineas = [
    `Hola${profesor ? ` ${profesor}` : ""}, he hecho la prueba de nivel de ${asignatura}.`,
    ...(nombre ? [`Me llamo ${nombre}.`] : []),
    `Resultado: ${aciertos} de ${total} (prueba ${modo === "rapida" ? "rápida" : "completa"}).`,
    "",
  ];
  for (const b of bloques) {
    lineas.push(`${b.nombre}: ${b.aciertos}/${b.items.length}`);
    for (const it of b.items) {
      if (it.estado === "mal") lineas.push(`  ✗ ${it.mide}`);
      if (it.estado === "nose") lineas.push(`  ? ${it.mide} (no lo sé)`);
    }
  }
  lineas.push("", final);
  return lineas.join("\n");
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
  const avisoInicio = raiz.querySelector("[data-aviso-inicio]");
  const todas = [...raiz.querySelectorAll(".prueba__pregunta")];
  const progreso = raiz.querySelector("[data-progreso]");
  const barra = raiz.querySelector("[data-barra]");
  const bAnterior = raiz.querySelector("[data-anterior]");
  const bSiguiente = raiz.querySelector("[data-siguiente]");
  const titular = raiz.querySelector("[data-titular]");
  const cajaBloques = raiz.querySelector("[data-bloques]");
  const campoNombre = raiz.querySelector("[data-nombre]");
  const bEnviar = raiz.querySelector("[data-enviar]");
  const bCopiar = raiz.querySelector("[data-copiar]");

  let modo = "rapida";
  let elegidas = [];
  let nombres = {};
  let actual = 0;
  let resumen = [];

  function mostrar(nombre) {
    for (const [clave, el] of Object.entries(pasos)) el.hidden = clave !== nombre;
    window.scrollTo({ top: 0 });
  }

  const marcada = (pregunta) => pregunta.querySelector("input:checked")?.value ?? null;

  function pintarPregunta() {
    elegidas.forEach((q, i) => { q.hidden = i !== actual; });
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
    modo = datos.get("modo");
    const bloques = datos.getAll("bloque");
    avisoInicio.hidden = bloques.length > 0;
    if (!bloques.length) return;
    nombres = Object.fromEntries([...inicio.querySelectorAll('[name="bloque"]')].map((c) => [c.value, c.dataset.nombre]));
    elegidas = todas.filter((q) => bloques.includes(q.dataset.bloque) && (modo === "completa" || "rapida" in q.dataset));
    for (const q of todas) {
      q.hidden = true;
      for (const r of q.querySelectorAll("input")) r.checked = false;
    }
    actual = 0;
    mostrar("preguntas");
    pintarPregunta();
  });

  pasos.preguntas.addEventListener("change", () => { bSiguiente.disabled = marcada(elegidas[actual]) === null; });
  bAnterior.addEventListener("click", () => { if (actual > 0) { actual--; pintarPregunta(); } });
  bSiguiente.addEventListener("click", () => {
    if (actual < elegidas.length - 1) { actual++; pintarPregunta(); } else terminar();
  });

  function terminar() {
    const porBloque = new Map();
    for (const q of elegidas) {
      const estado = corregir(q.dataset.id, marcada(q), q.dataset.clave);
      if (!porBloque.has(q.dataset.bloque)) porBloque.set(q.dataset.bloque, []);
      porBloque.get(q.dataset.bloque).push({ mide: q.dataset.mide, estado });
    }
    resumen = [...porBloque].map(([id, items]) => ({
      id, nombre: nombres[id], items, aciertos: items.filter((i) => i.estado === "bien").length,
    }));
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
    actualizarEnvio();
    mostrar("resultado");
    titular.focus({ preventScroll: true });
  }

  const mensaje = () => redactar({
    profesor: raiz.dataset.profesor,
    asignatura: raiz.dataset.asignatura,
    nombre: campoNombre.value.trim(),
    modo,
    bloques: resumen,
    final: raiz.dataset.mensajeFinal,
  });

  function actualizarEnvio() {
    const base = raiz.dataset.whatsapp || "https://wa.me/";
    bEnviar.href = `${base}?text=${encodeURIComponent(mensaje())}`;
  }
  campoNombre.addEventListener("input", actualizarEnvio);

  bCopiar.addEventListener("click", async () => {
    const original = "Copiar el resultado";
    try {
      await navigator.clipboard.writeText(mensaje());
      bCopiar.textContent = "Copiado";
    } catch {
      bCopiar.textContent = "No se ha podido copiar";
    }
    setTimeout(() => { bCopiar.textContent = original; }, 2000);
  });

  raiz.querySelector("[data-repetir]").addEventListener("click", () => mostrar("inicio"));

  // Acceso para pruebas automáticas.
  raiz.pruebaNivel = { terminar, get resumen() { return resumen; }, mensaje };
  document.documentElement.dataset.prueba = "ok";
}

const raiz = document.querySelector("[data-prueba]");
if (raiz) {
  try { montar(raiz); } catch (e) { document.documentElement.dataset.error = String(e?.message ?? e); }
}
