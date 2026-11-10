// Piezas comunes a todas las simulaciones: lienzo adaptable, bucle de
// animación, controles táctiles y formato de números en español.

let contador = 0;

function crear(etiqueta, clase, padre, texto) {
  const el = document.createElement(etiqueta);
  if (clase) el.className = clase;
  if (texto !== undefined) el.textContent = texto;
  if (padre) padre.append(el);
  return el;
}

/** Monta la estructura básica: lienzo a la izquierda (arriba en móvil) y panel. */
export function estructura(contenedor) {
  contenedor.querySelector("noscript")?.remove();
  const marco = crear("div", "sim__lienzo", contenedor);
  const estado = crear("p", "sim__estado", marco);
  estado.setAttribute("aria-live", "polite");
  const panel = crear("div", "sim__panel", contenedor);
  return { marco, estado, panel };
}

/**
 * Lienzo que ocupa el ancho disponible y se dibuja nítido en pantallas de
 * alta densidad. `dibujar` se llama también cuando cambia el tamaño.
 */
export function crearLienzo(marco, { aspecto = 1, descripcion = "" } = {}) {
  const canvas = crear("canvas", "", marco);
  canvas.setAttribute("role", "img");
  if (descripcion) canvas.setAttribute("aria-label", descripcion);
  const ctx = canvas.getContext("2d");
  const lienzo = { canvas, ctx, ancho: 300, alto: 300, alRedimensionar: null };

  const ajustar = () => {
    const ancho = Math.max(200, Math.round(marco.clientWidth));
    const alto = Math.round(ancho * aspecto);
    const dpr = Math.min(window.devicePixelRatio || 1, 3);
    canvas.width = Math.round(ancho * dpr);
    canvas.height = Math.round(alto * dpr);
    canvas.style.aspectRatio = `${ancho} / ${alto}`;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    lienzo.ancho = ancho;
    lienzo.alto = alto;
    lienzo.alRedimensionar?.();
  };
  new ResizeObserver(ajustar).observe(marco);
  ajustar();
  return lienzo;
}

/**
 * Bucle de animación. `paso(dt)` recibe los segundos reales transcurridos,
 * acotados para que un parón (cambio de pestaña) no provoque un salto.
 */
export function bucle(paso) {
  let id = 0;
  let anterior = 0;
  const cuadro = (t) => {
    const dt = Math.min((t - anterior) / 1000, 0.05);
    anterior = t;
    paso(dt);
    id = requestAnimationFrame(cuadro);
  };
  return {
    get activo() { return id !== 0; },
    arrancar() {
      if (id) return;
      anterior = performance.now();
      id = requestAnimationFrame(cuadro);
    },
    parar() {
      cancelAnimationFrame(id);
      id = 0;
    },
  };
}

export function grupo(panel, titulo) {
  const caja = crear("section", "sim__grupo", panel);
  if (titulo) crear("h2", "", caja, titulo);
  return caja;
}

/**
 * Deslizador con etiqueta, valor visible y atajos opcionales (`marcas`).
 * `formato(valor)` devuelve el texto que se muestra junto a la etiqueta.
 */
export function deslizador(padre, { etiqueta, min, max, paso = 1, valor, formato = String, marcas = [], alCambiar }) {
  const id = `sim-control-${++contador}`;
  const caja = crear("div", "sim__control", padre);
  const rotulo = crear("label", "", caja, etiqueta);
  rotulo.htmlFor = id;
  const salida = crear("output", "", caja);
  salida.htmlFor = id;
  const entrada = crear("input", "", caja);
  Object.assign(entrada, { type: "range", id, min, max, step: paso, value: valor });

  // `actual` puede no coincidir con un paso del deslizador: los atajos fijan
  // valores exactos (por ejemplo raíz de 2) aunque el control los redondee.
  let actual = Number(valor);
  const refrescar = () => {
    const texto = formato(actual);
    salida.textContent = texto;
    entrada.setAttribute("aria-valuetext", texto);
  };
  const fijar = (v, avisar) => {
    actual = Number(v);
    entrada.value = actual;
    refrescar();
    if (avisar) alCambiar?.(actual);
  };
  entrada.addEventListener("input", () => {
    actual = Number(entrada.value);
    refrescar();
    alCambiar?.(actual);
  });

  if (marcas.length) {
    const fila = crear("div", "sim__marcas", caja);
    for (const m of marcas) {
      const b = crear("button", "", fila, m.texto);
      b.type = "button";
      b.addEventListener("click", () => fijar(m.valor, true));
    }
  }
  refrescar();
  return {
    get valor() { return actual; },
    set valor(v) { fijar(v, false); },
    refrescar,
  };
}

/** Lista desplegable. `opciones`: [{ valor, texto }]. */
export function selector(padre, { etiqueta, opciones, valor, alCambiar }) {
  const id = `sim-control-${++contador}`;
  const caja = crear("div", "sim__campo", padre);
  const rotulo = crear("label", "", caja, etiqueta);
  rotulo.htmlFor = id;
  const lista = crear("select", "", caja);
  lista.id = id;
  for (const o of opciones) {
    const op = crear("option", "", lista, o.texto);
    op.value = o.valor;
  }
  lista.value = valor;
  lista.addEventListener("change", () => alCambiar?.(lista.value));
  return {
    caja,
    get valor() { return lista.value; },
    set valor(v) { lista.value = v; },
  };
}

/** Descompone un número en mantisa y exponente legibles: 5.97e24 -> [5.97, 24]. */
export function mantisaExponente(valor) {
  if (!Number.isFinite(valor) || valor === 0) return [0, 0];
  const abs = Math.abs(valor);
  if (abs >= 0.01 && abs < 1e5) return [Number(valor.toPrecision(6)), 0];
  const exp = Math.floor(Math.log10(abs));
  return [Number((valor / 10 ** exp).toPrecision(6)), exp];
}

/**
 * Campo para escribir un número como en el enunciado: mantisa, potencia de
 * diez y, si se quiere, unidad. `unidades`: [{ texto, factor }] con el factor
 * que pasa esa unidad al SI. `valor` se lee y se escribe siempre en el SI.
 */
export function campoCientifico(padre, { etiqueta, valor, unidades, alCambiar }) {
  const id = `sim-control-${++contador}`;
  const caja = crear("div", "sim__campo", padre);
  const rotulo = crear("label", "", caja, etiqueta);
  rotulo.htmlFor = id;
  const fila = crear("div", "sim__cientifico", caja);

  const mantisa = crear("input", "sim__mantisa", fila);
  Object.assign(mantisa, { type: "number", id, step: "any", inputMode: "decimal" });
  crear("span", "", fila, "· 10");
  const exponente = crear("input", "sim__exponente", fila);
  Object.assign(exponente, { type: "number", step: 1, inputMode: "numeric" });
  exponente.setAttribute("aria-label", `${etiqueta}: exponente de diez`);

  let unidad;
  if (unidades.length > 1) {
    unidad = crear("select", "", fila);
    unidad.setAttribute("aria-label", `${etiqueta}: unidad`);
    unidades.forEach((u, i) => {
      const op = crear("option", "", unidad, u.texto);
      op.value = i;
    });
  } else {
    crear("span", "sim__unidad", fila, unidades[0].texto);
  }
  const factor = () => unidades[unidad ? Number(unidad.value) : 0].factor;

  const leer = () => Number(mantisa.value) * 10 ** Number(exponente.value || 0) * factor();
  const escribir = (si) => {
    const [m, e] = mantisaExponente(si / factor());
    mantisa.value = m;
    exponente.value = e;
  };
  escribir(valor);
  const avisar = () => {
    const v = leer();
    if (mantisa.value !== "" && Number.isFinite(v)) alCambiar?.(v);
  };
  mantisa.addEventListener("input", avisar);
  exponente.addEventListener("input", avisar);
  unidad?.addEventListener("change", avisar);
  return {
    caja,
    get valor() { return leer(); },
    set valor(si) { escribir(si); },
    /** Cambia de unidad conservando el valor físico. */
    ponerUnidad(indice, si) {
      if (unidad) unidad.value = indice;
      escribir(si);
    },
  };
}

/** Parámetros numéricos de la URL (?M=5.97e24&h=6e5). Ignora los que no son números. */
export function parametrosURL() {
  const datos = {};
  for (const [clave, texto] of new URLSearchParams(window.location.search)) {
    const valor = Number(texto);
    if (texto !== "" && Number.isFinite(valor)) datos[clave] = valor;
  }
  return datos;
}

export function botones(padre) {
  const fila = crear("div", "sim__botones", padre);
  return (texto, alPulsar, { suave = false } = {}) => {
    const b = crear("button", suave ? "boton boton--suave" : "boton", fila, texto);
    b.type = "button";
    b.addEventListener("click", alPulsar);
    return b;
  };
}

/** Tabla de lecturas (magnitud y valor). Devuelve `poner(clave, html)`. */
export function lecturas(padre, filas) {
  const dl = crear("dl", "sim__lecturas", padre);
  const celdas = {};
  for (const [clave, etiqueta] of filas) {
    crear("dt", "", dl, etiqueta);
    celdas[clave] = crear("dd", "", dl, "—");
  }
  const previo = {};
  return (clave, html) => {
    if (previo[clave] === html) return;
    previo[clave] = html;
    celdas[clave].innerHTML = html;
  };
}

/** Barras horizontales con el cero en el centro (para energías con signo). */
export function barras(padre, filas) {
  const caja = crear("div", "sim__barras", padre);
  caja.setAttribute("aria-hidden", "true");
  const tiras = {};
  for (const [clave, etiqueta, color] of filas) {
    const fila = crear("div", "sim__barra", caja);
    crear("span", "", fila, etiqueta);
    const pista = crear("div", "", fila);
    tiras[clave] = crear("i", "", pista);
    tiras[clave].style.background = color;
  }
  /** `fraccion` entre -1 y 1. */
  return (clave, fraccion) => {
    const f = Math.max(-1, Math.min(1, fraccion));
    const tira = tiras[clave];
    tira.style.left = `${f < 0 ? 50 + f * 50 : 50}%`;
    tira.style.width = `${Math.abs(f) * 50}%`;
  };
}

// ---- Formato de números ---------------------------------------------------

/** Número con coma decimal y espacio fino de millares: 35 786,0 */
export function num(valor, decimales = 0) {
  const texto = Math.abs(valor).toFixed(decimales);
  let [entera, decimal] = texto.split(".");
  if (entera.length > 4) entera = entera.replace(/\B(?=(\d{3})+(?!\d))/g, " ");
  const signo = valor < 0 && Number(texto) !== 0 ? "−" : "";
  return signo + entera + (decimal ? "," + decimal : "");
}

/** Notación científica en HTML: 2,94·10<sup>10</sup> */
export function cientifica(valor, cifras = 3) {
  if (valor === 0 || !Number.isFinite(valor)) return "0";
  let exp = Math.floor(Math.log10(Math.abs(valor)));
  let mantisa = valor / 10 ** exp;
  if (Math.abs(Number(mantisa.toFixed(cifras - 1))) >= 10) {
    mantisa /= 10;
    exp += 1;
  }
  const expTexto = String(exp).replace("-", "−");
  return `${num(mantisa, cifras - 1)}·10<sup>${expTexto}</sup>`;
}

/**
 * Valor con unidad y tres cifras significativas, como en un resultado de
 * examen: decimal si es un número cómodo (8,19 m/s²) y científica si no.
 */
export function medida(valor, unidad, cifras = 3) {
  if (!Number.isFinite(valor)) return "—";
  const abs = Math.abs(valor);
  let texto;
  if (valor === 0) texto = "0";
  else if (abs >= 0.1 && abs < 1000) {
    const exp = Math.floor(Math.log10(abs));
    texto = num(valor, Math.max(0, cifras - 1 - exp));
  } else texto = cientifica(valor, cifras);
  return unidad ? `${texto} ${unidad}` : texto;
}

/** Duración en la unidad más natural: 96,5 min · 23,9 h · 27,3 días · 248 años */
export function duracion(segundos) {
  if (!Number.isFinite(segundos)) return "—";
  if (segundos < 120) return `${num(segundos, 1)} s`;
  if (segundos < 2 * 3600) return `${num(segundos / 60, 1)} min`;
  if (segundos < 3 * 86400) return `${num(segundos / 3600, 2)} h`;
  if (segundos < 2 * 365.25 * 86400) return `${num(segundos / 86400, 1)} días`;
  return `${medida(segundos / (365.25 * 86400), "años")}`;
}

// ---- Dibujo ---------------------------------------------------------------

/** Flecha de (x, y) a (x + dx, y + dy), en píxeles. */
export function flecha(ctx, x, y, dx, dy, color, grosor = 2.5) {
  const largo = Math.hypot(dx, dy);
  if (largo < 0.5) return;
  const punta = Math.min(9, largo * 0.6);
  const ang = Math.atan2(dy, dx);
  ctx.save();
  ctx.strokeStyle = ctx.fillStyle = color;
  ctx.lineWidth = grosor;
  ctx.lineCap = "round";
  ctx.beginPath();
  ctx.moveTo(x, y);
  ctx.lineTo(x + dx - Math.cos(ang) * punta * 0.8, y + dy - Math.sin(ang) * punta * 0.8);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(x + dx, y + dy);
  ctx.lineTo(x + dx - punta * Math.cos(ang - 0.45), y + dy - punta * Math.sin(ang - 0.45));
  ctx.lineTo(x + dx - punta * Math.cos(ang + 0.45), y + dy - punta * Math.sin(ang + 0.45));
  ctx.closePath();
  ctx.fill();
  ctx.restore();
}
