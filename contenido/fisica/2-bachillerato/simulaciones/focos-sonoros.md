---
id: focos-sonoros
titulo: "Focos sonoros: intensidad y nivel"
resumen: "Coloca hasta tres focos y un observador: intensidad de cada uno, intensidad total, nivel en decibelios y el punto donde dos focos se oyen igual."
bloque: ondas
modulo: focos-sonoros.js
---

## Cómo usarla

De cada foco puedes dar la **potencia** o el **nivel que produce a cierta distancia**, que es como suelen venir los datos. Arrastra los focos y el observador, o escribe sus coordenadas. La simulación usa

$$I = \frac{P}{4\pi r^2} \qquad \beta = 10\,\log\frac{I}{I_0} \qquad I_0 = 10^{-12}\ \mathrm{W\,m^{-2}}$$

## Qué estás viendo

- Los círculos alrededor de cada foco son frentes de onda; el sonido se reparte sobre esferas cada vez mayores y por eso la intensidad cae con $1/r^2$.
- En el panel, la intensidad que llega de cada foco, la **suma de intensidades** y el nivel total.

## Prueba esto

1. **Los decibelios no se suman.** Pon dos focos iguales a la misma distancia del observador: el nivel sube solo 3 dB, porque lo que se duplica es la intensidad.
2. **Doble de distancia.** Aleja el observador al doble de distancia de un único foco: la intensidad se divide entre 4 y el nivel baja 6 dB.
3. **Diez fuentes iguales.** Usa "fuentes iguales en ese punto" con 10: el nivel sube exactamente 10 dB.
4. **Punto de igual intensidad.** Con dos focos de distinta potencia, el panel te da el punto del segmento que los une donde ambos se reciben con la misma intensidad: $P_1/r_1^2 = P_2/r_2^2$.
5. **El problema de partida** es el de dos focos de la extraordinaria de 2024.
