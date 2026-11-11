---
id: carga-campos
titulo: "Carga en campos magnético y eléctrico"
resumen: "Lanza una partícula cargada en un campo magnético: radio, periodo y sentido de giro. Añade un campo eléctrico y tendrás el selector de velocidades."
bloque: electromagnetismo
modulo: carga-campos.js
---

## Cómo usarla

Elige la partícula (o escribe su masa en u y su carga en unidades de $e$, con signo), su velocidad y el campo magnético. La carga entra moviéndose hacia la derecha, perpendicular al campo. La simulación aplica la fuerza de Lorentz,

$$\vec F = q\,(\vec E + \vec v \times \vec B) \qquad R = \frac{m\,v}{|q|\,B} \qquad T = \frac{2\pi m}{|q|\,B}$$

## Qué estás viendo

- El plano del movimiento visto desde arriba. Las cruces indican un campo que entra en el papel y los puntos, uno que sale.
- En verde la **velocidad** y en naranja la **fuerza** sobre la carga. Con solo campo magnético son siempre perpendiculares: la fuerza cambia la dirección, no la rapidez.

## Prueba esto

1. **Signo de la carga.** Cambia la carga de positiva a negativa: gira hacia el otro lado. Lo mismo ocurre al invertir el sentido de $\vec B$.
2. **Más velocidad.** Duplica la velocidad: el radio se duplica, pero el periodo no cambia. El periodo no depende de $v$.
3. **Espectrómetro de masas.** Cambia solo la masa: el radio es proporcional a ella, y por eso iones distintos caen en puntos distintos.
4. **Selector de velocidades.** Añade un campo eléctrico. La carga solo sigue recta si $v = E/B$; la simulación te da esa velocidad. Si va más rápida gana la fuerza magnética; si va más lenta, la eléctrica.
5. **Acelerada desde el reposo.** Abajo tienes la velocidad que alcanzaría con una diferencia de potencial $\Delta V$: $|q|\,\Delta V = \tfrac12 m v^2$. También la longitud de onda de De Broglie, $\lambda = h/(m v)$.
6. **El problema de partida** es el ion $\mathrm{Ca^{2+}}$ del espectrómetro de la extraordinaria de 2025.

La velocidad se trata con las fórmulas clásicas, que es lo que se pide en estos problemas; para velocidades cercanas a la de la luz, usa la calculadora relativista.
