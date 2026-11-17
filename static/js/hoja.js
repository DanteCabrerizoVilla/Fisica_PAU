// Generador de hojas de ejercicios.
// La selección es aleatoria pero reproducible: los filtros y una semilla viajan
// en la URL, así que el mismo enlace siempre da la misma hoja.

(() => {
  const raiz = document.querySelector("[data-hoja]");
  if (!raiz) return;
  const form = raiz.querySelector("[data-hoja-form]");
  const cuenta = raiz.querySelector("[data-hoja-cuenta]");
  const otra = raiz.querySelector("[data-hoja-otra]");
  const salida = raiz.querySelector("[data-hoja-salida]");
  const lista = raiz.querySelector("[data-hoja-lista]");
  const resumen = raiz.querySelector("[data-hoja-resumen]");
  const bloqueResultados = raiz.querySelector("[data-hoja-resultados]");
  const listaResultados = raiz.querySelector("[data-hoja-resultados-lista]");
  const enlacePie = raiz.querySelector("[data-hoja-enlace]");
  const copiado = raiz.querySelector("[data-hoja-copiado]");

  const ordenBloques = [...form.querySelectorAll('input[name="b"]')].map((i) => i.value);
  const nombreConv = { modelo: "Modelo", ordinaria: "Ordinaria", extraordinaria: "Extraordinaria",
    "ordinaria-coincidentes": "Ordinaria (coincidentes)", "extraordinaria-coincidentes": "Extraordinaria (coincidentes)" };

  let datos = null;
  const cargar = async () => {
    if (!datos) {
      const r = await fetch(raiz.dataset.datos);
      if (!r.ok) throw new Error(`No se han podido cargar los problemas (${r.status})`);
      datos = await r.json();
    }
    return datos;
  };

  // ---- azar con semilla (xmur3 + mulberry32) ----
  const nuevaSemilla = () => Math.random().toString(36).slice(2, 8);
  function generador(semilla) {
    let h = 1779033703 ^ semilla.length;
    for (let i = 0; i < semilla.length; i++) {
      h = Math.imul(h ^ semilla.charCodeAt(i), 3432918353);
      h = (h << 13) | (h >>> 19);
    }
    let a = h >>> 0;
    return () => {
      a = (a + 0x6d2b79f5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function barajar(v, azar) {
    const c = [...v];
    for (let i = c.length - 1; i > 0; i--) {
      const j = Math.floor(azar() * (i + 1));
      [c[i], c[j]] = [c[j], c[i]];
    }
    return c;
  }

  // ---- filtros <-> formulario <-> URL ----
  function leerFormulario() {
    const f = new FormData(form);
    return {
      b: f.getAll("b"),
      t: f.getAll("t"),
      d: f.getAll("d").map(Number),
      desde: Number(f.get("desde")),
      hasta: Number(f.get("hasta")),
      n: Number(f.get("n")),
      r: f.get("r") === "1",
    };
  }

  function escribirFormulario(o) {
    const marcar = (nombre, valores) => {
      for (const i of form.querySelectorAll(`input[name="${nombre}"]`)) i.checked = valores.includes(i.value);
    };
    marcar("b", o.b);
    marcar("t", o.t);
    marcar("d", o.d.map(String));
    if (o.t.length) form.querySelector(".hoja__temas").open = true;
    for (const [nombre, valor] of [["desde", o.desde], ["hasta", o.hasta], ["n", o.n]]) {
      const sel = form.elements[nombre];
      if ([...sel.options].some((op) => Number(op.value) === valor)) sel.value = String(valor);
    }
    form.elements.r.checked = o.r;
  }

  function aURL(o, semilla) {
    const p = new URLSearchParams();
    p.set("b", o.b.join(","));
    if (o.t.length) p.set("t", o.t.join(","));
    p.set("d", o.d.join(","));
    p.set("desde", o.desde);
    p.set("hasta", o.hasta);
    p.set("n", o.n);
    p.set("r", o.r ? "1" : "0");
    p.set("s", semilla);
    return p;
  }

  function deURL() {
    const p = new URLSearchParams(location.search);
    if (!p.get("s")) return null;
    const lista = (k) => (p.get(k) || "").split(",").filter(Boolean);
    return {
      opciones: {
        b: lista("b"), t: lista("t"), d: lista("d").map(Number),
        desde: Number(p.get("desde")), hasta: Number(p.get("hasta")),
        n: Number(p.get("n")) || 6, r: p.get("r") !== "0",
      },
      semilla: p.get("s"),
    };
  }

  // ---- selección ----
  function candidatos(todos, o) {
    const temas = new Set(o.t);
    return todos.filter((p) => {
      if (!o.b.includes(p.bloque)) return false;
      if (!o.d.includes(p.dificultad)) return false;
      if (p.anio < Math.min(o.desde, o.hasta) || p.anio > Math.max(o.desde, o.hasta)) return false;
      // Los temas solo restringen dentro de los bloques en los que se ha marcado alguno.
      const temasDelBloque = o.t.filter((t) => form.querySelector(`input[name="t"][value="${t}"]`)?.dataset.bloque === p.bloque);
      if (temasDelBloque.length && !p.subtemas.some((s) => temas.has(s))) return false;
      return true;
    });
  }

  function elegir(cands, n, semilla) {
    const azar = generador(semilla);
    const ordenados = [...cands].sort((x, y) => (x.id < y.id ? -1 : 1));
    // Reparto por bloques: se van cogiendo de uno en uno para que la hoja quede variada.
    const porBloque = new Map();
    for (const p of barajar(ordenados, azar)) {
      if (!porBloque.has(p.bloque)) porBloque.set(p.bloque, []);
      porBloque.get(p.bloque).push(p);
    }
    const colas = barajar([...porBloque.values()], azar);
    const elegidos = [];
    while (elegidos.length < n && colas.some((c) => c.length)) {
      for (const c of colas) if (c.length && elegidos.length < n) elegidos.push(c.shift());
    }
    // En la hoja, ordenados como el temario y de más fácil a más difícil.
    return elegidos.sort((x, y) =>
      ordenBloques.indexOf(x.bloque) - ordenBloques.indexOf(y.bloque) || x.dificultad - y.dificultad);
  }

  // ---- pintar ----
  const etiquetaOrigen = (p) =>
    `${p.coleccion_etiqueta} · Pregunta ${p.numero} · ${p.bloque_nombre} · ${p.dificultad_nombre}`;

  function pintar(elegidos, o, total) {
    lista.replaceChildren();
    listaResultados.replaceChildren();
    for (const p of elegidos) {
      const li = document.createElement("li");
      li.className = "hoja__problema";
      li.innerHTML = `
        <p class="hoja__origen"></p>
        <div class="hoja__enunciado">${p.enunciado}</div>
        <p class="hoja__enlace no-impresion"><a href="${p.url}">Ver la solución paso a paso</a></p>`;
      li.querySelector(".hoja__origen").textContent = etiquetaOrigen(p);
      lista.append(li);

      const r = document.createElement("li");
      r.innerHTML = p.resultados.length
        ? p.resultados.map((x) => `<span class="hoja__apartado"><strong>${x.apartado})</strong> ${x.html}</span>`).join(" ")
        : "<span>Pregunta de teoría: ver la solución en la web.</span>";
      listaResultados.append(r);
    }
    bloqueResultados.hidden = !o.r;
    const nombres = [...form.querySelectorAll('input[name="b"]')].filter((i) => o.b.includes(i.value))
      .map((i) => i.nextElementSibling.textContent);
    const anios = o.desde === o.hasta ? `${o.desde}` : `${Math.min(o.desde, o.hasta)}–${Math.max(o.desde, o.hasta)}`;
    resumen.textContent = `${elegidos.length} problemas de examen · ${nombres.join(", ")} · ${anios}` +
      (elegidos.length < o.n ? ` (solo había ${total} con estos filtros)` : "");
    enlacePie.textContent = location.href.replace(/^https?:\/\//, "");
    salida.hidden = false;
    // KaTeX se carga aparte: si aún no ha llegado, se pinta al terminar de cargar la página.
    const formulas = () => window.pintarFormulas && window.pintarFormulas(salida);
    if (window.katex) formulas();
    else window.addEventListener("load", formulas, { once: true });
  }

  async function generar(o, semilla, desplazar) {
    let todos;
    try {
      todos = await cargar();
    } catch (e) {
      cuenta.textContent = e.message;
      return;
    }
    const cands = candidatos(todos, o);
    if (!cands.length) {
      cuenta.textContent = "No hay problemas con esos filtros. Prueba a abrir más bloques, años o dificultades.";
      salida.hidden = true;
      return;
    }
    history.replaceState(null, "", `${location.pathname}?${aURL(o, semilla).toString().replace(/%2C/g, ",")}`);
    pintar(elegir(cands, o.n, semilla), o, cands.length);
    otra.hidden = false;
    cuenta.textContent = `${cands.length} problemas cumplen los filtros.`;
    if (desplazar) salida.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  // Al cambiar un filtro, se avisa de cuántos problemas quedan.
  form.addEventListener("change", async () => {
    try {
      const n = candidatos(await cargar(), leerFormulario()).length;
      cuenta.textContent = n ? `${n} problemas cumplen los filtros.` : "No hay problemas con esos filtros.";
    } catch (e) {
      cuenta.textContent = e.message;
    }
  });
  form.addEventListener("submit", (ev) => {
    ev.preventDefault();
    generar(leerFormulario(), nuevaSemilla(), true);
  });
  otra.addEventListener("click", () => generar(leerFormulario(), nuevaSemilla(), true));

  raiz.querySelector("[data-hoja-imprimir]").addEventListener("click", () => window.print());
  raiz.querySelector("[data-hoja-copiar]").addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(location.href);
      copiado.textContent = "Enlace copiado.";
    } catch {
      copiado.textContent = location.href;
    }
    copiado.hidden = false;
    setTimeout(() => { copiado.hidden = true; }, 4000);
  });

  // Si se llega con un enlace compartido, se reconstruye la misma hoja.
  const compartida = deURL();
  if (compartida) {
    escribirFormulario(compartida.opciones);
    generar(compartida.opciones, compartida.semilla, false);
  }
})();
