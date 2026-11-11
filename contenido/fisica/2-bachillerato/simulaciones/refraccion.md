---
id: refraccion
titulo: "Refracción: láminas y prisma"
resumen: "Sigue un rayo a través de capas planas o de un prisma: ángulos en cada cara, desplazamiento, tiempo de recorrido y reflexión total."
bloque: optica
modulo: refraccion.js
---

## Cómo usarla

Elige si el rayo atraviesa **capas planas y paralelas** (una lámina, o varias pegadas) o **un prisma**, escribe los índices de refracción y mueve el ángulo de incidencia. En cada superficie se aplica la ley de Snell,

$$n_1 \operatorname{sen}\theta_1 = n_2 \operatorname{sen}\theta_2$$

Los ángulos se miden siempre **respecto a la normal**, que aparece dibujada a trazos.

## Qué estás viendo

- La marcha del rayo con el ángulo en cada medio.
- En el panel: ángulos, camino recorrido dentro de cada capa, tiempo que tarda ($v = c/n$) y, si existe, el ángulo límite.

## Prueba esto

1. **Lámina.** El rayo sale paralelo al de entrada, solo desplazado. Cambia el índice de la lámina: el ángulo de salida no cambia, el desplazamiento sí.
2. **Varias capas.** Con el mismo medio a los dos lados, el ángulo de salida es igual al de entrada pongas las capas que pongas: $n\operatorname{sen}\theta$ se conserva en todo el recorrido.
3. **Reflexión total.** Pon un medio de salida con índice menor que el de la última capa y sube el ángulo de incidencia: llega un momento en que el rayo no sale. Solo puede ocurrir al pasar a un medio de índice menor.
4. **Prisma.** Baja el ángulo de incidencia hasta que el rayo deje de salir por la segunda cara: el panel te da esa incidencia mínima.
5. **El problema de partida** es la lámina de la ordinaria de 2026 (n = 1,7, 3 cm de espesor, incidencia de 48°).
