---
bloque: gravitacion
resumen: "Fuerza y campo gravitatorio, energía potencial, satélites en órbita circular, velocidad de escape y leyes de Kepler."
formulas:
  - grupo: "Fuerza, campo y potencial"
    lista:
      - nombre: "Ley de gravitación universal"
        tex: 'F = G\,\dfrac{M\,m}{r^2}'
        nota: 'Siempre atractiva. $r$ es la distancia entre los **centros**.'
      - nombre: "Campo gravitatorio"
        tex: 'g = G\,\dfrac{M}{r^2}'
        nota: 'Apunta hacia la masa que lo crea. Con varias masas se suman los vectores.'
      - nombre: "Energía potencial"
        tex: 'E_p = -G\,\dfrac{M\,m}{r}'
        nota: 'Cero en el infinito y negativa a cualquier distancia finita.'
      - nombre: "Potencial gravitatorio"
        tex: 'V = -G\,\dfrac{M}{r}'
        nota: 'Es un escalar: con varias masas se suman los valores, sin vectores.'
      - nombre: "Trabajo del campo"
        tex: 'W_{A\to B} = -\Delta E_p = m\,(V_A - V_B)'
        nota: 'No depende del camino. Positivo si la masa se mueve a favor del campo.'
  - grupo: "Satélite en órbita circular"
    lista:
      - nombre: "Velocidad orbital"
        tex: 'v = \sqrt{\dfrac{G\,M}{r}}'
        nota: 'Sale de igualar la fuerza gravitatoria con la centrípeta. No depende de la masa del satélite.'
      - nombre: "Periodo"
        tex: 'T = \dfrac{2\pi r}{v} = 2\pi\sqrt{\dfrac{r^3}{G\,M}}'
      - nombre: "Energía cinética"
        tex: 'E_c = \dfrac{1}{2}\,m\,v^2 = \dfrac{G\,M\,m}{2r}'
      - nombre: "Energía mecánica"
        tex: 'E_m = E_c + E_p = -\dfrac{G\,M\,m}{2r}'
        nota: 'Negativa: el satélite está ligado al planeta.'
  - grupo: "Escape y cambios de órbita"
    lista:
      - nombre: "Velocidad de escape"
        tex: 'v_e = \sqrt{\dfrac{2\,G\,M}{r}}'
        nota: 'Desde un punto a distancia $r$ del centro, partiendo del reposo respecto al planeta. Sale de $E_m = 0$.'
      - nombre: "Energía para cambiar de órbita"
        tex: '\Delta E = E_{m,\text{final}} - E_{m,\text{inicial}}'
        nota: 'Para escapar desde una órbita, la energía final es cero: $\Delta E = -E_m$.'
  - grupo: "Kepler y momento angular"
    lista:
      - nombre: "Momento angular"
        tex: 'L = m\,r\,v\,\operatorname{sen}\varphi'
        nota: '$\varphi$ es el ángulo entre $\vec r$ y $\vec v$. Se conserva porque la fuerza es central.'
      - nombre: "Perihelio y afelio"
        tex: 'r_p\,v_p = r_a\,v_a'
        nota: 'En esos dos puntos la velocidad es perpendicular al radio.'
      - nombre: "Ley de las áreas"
        tex: '\dfrac{\mathrm{d}A}{\mathrm{d}t} = \dfrac{L}{2m} = \text{cte}'
      - nombre: "Tercera ley de Kepler"
        tex: '\dfrac{T^2}{a^3} = \dfrac{4\pi^2}{G\,M}'
        nota: '$a$ es el semieje mayor; en una órbita circular, el radio.'
      - nombre: "Distancias extremas de la elipse"
        tex: 'r_p = a\,(1 - e) \qquad r_a = a\,(1 + e)'
        nota: '$e$ es la excentricidad; $r_p + r_a = 2a$.'
---

Casi todos los problemas de gravitación del examen se resuelven con dos ideas: **la fuerza gravitatoria hace de fuerza centrípeta** en las órbitas circulares, y **la energía mecánica se conserva** cuando solo actúa la gravedad. En las órbitas elípticas se añade una tercera: **el momento angular se conserva**.

## Fuerza y campo gravitatorio

Dos masas se atraen con una fuerza proporcional al producto de las masas e inversamente proporcional al cuadrado de la distancia que separa sus centros:

$$F = G\,\frac{M\,m}{r^2}$$

El **campo gravitatorio** en un punto es la fuerza por unidad de masa que sentiría un cuerpo colocado allí. Para una masa $M$:

$$g = G\,\frac{M}{r^2}$$

Es un vector que apunta hacia $M$. En la superficie de un planeta de radio $R$ vale $g_0 = GM/R^2$, y a una altura $h$ hay que usar $r = R + h$. Si doblas la distancia al centro, el campo se divide por cuatro.

Cuando hay varias masas, el campo total es la **suma vectorial** de los campos de cada una. En la práctica: dibuja cada vector, descomponlo en $x$ e $y$, y suma por componentes.

## Energía potencial y potencial

La fuerza gravitatoria es conservativa, así que se le puede asociar una energía potencial. Tomando el cero en el infinito:

$$E_p = -G\,\frac{M\,m}{r}$$

El signo menos no es un adorno. Significa que la masa $m$ está «atrapada»: para llevarla al infinito hay que darle energía. Cuanto más cerca de $M$, más negativa es $E_p$.

La expresión $E_p = m g h$ que usabas en cursos anteriores solo vale cerca de la superficie, donde $g$ casi no cambia. En este bloque, con alturas de cientos de kilómetros, hay que usar siempre la expresión general.

El **potencial** es la energía potencial por unidad de masa, $V = -GM/r$. Es un escalar, y por eso con varias masas se suma directamente, sin descomponer nada. El trabajo que hace el campo cuando una masa $m$ va de A a B es:

$$W_{A\to B} = -\Delta E_p = m\,(V_A - V_B)$$

Si el resultado es positivo, el campo hace el trabajo por sí solo; si es negativo, hace falta una fuerza externa.

## Satélites en órbita circular

En una órbita circular la única fuerza es la gravitatoria, y es justo la fuerza centrípeta que hace falta para girar:

$$G\,\frac{M\,m}{r^2} = m\,\frac{v^2}{r}
\quad\Longrightarrow\quad
v = \sqrt{\frac{G\,M}{r}}$$

De aquí sale casi todo lo demás:

- La velocidad **no depende de la masa del satélite**, solo de la del planeta y del radio de la órbita.
- Cuanto más alta es la órbita, más despacio va el satélite y más tarda en dar la vuelta.
- El periodo es $T = 2\pi r / v$. Si sustituyes $v$, llegas a la tercera ley de Kepler, $T^2 = 4\pi^2 r^3 / (GM)$.

Las energías en la órbita circular guardan una relación fija que conviene saber de memoria:

$$E_c = \frac{G\,M\,m}{2r}
\qquad
E_p = -\frac{G\,M\,m}{r}
\qquad
E_m = -\frac{G\,M\,m}{2r}$$

La cinética es la mitad de la potencial cambiada de signo, y la mecánica es la mitad de la potencial. Un satélite **geoestacionario** es simplemente uno cuyo periodo es de 24 horas y que gira sobre el ecuador: con $T$ se despeja $r$ de la tercera ley.

> Para pasar a una órbita más alta hay que **dar** energía al satélite ($E_m$ se hace menos negativa), aunque en la órbita alta acabe yendo más despacio.

## Velocidad de escape

Escapar significa llegar al infinito sin velocidad, es decir, con energía mecánica cero. Si un cuerpo parte en reposo respecto al planeta desde una distancia $r$ del centro:

$$\frac{1}{2}\,m\,v_e^2 - G\,\frac{M\,m}{r} = 0
\quad\Longrightarrow\quad
v_e = \sqrt{\frac{2\,G\,M}{r}}$$

Hay dos situaciones de examen y no son la misma:

- **Desde la superficie**: $r = R$ y se obtiene la velocidad de escape del planeta.
- **Desde una órbita**: el satélite ya tiene energía cinética. Lo que se pide suele ser la energía que falta para llegar a cero, que es $\Delta E = -E_m = GMm/(2r)$.

## Leyes de Kepler y momento angular

1. **Órbitas elípticas.** Los planetas describen elipses con el Sol en uno de los focos. El punto más cercano es el perihelio y el más lejano, el afelio.
2. **Ley de las áreas.** El radio que une el Sol con el planeta barre áreas iguales en tiempos iguales. Por eso el planeta va más rápido cerca del Sol.
3. **Ley de los periodos.** $T^2$ es proporcional a $a^3$, con la misma constante para todos los cuerpos que giran en torno al mismo astro.

La segunda ley es la conservación del **momento angular**. La fuerza gravitatoria apunta siempre hacia el Sol, así que no ejerce momento respecto a él y $L$ no cambia:

$$L = m\,r\,v\,\operatorname{sen}\varphi = \text{cte}$$

En el perihelio y el afelio la velocidad es perpendicular al radio ($\operatorname{sen}\varphi = 1$), y queda la relación que más se usa:

$$r_p\,v_p = r_a\,v_a$$

Con esa ecuación y la conservación de la energía mecánica entre los dos puntos se obtienen las dos velocidades. Las distancias salen del semieje mayor y la excentricidad: $r_p = a(1-e)$ y $r_a = a(1+e)$.

## Cómo plantear un problema

1. Dibuja la situación y marca $r$ desde el **centro** del astro. Pasa todo al SI: los kilómetros a metros.
2. ¿Órbita circular? Iguala fuerza gravitatoria y centrípeta.
3. ¿Se compara un punto con otro (lanzamientos, cambios de órbita, escape, perihelio y afelio)? Conservación de la energía mecánica.
4. ¿Órbita elíptica? Añade la conservación del momento angular.
5. ¿Campo o potencial de varias masas? Vectores para el campo, suma directa para el potencial.
