---
id: orbita-circular
titulo: "Órbita circular: comprueba tu problema"
resumen: "Escribe los datos del enunciado (astro, altura o periodo, masa del satélite) y compara tus resultados de velocidad, periodo y energías."
bloque: gravitacion
modulo: orbita-circular.js
---

## Cómo usarla

Resuelve primero el problema en papel. Después escribe aquí los datos tal como los da el enunciado y compara.

- **Astro central.** Elige uno de la lista o escribe su masa y su radio. Los valores de la lista son los que suelen darse en el examen; si tu enunciado da otros, cámbialos.
- **Dato de la órbita.** Según el problema te darán la altura, el radio de la órbita o el periodo. Elige cuál y escríbelo; puedes cambiar la unidad.
- Los números se escriben con su potencia de diez: $5{,}97\cdot 10^{24}$ es 5,97 y 24.

Todos los resultados salen en unidades del SI y con tres cifras, igual que en una solución de examen.

## Qué estás viendo

- La **flecha verde** es la velocidad: siempre tangente a la órbita y de módulo constante.
- La **flecha naranja** es la fuerza gravitatoria: apunta al centro del astro y es la fuerza centrípeta.
- El tramo amarillo del radio es la altura $h$. La distancia que entra en las fórmulas es $r = R + h$, desde el centro.

El astro y la órbita están dibujados a escala entre sí.

## De dónde sale cada resultado

| Resultado | Expresión |
|---|---|
| Velocidad orbital | $v = \sqrt{GM/r}$ |
| Periodo | $T = 2\pi r/v$ |
| Energía mecánica | $E_m = -\dfrac{GMm}{2r}$ |
| Energía para escapar desde la órbita | $-E_m$ |
| Velocidad de escape desde la superficie | $v_e = \sqrt{2GM/R}$ |
| Energía para ponerlo en órbita | $E_m - E_{p,\text{suelo}}$ |

## Prueba esto

1. **Mira las barras de energía.** En cualquier órbita circular la cinética es la mitad de la potencial cambiada de signo, y la mecánica es negativa.
2. **Sube la altura.** La velocidad baja y el periodo crece, pero la energía mecánica aumenta (se hace menos negativa): subir de órbita cuesta energía.
3. **Cambia la masa del satélite.** La velocidad y el periodo no cambian; las energías sí.
4. **Satélite geoestacionario.** Elige «El periodo» y escribe 24 h. Sale un radio de unos 42 000 km desde el centro de la Tierra.
