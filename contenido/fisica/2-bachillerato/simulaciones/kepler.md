---
id: kepler
titulo: "Ley de las áreas y momento angular"
resumen: "Una órbita elíptica dividida en tramos de igual duración: las áreas barridas son iguales y el producto r·v·sen φ no cambia."
bloque: gravitacion
modulo: kepler.js
---

## Qué estás viendo

El astro central está en un **foco** de la elipse, no en el centro. La órbita está dividida en franjas que el cuerpo recorre **en el mismo tiempo**. La franja más intensa es la que está barriendo ahora.

- Cerca del astro las franjas son cortas y anchas; lejos, largas y estrechas. Su **área es la misma**: es la segunda ley de Kepler.
- La **flecha verde** es la velocidad. Crece al acercarse al astro y disminuye al alejarse.
- El **arco naranja** es el ángulo $\varphi$ entre el radio y la velocidad. Solo vale 90° en los dos puntos extremos.

## Por qué ocurre

La fuerza gravitatoria apunta siempre hacia el astro. Una fuerza así no ejerce momento respecto a él, y por eso el **momento angular** se conserva:

$$L = m\,r\,v\,\operatorname{sen}\varphi = \text{cte}$$

Fíjate en la lectura «r · v · sen φ»: $r$ y $v$ cambian todo el rato, pero ese producto no se mueve. El área barrida cada segundo es justo la mitad de ese valor, $\mathrm{d}A/\mathrm{d}t = L/(2m)$, y por eso tampoco cambia.

En los puntos extremos $\operatorname{sen}\varphi = 1$ y queda la relación que se usa en los problemas:

$$r_p\,v_p = r_a\,v_a$$

## Prueba esto

1. **Plutón.** Es la órbita de una pregunta del modelo de examen: periodo de 248 años y excentricidad 0,244. Compara las distancias y velocidades en el perihelio y el afelio con las que obtienes en papel.
2. **Pausa en dos sitios.** Detén el cuerpo cerca del astro y luego lejos, y multiplica $r\cdot v\cdot\operatorname{sen}\varphi$ con tu calculadora.
3. **Excentricidad cero.** La órbita es circular, todas las franjas son iguales y la velocidad es constante.
4. **Cometa Halley.** Con una excentricidad de 0,967 pasa casi todo el periodo lejos del Sol y cruza el perihelio a toda velocidad.
5. **Energías.** La cinética y la potencial cambian a lo largo de la órbita, pero la mecánica se queda fija.
6. **Cambio de órbita.** Carga el satélite Molniya y marca «Dibujar las dos órbitas circulares». En el apogeo va más lento que un satélite en órbita circular de ese radio, así que para quedarse en ella hay que **acelerar**; en el perigeo va más rápido y habría que **frenar**. La energía que hay que aportar es la diferencia de energías mecánicas, $\Delta E = -\dfrac{GMm}{2r} - \left(-\dfrac{GMm}{2a}\right)$.

## Lo que conviene llevarse al examen

- Para hallar las velocidades en perihelio y afelio hacen falta **dos** ecuaciones: conservación del momento angular y conservación de la energía mecánica.
- Las distancias extremas salen del semieje mayor y la excentricidad: $r_p = a(1-e)$ y $r_a = a(1+e)$.
- El semieje mayor se obtiene del periodo con la tercera ley de Kepler.
