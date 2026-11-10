---
bloque: ondas
resumen: "Movimiento armónico simple, ecuación de la onda armónica, energía e intensidad, sonido y ondas estacionarias."
formulas:
  - grupo: "Movimiento armónico simple"
    lista:
      - nombre: "Posición"
        tex: 'x(t) = A\cos(\omega t + \varphi_0)'
        nota: 'También puede escribirse con seno; solo cambia la fase inicial.'
      - nombre: "Velocidad"
        tex: 'v(t) = -A\,\omega\operatorname{sen}(\omega t + \varphi_0) \qquad v_\text{máx} = A\,\omega'
      - nombre: "Aceleración"
        tex: 'a = -\omega^2 x \qquad a_\text{máx} = A\,\omega^2'
      - nombre: "Frecuencia angular"
        tex: '\omega = \dfrac{2\pi}{T} = 2\pi f'
      - nombre: "Velocidad en función de la posición"
        tex: 'v = \pm\,\omega\sqrt{A^2 - x^2}'
      - nombre: "Masa unida a un muelle"
        tex: '\omega = \sqrt{\dfrac{k}{m}} \qquad T = 2\pi\sqrt{\dfrac{m}{k}}'
      - nombre: "Péndulo simple"
        tex: 'T = 2\pi\sqrt{\dfrac{L}{g}}'
        nota: 'Para oscilaciones pequeñas. No depende de la masa.'
      - nombre: "Energía"
        tex: 'E_m = \dfrac12 k A^2 = \dfrac12 m v^2 + \dfrac12 k x^2'
  - grupo: "Onda armónica"
    lista:
      - nombre: "Ecuación de onda"
        tex: 'y(x,t) = A\operatorname{sen}(\omega t - kx + \varphi_0)'
        nota: 'Signo menos: avanza hacia $x$ positivas. Signo más: hacia $x$ negativas.'
      - nombre: "Número de onda"
        tex: 'k = \dfrac{2\pi}{\lambda}'
      - nombre: "Velocidad de propagación"
        tex: 'v = \lambda f = \dfrac{\lambda}{T} = \dfrac{\omega}{k}'
        nota: 'Depende del medio, no de la amplitud ni de la frecuencia.'
      - nombre: "Velocidad de vibración"
        tex: 'v_y = \dfrac{\partial y}{\partial t} = A\,\omega\cos(\omega t - kx + \varphi_0)'
        nota: 'Es la velocidad de un punto del medio. No confundir con la de propagación.'
      - nombre: "Diferencia de fase"
        tex: '\Delta\varphi = k\,\Delta x \qquad \Delta\varphi = \omega\,\Delta t'
        nota: 'Entre dos puntos en el mismo instante, y en un mismo punto entre dos instantes.'
  - grupo: "Energía, intensidad y sonido"
    lista:
      - nombre: "Intensidad"
        tex: 'I = \dfrac{P}{S}'
        nota: 'Potencia por unidad de superficie perpendicular a la propagación ($\mathrm{W\,m^{-2}}$).'
      - nombre: "Foco puntual (ondas esféricas)"
        tex: 'I = \dfrac{P}{4\pi r^2}'
        nota: 'La intensidad cae como $1/r^2$ y la amplitud como $1/r$.'
      - nombre: "Dos distancias al mismo foco"
        tex: '\dfrac{I_1}{I_2} = \dfrac{r_2^2}{r_1^2}'
      - nombre: "Nivel de intensidad sonora"
        tex: '\beta = 10\log\dfrac{I}{I_0}'
        nota: 'En decibelios, con $I_0 = 10^{-12}\ \mathrm{W\,m^{-2}}$.'
      - nombre: "Efecto Doppler"
        tex: 'f^{\prime} = f\,\dfrac{v \pm v_\text{obs}}{v \mp v_\text{foco}}'
        nota: 'Signos de arriba cuando se acercan (la frecuencia percibida aumenta); los de abajo cuando se alejan.'
  - grupo: "Interferencia y ondas estacionarias"
    lista:
      - nombre: "Interferencia constructiva"
        tex: '\Delta r = n\,\lambda'
        nota: 'Focos en fase; $n = 0, 1, 2\ldots$'
      - nombre: "Interferencia destructiva"
        tex: '\Delta r = (2n + 1)\,\dfrac{\lambda}{2}'
      - nombre: "Onda estacionaria"
        tex: 'y(x,t) = 2A\operatorname{sen}(kx)\cos(\omega t)'
        nota: 'Nodos consecutivos separados $\lambda/2$; de nodo a vientre, $\lambda/4$.'
      - nombre: "Cuerda fija por los dos extremos"
        tex: 'L = n\,\dfrac{\lambda}{2} \qquad f_n = n\,\dfrac{v}{2L}'
        nota: 'También vale para un tubo abierto por los dos extremos.'
      - nombre: "Tubo cerrado por un extremo"
        tex: 'L = (2n - 1)\,\dfrac{\lambda}{4} \qquad f_n = (2n - 1)\,\dfrac{v}{4L}'
        nota: 'Solo armónicos impares; $n = 1, 2, 3\ldots$'
---

Una onda es una perturbación que se propaga transportando **energía, pero no materia**. Cada punto del medio se limita a oscilar alrededor de su posición de equilibrio, y esa oscilación es un movimiento armónico simple. Por eso el bloque empieza por ahí.

## Movimiento armónico simple

Un cuerpo describe un movimiento armónico simple (MAS) cuando la fuerza que lo devuelve al equilibrio es proporcional a lo que se ha separado: $F = -kx$. La posición es entonces una función seno o coseno del tiempo:

$$x(t) = A\cos(\omega t + \varphi_0)$$

- $A$ es la **amplitud**: la separación máxima.
- $\omega$ es la **frecuencia angular**, relacionada con el periodo por $\omega = 2\pi/T$.
- $\varphi_0$ es la **fase inicial**: se obtiene de la posición (y el sentido de la velocidad) en $t = 0$.

Derivando se obtienen la velocidad y la aceleración. Lo importante es dónde son máximas:

| | Extremos ($x = \pm A$) | Centro ($x = 0$) |
|---|---|---|
| Velocidad | cero | máxima, $A\omega$ |
| Aceleración | máxima, $A\omega^2$ | cero |
| Energía cinética | cero | máxima |
| Energía potencial | máxima | cero |

La energía mecánica se conserva y vale $\tfrac12 kA^2$. Depende del **cuadrado** de la amplitud: si la amplitud se duplica, la energía se multiplica por cuatro.

Para un muelle, $\omega = \sqrt{k/m}$. Para un péndulo que oscila poco, $T = 2\pi\sqrt{L/g}$.

## Onda armónica

Si un foco vibra con un MAS, la perturbación se propaga y cada punto repite el movimiento del foco con un retraso. El estado de un punto que está en la posición $x$ en el instante $t$ es:

$$y(x,t) = A\operatorname{sen}(\omega t - kx + \varphi_0)$$

La función depende de dos variables, y eso da dos periodicidades:

- en el **tiempo**: cada punto repite su movimiento cada periodo $T$;
- en el **espacio**: la forma de la onda se repite cada longitud de onda $\lambda$.

El número de onda $k = 2\pi/\lambda$ es al espacio lo que $\omega$ es al tiempo. La velocidad de propagación las relaciona: $v = \lambda f = \omega/k$.

Hay dos velocidades distintas y el examen juega con ello:

- la **velocidad de propagación**, $v = \lambda f$, constante, que depende del medio;
- la **velocidad de vibración** de cada punto, $\partial y/\partial t$, que cambia con el tiempo y tiene un máximo $A\omega$.

El signo entre $\omega t$ y $kx$ da el sentido: signos opuestos, la onda avanza hacia las $x$ positivas; signos iguales, hacia las negativas.

Dos puntos separados una distancia $\Delta x$ tienen una diferencia de fase $\Delta\varphi = k\,\Delta x$. Están **en fase** si la distancia es un número entero de longitudes de onda, y en **oposición de fase** si es un número impar de medias longitudes de onda.

## Energía e intensidad

La intensidad es la energía que atraviesa cada segundo una superficie de un metro cuadrado perpendicular a la propagación: $I = P/S$.

Un foco puntual emite en todas direcciones, y su potencia se reparte sobre esferas cada vez mayores:

$$I = \frac{P}{4\pi r^2}$$

Al doble de distancia, la intensidad es la cuarta parte. Como la intensidad es proporcional al cuadrado de la amplitud, la amplitud cae como $1/r$.

## Sonido

El sonido es una onda mecánica longitudinal: necesita un medio y las partículas vibran en la dirección de propagación. El oído no responde de forma lineal a la intensidad, así que se usa una escala logarítmica, el **nivel de intensidad sonora**:

$$\beta = 10\log\frac{I}{I_0} \qquad I_0 = 10^{-12}\ \mathrm{W\,m^{-2}}$$

Tres consecuencias que evitan muchos errores:

- Los decibelios **no se suman**. Con varios focos se suman las intensidades y después se calcula el nivel.
- Duplicar la intensidad sube el nivel unos 3 dB; multiplicarla por diez, 10 dB.
- Para ir de decibelios a intensidad: $I = I_0\cdot 10^{\beta/10}$.

El **efecto Doppler** es el cambio de frecuencia que percibe un observador cuando él o el foco se mueven: más aguda al acercarse y más grave al alejarse.

## Interferencia y ondas estacionarias

Cuando dos ondas coinciden en un punto, sus elongaciones se suman. Con dos focos que emiten en fase, lo que ocurre en cada punto depende de la **diferencia de caminos**:

- un número entero de longitudes de onda: llegan en fase y se refuerzan (interferencia constructiva);
- un número impar de medias longitudes de onda: llegan en oposición y se anulan (destructiva).

Una **onda estacionaria** se forma al superponerse dos ondas iguales que viajan en sentidos contrarios, por ejemplo una onda y su reflexión. Ya no se propaga: hay puntos que nunca se mueven (**nodos**) y puntos que vibran con amplitud máxima (**vientres**). La distancia entre dos nodos consecutivos es $\lambda/2$.

En una cuerda fija por los dos extremos tiene que haber un nodo en cada extremo, y solo caben las ondas con $L = n\lambda/2$. De ahí salen las frecuencias permitidas, los **armónicos**: $f_n = n\,v/(2L)$. En un tubo con un extremo cerrado hay un nodo en el extremo cerrado y un vientre en el abierto, y solo aparecen los armónicos impares.

## Cómo plantear un problema

1. Si te dan la ecuación, compárala con $A\operatorname{sen}(\omega t - kx + \varphi_0)$ e identifica $A$, $\omega$ y $k$. De ahí salen $T$, $f$, $\lambda$ y $v$.
2. Si te piden la ecuación, calcula $A$, $\omega$ y $k$, elige el signo según el sentido y ajusta $\varphi_0$ con la condición inicial.
3. Velocidad o aceleración de un punto: deriva respecto al tiempo.
4. Sonido: trabaja siempre con intensidades y pasa a decibelios al final.
