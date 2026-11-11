// Corrección y redacción del resultado de la prueba de nivel.

import { corregir, huella, redactar, valorar } from "../static/js/prueba-nivel.js";

export async function probar() {
  const ref = await (await fetch("prueba_nivel.ref.json")).json();
  const res = [];
  const anotar = (nombre, ok, detalle = "") => res.push({ nombre, ok, detalle });

  anotar("prueba de nivel: hay preguntas", ref.casos.length >= 10, `${ref.casos.length}`);
  for (const c of ref.casos) {
    anotar(`prueba de nivel ${c.id}: la huella coincide con la de Python`, huella(`${c.id}|${c.correcta}|nivel`) === c.clave);
    const estados = [0, 1, 2, 3].map((i) => corregir(c.id, String(i), c.clave));
    anotar(`prueba de nivel ${c.id}: solo una opción se da por buena`,
      estados.filter((e) => e === "bien").length === 1 && estados[c.correcta] === "bien", estados.join(","));
    anotar(`prueba de nivel ${c.id}: «No lo sé» no cuenta como acierto`, corregir(c.id, "x", c.clave) === "nose" && corregir(c.id, null, c.clave) === "nose");
  }

  anotar("valoración: 2 de 2 → bien", valorar(2, 2).clave === "bien");
  anotar("valoración: 5 de 6 → bien", valorar(5, 6).clave === "bien");
  anotar("valoración: 1 de 2 → regular", valorar(1, 2).clave === "regular");
  anotar("valoración: 3 de 6 → regular", valorar(3, 6).clave === "regular");
  anotar("valoración: 2 de 6 → mal", valorar(2, 6).clave === "mal");
  anotar("valoración: 0 de 2 → mal", valorar(0, 2).clave === "mal");

  const texto = redactar({
    profesor: "Dante", asignatura: "Física (PAU Madrid)", nombre: "Ana", modo: "rapida", final: "¿Vemos una clase?",
    bloques: [
      { nombre: "Gravitación", aciertos: 1, items: [{ mide: "Kepler", estado: "bien" }, { mide: "Energía", estado: "mal" }] },
      { nombre: "Ondas", aciertos: 0, items: [{ mide: "Sonido", estado: "nose" }, { mide: "Fase", estado: "mal" }] },
    ],
  });
  anotar("mensaje: total de aciertos", texto.includes("Resultado: 1 de 4 (prueba rápida)."), texto);
  anotar("mensaje: nombre del alumno", texto.includes("Me llamo Ana."));
  anotar("mensaje: lista los fallos", texto.includes("✗ Energía") && texto.includes("✗ Fase"));
  anotar("mensaje: distingue lo que no sabía", texto.includes("? Sonido (no lo sé)"));
  anotar("mensaje: no lista lo acertado", !texto.includes("Kepler"));
  anotar("mensaje: sin nombre no queda línea vacía de más", !redactar({ profesor: "", asignatura: "F", nombre: "", modo: "completa", final: "x", bloques: [] }).includes("Me llamo"));
  return res;
}
