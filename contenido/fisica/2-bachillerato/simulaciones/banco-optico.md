---
id: banco-optico
titulo: "Banco óptico: lentes y espejos"
resumen: "Una lente, dos lentes o un espejo esférico: coloca el objeto, mira el trazado de rayos y compara la posición y el tamaño de la imagen con tu cálculo."
bloque: optica
modulo: banco-optico.js
---

## Cómo usarla

Elige el sistema óptico, escribe la distancia focal **con su signo** y coloca el objeto. La simulación dibuja los rayos principales y da la posición de la imagen, el aumento y su naturaleza con el mismo criterio de signos del examen (DIN).

- La **distancia del objeto** se escribe en positivo; en los resultados aparece como $s$ negativa, porque el objeto está a la izquierda.
- Con **dos lentes**, la posición de la imagen final se mide desde la segunda lente, igual que en el cálculo por pasos.
- Si la imagen se va muy lejos, el dibujo lo avisa y los datos siguen siendo correctos.

## Qué estás viendo

- La flecha blanca es el **objeto**; la amarilla, la **imagen**.
- Las líneas continuas son **rayos de luz**. Las discontinuas son **prolongaciones**: por ahí no pasa luz, pero indican de dónde parece venir.
- Si los rayos se cruzan de verdad, la imagen es **real**. Si solo se cruzan las prolongaciones, es **virtual**.

Las ecuaciones que se usan:

| | Posición | Aumento |
|---|---|---|
| Lente delgada | $\dfrac{1}{s'} - \dfrac{1}{s} = \dfrac{1}{f'}$ | $M = \dfrac{s'}{s}$ |
| Espejo esférico | $\dfrac{1}{s'} + \dfrac{1}{s} = \dfrac{1}{f}$ | $M = -\dfrac{s'}{s}$ |

## Prueba esto

1. **Lente convergente.** Arrastra el objeto desde lejos hacia la lente. Más allá de $2f'$ la imagen es menor; entre $2f'$ y $f'$, mayor; al cruzar el foco salta al otro lado y se vuelve virtual y derecha: es una lupa.
2. **Justo en el foco.** Pon el objeto a una distancia igual a la focal: los rayos salen paralelos y la imagen se forma en el infinito.
3. **Lente divergente.** Cambia el signo de la focal. Muevas como muevas el objeto, la imagen es virtual, derecha y menor.
4. **Espejo cóncavo y convexo.** Con focal negativa (cóncavo) ocurre lo mismo que con la lente convergente, pero la imagen real se forma delante del espejo. Con focal positiva (convexo), siempre virtual y menor.
5. **Dos lentes.** El montaje por defecto es el de la extraordinaria de 2026: convergente de 15 cm, divergente de −20 cm, separadas 60 cm y objeto a 30 cm. La imagen final sale a −12 cm de la segunda lente.
