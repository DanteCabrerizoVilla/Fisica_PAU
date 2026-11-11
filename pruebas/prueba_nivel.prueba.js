// Corrección, sorteo de variantes e informe de la prueba de nivel.

import { corregir, huella, informe, sortear, valorar } from "../static/js/prueba-nivel.js";

export async function probar() {
  const ref = await (await fetch("prueba_nivel.ref.json")).json();
  const res = [];
  const anotar = (nombre, ok, detalle = "") => res.push({ nombre, ok, detalle });

  anotar("prueba de nivel: 30 preguntas", ref.preguntas === 30, `${ref.preguntas}`);
  anotar("prueba de nivel: al menos tres variantes por pregunta", ref.casos.length >= 3 * ref.preguntas, `${ref.casos.length}`);
  for (const c of ref.casos) {
    anotar(`prueba de nivel ${c.id}: la huella coincide con la de Python`, huella(`${c.id}|${c.correcta}|nivel`) === c.clave);
    const estados = [0, 1, 2, 3].map((i) => corregir(c.id, String(i), c.clave));
    anotar(`prueba de nivel ${c.id}: solo una opción se da por buena`,
      estados.filter((e) => e === "bien").length === 1 && estados[c.correcta] === "bien", estados.join(","));
    anotar(`prueba de nivel ${c.id}: «No lo sé» no cuenta como acierto`, corregir(c.id, "x", c.clave) === "nose" && corregir(c.id, null, c.clave) === "nose");
  }

  anotar("valoración: 5 de 6 → bien", valorar(5, 6).clave === "bien");
  anotar("valoración: 4 de 6 → regular", valorar(4, 6).clave === "regular");
  anotar("valoración: 3 de 6 → regular", valorar(3, 6).clave === "regular");
  anotar("valoración: 2 de 6 → mal", valorar(2, 6).clave === "mal");

  // Sorteo: una variante por pregunta, y todas las variantes pueden salir.
  const grupos = [["a1", "a2", "a3"], ["b1", "b2", "b3"], ["c1"]];
  anotar("sorteo: una por pregunta, en orden", sortear(grupos, () => 0).join() === "a1,b1,c1");
  anotar("sorteo: el extremo superior no se sale", sortear(grupos, () => 0.999999).join() === "a3,b3,c1");
  const vistas = new Set();
  let semilla = 7;
  const azar = () => ((semilla = (semilla * 16807) % 2147483647) / 2147483647);
  for (let i = 0; i < 200; i++) for (const x of sortear(grupos, azar)) vistas.add(x);
  anotar("sorteo: salen todas las variantes", vistas.size === 7, [...vistas].join());
  let distintas = 0;
  for (let i = 0; i < 50; i++) if (sortear(grupos).join() !== sortear(grupos).join()) distintas++;
  anotar("sorteo: dos alumnos no suelen recibir la misma prueba", distintas > 25, `${distintas}/50`);

  const datos = informe({
    correo: "ana@ejemplo.com", nombre: "Ana", publicidad: false, asignatura: "Física (PAU Madrid)",
    bloques: [
      { nombre: "Gravitación", aciertos: 1, items: [{ id: "grav-1b", mide: "Kepler", estado: "bien" }, { id: "grav-2a", mide: "Energía", estado: "mal" }] },
      { nombre: "Ondas", aciertos: 0, items: [{ id: "onda-1c", mide: "Sonido", estado: "nose" }, { id: "onda-2a", mide: "Fase", estado: "mal" }] },
    ],
  });
  anotar("informe: correo y nombre", datos.correo === "ana@ejemplo.com" && datos.nombre === "Ana");
  anotar("informe: total de aciertos", datos.aciertos === 1 && datos.total === 4);
  anotar("informe: sin marcar la casilla no hay consentimiento", datos.publicidad === false);
  anotar("informe: fallos por bloque", datos.bloques[0].falla.join() === "Energía" && datos.bloques[1].falla.join() === "Fase");
  anotar("informe: lo que no sabía va aparte", datos.bloques[1].no_sabe.join() === "Sonido" && datos.bloques[0].no_sabe.length === 0);
  anotar("informe: lo acertado no aparece como debilidad", !JSON.stringify(datos.bloques).includes("Kepler"));
  anotar("informe: variantes que le han tocado", datos.variantes === "grav-1b grav-2a onda-1c onda-2a");
  return res;
}
