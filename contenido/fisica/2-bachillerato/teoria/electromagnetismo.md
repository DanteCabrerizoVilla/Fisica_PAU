---
bloque: electromagnetismo
resumen: "Campo y potencial eléctrico, fuerza de Lorentz, campo magnético creado por corrientes e inducción electromagnética."
formulas:
  - grupo: "Campo eléctrico"
    lista:
      - nombre: "Ley de Coulomb"
        tex: 'F = K\,\dfrac{|q_1\,q_2|}{r^2}'
        nota: 'Repulsiva si las cargas tienen el mismo signo, atractiva si no. $K = 9\cdot 10^{9}\ \mathrm{N\,m^2\,C^{-2}}$.'
      - nombre: "Campo de una carga puntual"
        tex: 'E = K\,\dfrac{|q|}{r^2}'
        nota: 'Sale de las cargas positivas y entra en las negativas. Con varias cargas se suman los vectores.'
      - nombre: "Fuerza sobre una carga"
        tex: '\vec F = q\,\vec E'
        nota: 'Si $q$ es negativa, la fuerza va en sentido contrario al campo.'
      - nombre: "Teorema de Gauss"
        tex: '\Phi_E = \oint \vec E\cdot \mathrm{d}\vec S = \dfrac{Q_\text{int}}{\varepsilon_0}'
        nota: 'El flujo a través de una superficie cerrada solo depende de la carga que encierra.'
  - grupo: "Potencial y energía"
    lista:
      - nombre: "Potencial de una carga puntual"
        tex: 'V = K\,\dfrac{q}{r}'
        nota: 'Con el signo de la carga. Es un escalar: se suma sin vectores.'
      - nombre: "Energía potencial"
        tex: 'E_p = q\,V = K\,\dfrac{q_1\,q_2}{r}'
      - nombre: "Trabajo del campo"
        tex: 'W_{A\to B} = q\,(V_A - V_B) = -\Delta E_p'
      - nombre: "Campo uniforme"
        tex: '|\Delta V| = E\,d'
        nota: '$d$ es la distancia medida a lo largo del campo. El potencial disminuye en el sentido del campo.'
  - grupo: "Fuerza magnética"
    lista:
      - nombre: "Fuerza de Lorentz"
        tex: '\vec F = q\,\vec v\times\vec B \qquad F = |q|\,v\,B\,\operatorname{sen}\theta'
        nota: 'Perpendicular a $\vec v$ y a $\vec B$. No cambia el módulo de la velocidad.'
      - nombre: "Radio de la trayectoria circular"
        tex: 'R = \dfrac{m\,v}{|q|\,B}'
        nota: 'Cuando $\vec v$ es perpendicular a $\vec B$.'
      - nombre: "Periodo de giro"
        tex: 'T = \dfrac{2\pi\,m}{|q|\,B}'
        nota: 'No depende de la velocidad.'
      - nombre: "Selector de velocidades"
        tex: 'v = \dfrac{E}{B}'
        nota: 'Campos eléctrico y magnético perpendiculares: solo pasan sin desviarse las partículas con esa velocidad.'
      - nombre: "Fuerza sobre un conductor"
        tex: '\vec F = I\,\vec L\times\vec B \qquad F = I\,L\,B\,\operatorname{sen}\theta'
  - grupo: "Campo magnético de corrientes"
    lista:
      - nombre: "Hilo recto muy largo"
        tex: 'B = \dfrac{\mu_0\,I}{2\pi\,d}'
        nota: 'Líneas circulares alrededor del hilo; sentido con la regla de la mano derecha. $\mu_0 = 4\pi\cdot 10^{-7}\ \mathrm{T\,m\,A^{-1}}$.'
      - nombre: "Centro de una espira circular"
        tex: 'B = \dfrac{\mu_0\,I}{2R}'
      - nombre: "Interior de un solenoide"
        tex: 'B = \mu_0\,\dfrac{N}{L}\,I'
      - nombre: "Fuerza entre hilos paralelos"
        tex: '\dfrac{F}{L} = \dfrac{\mu_0\,I_1\,I_2}{2\pi\,d}'
        nota: 'Se atraen si las corrientes van en el mismo sentido y se repelen si van en sentidos contrarios.'
  - grupo: "Inducción electromagnética"
    lista:
      - nombre: "Flujo magnético"
        tex: '\Phi = B\,S\cos\theta'
        nota: '$\theta$ es el ángulo entre $\vec B$ y la **normal** a la superficie. Se mide en weber (Wb).'
      - nombre: "Ley de Faraday-Lenz"
        tex: '\varepsilon = -N\,\dfrac{\mathrm{d}\Phi}{\mathrm{d}t}'
        nota: 'El signo menos es la ley de Lenz: la corriente inducida se opone al cambio de flujo.'
      - nombre: "Intensidad inducida"
        tex: 'I = \dfrac{\varepsilon}{R}'
      - nombre: "Varilla que se mueve en un campo"
        tex: '|\varepsilon| = B\,L\,v'
        nota: 'Con $\vec B$, la varilla y la velocidad perpendiculares entre sí.'
      - nombre: "Espira que gira (alternador)"
        tex: '\varepsilon(t) = N\,B\,S\,\omega\,\operatorname{sen}(\omega t)'
        nota: 'Valor máximo: $\varepsilon_0 = N B S \omega$.'
---

Este bloque tiene dos mitades. En la primera, el **campo eléctrico** se trabaja igual que el gravitatorio, con la diferencia de que hay cargas de dos signos. En la segunda aparecen el **campo magnético**, que actúa solo sobre cargas en movimiento, y la **inducción**, que relaciona los dos campos.

## Campo eléctrico

Dos cargas puntuales se ejercen una fuerza dada por la ley de Coulomb, $F = K|q_1 q_2|/r^2$. A diferencia de la gravedad, puede ser atractiva o repulsiva.

El campo eléctrico en un punto es la fuerza por unidad de carga positiva. Para una carga puntual vale $E = K|q|/r^2$ y su sentido es:

- **hacia fuera** si la carga que lo crea es positiva,
- **hacia la carga** si es negativa.

Con varias cargas se aplica el principio de superposición: se calcula el módulo del campo de cada una, se dibuja su vector, se descompone en $x$ e $y$ y se suman las componentes. El error más habitual está en el dibujo, no en las cuentas, así que merece la pena hacerlo grande y con cuidado.

Una carga $q$ colocada en un campo sufre una fuerza $\vec F = q\vec E$. Si la carga es negativa, se mueve en contra del campo. En un **campo uniforme** (entre dos placas, por ejemplo) la fuerza es constante y la carga lleva un movimiento uniformemente acelerado con $a = qE/m$, igual que un tiro parabólico.

El **teorema de Gauss** dice que el flujo del campo eléctrico a través de una superficie cerrada es $Q_\text{int}/\varepsilon_0$. Se usa para obtener el campo cuando hay mucha simetría: fuera de una esfera cargada el campo es el de una carga puntual en su centro, y dentro de un conductor en equilibrio el campo es nulo.

## Potencial eléctrico y trabajo

El potencial de una carga puntual es $V = Kq/r$, **con el signo de la carga**. Como es un escalar, el potencial de varias cargas es la suma de los potenciales, sin vectores. Por eso suele ser más rápido que el campo.

Una carga $q$ en un punto de potencial $V$ tiene una energía potencial $E_p = qV$. El trabajo que hace el campo al llevarla de A a B es:

$$W_{A\to B} = q\,(V_A - V_B)$$

- Si $W > 0$, la carga se mueve espontáneamente y pierde energía potencial.
- Si $W < 0$, hay que empujarla con una fuerza externa.

Para calcular velocidades se usa la conservación de la energía: $\tfrac12 m v^2 + qV$ vale lo mismo en los dos puntos. Una partícula de carga $q$ acelerada desde el reposo por una diferencia de potencial $\Delta V$ gana una energía cinética $|q|\,\Delta V$.

Un detalle que se pregunta mucho: que el campo sea cero en un punto **no implica** que el potencial sea cero, ni al revés. En el punto medio entre dos cargas iguales el campo se anula y el potencial no; entre dos cargas del mismo valor y signo contrario ocurre lo opuesto.

## Fuerza de Lorentz

Un campo magnético solo actúa sobre cargas en movimiento:

$$\vec F = q\,\vec v\times\vec B$$

El módulo es $|q|\,v\,B\,\operatorname{sen}\theta$ y la dirección es perpendicular a la velocidad y al campo. El sentido lo da la regla de la mano derecha para una carga positiva; si la carga es negativa, el contrario.

Como la fuerza es siempre perpendicular a la velocidad, **no hace trabajo**: cambia la dirección del movimiento pero no su rapidez. Hay tres casos:

- $\vec v$ paralela a $\vec B$: no hay fuerza y la carga sigue recta.
- $\vec v$ perpendicular a $\vec B$: movimiento circular uniforme. Igualando la fuerza magnética con la centrípeta, $R = mv/(|q|B)$ y $T = 2\pi m/(|q|B)$.
- Caso intermedio: trayectoria helicoidal.

Si además hay un campo eléctrico, la fuerza total es $\vec F = q(\vec E + \vec v\times\vec B)$. Cuando las dos fuerzas se compensan, la carga no se desvía: es el selector de velocidades, $v = E/B$.

Sobre un conductor de longitud $L$ recorrido por una corriente $I$, la fuerza es $F = ILB\operatorname{sen}\theta$.

## Campo magnético creado por corrientes

Las corrientes eléctricas crean campo magnético. Para un hilo recto muy largo:

$$B = \frac{\mu_0\,I}{2\pi\,d}$$

Las líneas de campo son circunferencias alrededor del hilo. El sentido se obtiene con la mano derecha: el pulgar en el sentido de la corriente y los dedos indican el giro del campo. En los problemas se dibuja el hilo perpendicular al papel, con un punto (corriente que sale) o un aspa (corriente que entra).

Con dos o más hilos, el campo total es la suma vectorial. Dos hilos paralelos se ejercen fuerzas entre sí: se **atraen** si las corrientes tienen el mismo sentido y se **repelen** si son opuestas, justo al revés de lo que la intuición de las cargas sugiere.

## Inducción electromagnética

El **flujo magnético** mide cuántas líneas de campo atraviesan una superficie: $\Phi = BS\cos\theta$, donde $\theta$ es el ángulo entre el campo y la normal a la superficie.

La ley de Faraday dice que aparece una fuerza electromotriz siempre que el flujo **cambia**:

$$\varepsilon = -N\,\frac{\mathrm{d}\Phi}{\mathrm{d}t}$$

El flujo puede cambiar por tres motivos, y cada uno da un tipo de problema:

- cambia el **campo** $B(t)$ con la espira quieta;
- cambia la **superficie** dentro del campo (una espira que entra o sale, una varilla que desliza);
- cambia el **ángulo** (una espira que gira: el alternador).

La **ley de Lenz** da el sentido: la corriente inducida crea un campo que se opone al cambio. Si el flujo aumenta, el campo inducido va en contra del original; si disminuye, lo refuerza.

Mientras el flujo no cambie no hay fem, por grande que sea el campo. Una espira completamente dentro de un campo uniforme y constante no tiene corriente inducida aunque se desplace, siempre que no gire.

## Cómo plantear un problema

1. Haz el dibujo con los ejes y los signos de las cargas. Pasa a SI: los nC, µC, cm y mT son la principal fuente de errores.
2. Campo de varias cargas o hilos: módulo de cada uno, vector, componentes y suma.
3. Potencial o trabajo: suma escalar y $W = q(V_A - V_B)$.
4. Carga en un campo magnético: fuerza de Lorentz igual a fuerza centrípeta.
5. Inducción: escribe $\Phi(t)$, deriva y aplica Lenz para el sentido.
