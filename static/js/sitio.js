// Comportamiento común: fórmulas, desplegables de la solución, filtros e impresión.

function pintarFormulas(raiz = document) {
  if (!window.katex) return;
  // Un número en notación científica (6,67·10^{-11}) no debe partirse entre
  // dos líneas: se agrupa entre llaves para que KaTeX lo trate como un bloque.
  const cientifica = /(\d+(?:\{,\}\d+)?\s*\\cdot\s*10\^\{[^{}]*\})/g;
  for (const el of raiz.querySelectorAll(".math:not(.listo)")) {
    const enBloque = el.classList.contains("block");
    const original = el.textContent;
    const tex = enBloque ? original : original.replace(cientifica, "{$1}");
    try {
      window.katex.render(tex, el, {
        displayMode: enBloque,
        throwOnError: false,
        strict: "ignore",
      });
    } catch (e) {
      el.textContent = original;
    }
    el.classList.add("listo");
  }
}

function prepararSolucion() {
  const boton = document.querySelector("[data-abrir-todo]");
  if (!boton) return;
  const pasos = [...document.querySelectorAll(".solucion details")];
  const actualizar = () => {
    const todos = pasos.every((d) => d.open);
    boton.textContent = todos ? "Ocultar todo" : "Mostrar todo";
    boton.setAttribute("aria-pressed", String(todos));
  };
  boton.addEventListener("click", () => {
    const abrir = !pasos.every((d) => d.open);
    for (const d of pasos) d.open = abrir;
    actualizar();
  });
  for (const d of pasos) d.addEventListener("toggle", actualizar);
  // Al imprimir se muestra la solución completa.
  window.addEventListener("beforeprint", () => { for (const d of pasos) d.open = true; });
}

function prepararFiltros() {
  const form = document.querySelector("[data-filtros]");
  if (!form) return;
  const lista = form.parentElement.querySelector(".problemas");
  const vacio = form.parentElement.querySelector("[data-filtros-vacio]");
  const aplicar = () => {
    const datos = new FormData(form);
    const bloque = datos.get("bloque");
    const dificultad = datos.get("dificultad");
    let visibles = 0;
    for (const li of lista.children) {
      const ok = (!bloque || li.dataset.bloque === bloque) &&
                 (!dificultad || li.dataset.dificultad === dificultad);
      li.hidden = !ok;
      if (ok) visibles++;
    }
    lista.hidden = visibles === 0;
    if (vacio) vacio.hidden = visibles !== 0;
  };
  form.addEventListener("change", aplicar);
  aplicar();
}

function prepararImpresion() {
  for (const boton of document.querySelectorAll("[data-imprimir]")) {
    boton.addEventListener("click", () => window.print());
  }
}

document.addEventListener("DOMContentLoaded", () => {
  pintarFormulas();
  prepararImpresion();
  prepararSolucion();
  prepararFiltros();
});
