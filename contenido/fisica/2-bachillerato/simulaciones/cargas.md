---
id: cargas
titulo: "Cargas puntuales: campo, potencial y trabajo"
resumen: "Coloca hasta cuatro cargas y un punto: verás el campo de cada una, el campo total, el potencial, el trabajo entre dos puntos y dónde se anula el campo."
bloque: electromagnetismo
modulo: cargas.js
---

## Cómo usarla

Escribe el valor de cada carga **con su signo** y su posición, tal como las da el enunciado, y las coordenadas del punto A. Elige antes la unidad de las posiciones (m, cm, mm o nm): es la que usa el dibujo, pero todos los resultados salen en unidades del SI.

Para problemas de trabajo, añade el punto B y la carga que se traslada.

## Qué estás viendo

- Las **flechas de colores** que salen de A son los campos que crea cada carga, con el color de su carga. Salen de las cargas positivas y entran en las negativas.
- La **flecha amarilla** es el campo total: la suma vectorial de las anteriores. Sus componentes aparecen en las lecturas.
- Las flechas grises pequeñas indican hacia dónde apunta el campo total en cada zona del plano.
- El círculo verde marca el punto de la recta que une las dos primeras cargas donde el campo se anula.

Las expresiones que se usan son las del formulario:

$$E = K\,\frac{|q|}{r^2} \qquad V = K\,\frac{q}{r} \qquad W_{A\to B} = q'\,(V_A - V_B)$$

con $K = 9\cdot 10^{9}\ \mathrm{N\,m^2\,C^{-2}}$.

## Prueba esto

1. **El problema de partida** es del modelo de 2027: $-2\ \mathrm{nC}$ en $(-5, 0)$ y $+2\ \mathrm{nC}$ en $(5, 0)$, con A en $(5, 4)$ y B en $(0, 4)$. Compara con tu cálculo: $\vec E = (-0{,}144;\ 1{,}07)\ \mathrm{N/C}$, $V_A = 2{,}83\ \mathrm{V}$ y $W = 8{,}49\cdot 10^{-9}\ \mathrm{J}$.
2. **Campo nulo, potencial no nulo.** Pon dos cargas iguales del mismo signo y lleva A al punto medio: el campo se anula, pero el potencial es el doble del de una sola.
3. **Potencial nulo, campo no nulo.** Cambia el signo de una de ellas: en el punto medio el potencial es cero y el campo no.
4. **Dónde se anula el campo.** Con cargas del mismo signo, el punto está entre ellas y más cerca de la menor. Con signos opuestos, está fuera del segmento, del lado de la menor en valor absoluto.
5. **Signo del trabajo.** Arrastra B y mira cuándo el traslado lo hace el campo y cuándo necesita una fuerza externa.
