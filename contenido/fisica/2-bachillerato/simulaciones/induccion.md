---
id: induccion
titulo: "Inducción: flujo y fem"
resumen: "Una espira que entra en un campo, que gira, o un campo que cambia con el tiempo: gráficas del flujo y de la fem, y sentido de la corriente inducida."
bloque: electromagnetismo
modulo: induccion.js
---

## Cómo usarla

Elige la situación del enunciado y escribe sus datos. La simulación aplica la ley de Faraday-Lenz,

$$\Phi = N\,B\,S\cos\theta \qquad \varepsilon = -\frac{d\Phi}{dt} \qquad I = \frac{\varepsilon}{R}$$

Mueve el deslizador de tiempo para leer el flujo, la fem y la corriente en cada instante.

## Qué estás viendo

- **Arriba**, el montaje: la espira, el campo (⊗ entra, ⊙ sale) y, cuando hay corriente inducida, su sentido.
- **Gráfica del flujo** $\Phi(t)$ y, debajo, **gráfica de la fem** $\varepsilon(t)$. La fem es, cambiada de signo, la pendiente de la gráfica del flujo.

## Prueba esto

1. **Espira que entra.** Mientras entra, el flujo crece en línea recta y la fem es constante, $|\varepsilon| = B\,L\,v$. Cuando ya está entera dentro, el flujo no cambia y la fem es cero aunque haya campo.
2. **Lenz.** Cambia el sentido del campo: la corriente inducida cambia de sentido. Siempre crea un campo que se opone al cambio de flujo, no al campo.
3. **Campo por tramos.** Es la gráfica $B(t)$ típica del examen: en los tramos inclinados hay fem constante, en los horizontales no hay. Cuanto más inclinado el tramo, mayor fem.
4. **Espira que gira.** El flujo va como un coseno y la fem como un seno: cuando el flujo es máximo la fem es nula, y al revés. La fem máxima es $N\,B\,S\,\omega$.
5. **Más espiras.** Duplica $N$: se duplican el flujo y la fem.
