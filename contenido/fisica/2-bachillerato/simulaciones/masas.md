---
id: masas
titulo: "Masas puntuales: campo gravitatorio y potencial"
resumen: "Coloca varias masas y un punto para ver el campo gravitatorio de cada una, el campo total, el potencial, el trabajo entre dos puntos y el punto de campo nulo."
bloque: gravitacion
modulo: masas.js
---

## Cómo usarla

Escribe cada masa en kilogramos y su posición, y las coordenadas del punto A donde quieres el campo. Para problemas de trabajo, añade el punto B y la masa que se traslada.

## Qué estás viendo

- Las **flechas de colores** son los campos de cada masa en A. A diferencia de las cargas, **siempre apuntan hacia la masa**: la gravedad solo atrae.
- La **flecha amarilla** es el campo total, suma vectorial de las anteriores.
- El círculo verde marca el punto del segmento que une las dos primeras masas donde el campo se anula.

$$g = G\,\frac{M}{r^2} \qquad V = -G\,\frac{M}{r} \qquad W_{A\to B} = m'\,(V_A - V_B)$$

con $G = 6{,}67\cdot 10^{-11}\ \mathrm{N\,m^2\,kg^{-2}}$.

## Prueba esto

1. **El problema de partida** es de la ordinaria de 2026: 2 kg en el origen y 4 kg en $(4, 0)\ \mathrm{m}$. El campo se anula a 1,66 m de la primera, y en $(0, 2)\ \mathrm{m}$ vale $(1{,}19;\ -3{,}93)\cdot 10^{-11}\ \mathrm{N/kg}$.
2. **Más cerca de la pequeña.** Aumenta una de las masas y mira cómo el punto de campo nulo se desplaza hacia la otra.
3. **Potencial siempre negativo.** Mueve A por el plano: el potencial nunca es positivo, y se hace más negativo cerca de las masas.
4. **Simetría.** Pon dos masas iguales y lleva A a la mediatriz: las componentes paralelas a la línea que las une se cancelan.
