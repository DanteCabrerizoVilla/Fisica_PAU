---
id: desintegracion
titulo: "Desintegración radiactiva"
resumen: "Introduce el periodo, la vida media o la constante, y la masa o la actividad de la muestra: evolución en el tiempo, con todas las conversiones de unidades."
bloque: fisica-moderna
modulo: desintegracion.js
---

## Cómo usarla

1. Elige **qué dato de ritmo** da tu enunciado (periodo de semidesintegración, vida media o constante) y escríbelo con su unidad.
2. Elige **qué se sabe de la muestra**: su actividad, su masa o su número de núcleos. Con la masa molar, la simulación calcula las otras dos.
3. Mueve el **tiempo** o escríbelo.

Los números se escriben con su potencia de diez: $2{,}64\cdot 10^{9}$ es 2,64 y 9.

## Qué estás viendo

- Los **puntos** representan núcleos. Cada uno se desintegra en un instante al azar: no se sabe cuál será el siguiente, pero sí cuántos quedarán.
- La **curva** es la ley de desintegración. Cada periodo $T_{1/2}$ la muestra se reduce a la mitad.

$$N = N_0\,e^{-\lambda t} \qquad A = \lambda\,N \qquad T_{1/2} = \frac{\ln 2}{\lambda} \qquad \tau = \frac{1}{\lambda}$$

## Donde se pierden los puntos

- **Unidades de $\lambda$.** La simulación la da en $\mathrm{s^{-1}}$ y en $\text{días}^{-1}$. Para pasar de actividad (en becquerel) a número de núcleos hace falta en $\mathrm{s^{-1}}$. En el exponente, $\lambda$ y $t$ deben ir en la misma unidad.
- **Periodo y vida media no son lo mismo.** Cambia el dato de ritmo de uno a otro y verás que $\tau$ es un 44 % mayor que $T_{1/2}$.
- **Lo que queda y lo que se ha desintegrado.** La ley da lo que queda. Si te piden los núcleos desintegrados, es la diferencia.

## Prueba esto

1. **El problema de partida** es del modelo de 2027: cobalto-60, con periodo de 1925,2 días y actividad inicial de $2{,}64\cdot 10^{9}\ \mathrm{Bq}$. Al cabo de un año quedan $2{,}31\cdot 10^{9}\ \mathrm{Bq}$, y la masa inicial es de $6{,}31\cdot 10^{-5}\ \mathrm{g}$.
2. **Tras $n$ periodos** queda $1/2^n$: pon el tiempo en 1, 2 y 3 periodos.
3. **¿Cuánto tarda?** Escribe una actividad objetivo y compara el tiempo con tu cálculo.
