---
bloque: optica
resumen: "Reflexión, refracción y ángulo límite; formación de imágenes en lentes delgadas y espejos con el criterio de signos del examen; el ojo."
formulas:
  - grupo: "Reflexión y refracción"
    lista:
      - nombre: "Índice de refracción"
        tex: 'n = \dfrac{c}{v}'
        nota: 'Siempre mayor o igual que 1. Al cambiar de medio la frecuencia no cambia; la longitud de onda sí: $\lambda = \lambda_0/n$.'
      - nombre: "Ley de la reflexión"
        tex: '\theta_i = \theta_r'
      - nombre: "Ley de Snell"
        tex: 'n_1\operatorname{sen}\theta_1 = n_2\operatorname{sen}\theta_2'
        nota: 'Los ángulos se miden respecto a la **normal** a la superficie.'
      - nombre: "Ángulo límite"
        tex: '\operatorname{sen}\theta_L = \dfrac{n_2}{n_1}'
        nota: 'Solo al pasar a un medio de menor índice ($n_1 > n_2$). Por encima hay reflexión total.'
      - nombre: "Lámina de caras paralelas"
        tex: 'd = e\,\dfrac{\operatorname{sen}(\theta_1 - \theta_2)}{\cos\theta_2}'
        nota: 'Desplazamiento lateral del rayo; $e$ es el espesor. El rayo sale paralelo al que entra.'
  - grupo: "Lentes delgadas"
    lista:
      - nombre: "Ecuación de la lente"
        tex: '\dfrac{1}{s^{\prime}} - \dfrac{1}{s} = \dfrac{1}{f^{\prime}}'
        nota: 'Objeto a la izquierda: $s$ negativa. Convergente: $f^{\prime} > 0$. Divergente: $f^{\prime} < 0$.'
      - nombre: "Aumento lateral"
        tex: 'M = \dfrac{y^{\prime}}{y} = \dfrac{s^{\prime}}{s}'
        nota: 'Negativo: imagen invertida. Valor absoluto mayor que 1: imagen mayor que el objeto.'
      - nombre: "Potencia"
        tex: 'P = \dfrac{1}{f^{\prime}}'
        nota: 'En dioptrías si $f^{\prime}$ está en metros.'
      - nombre: "Ecuación del fabricante de lentes"
        tex: '\dfrac{1}{f^{\prime}} = (n - 1)\left(\dfrac{1}{R_1} - \dfrac{1}{R_2}\right)'
        nota: 'Lente de índice $n$ en el aire; los radios, con su signo.'
  - grupo: "Espejos"
    lista:
      - nombre: "Ecuación del espejo"
        tex: '\dfrac{1}{s^{\prime}} + \dfrac{1}{s} = \dfrac{1}{f}'
        nota: 'Cóncavo: $f < 0$. Convexo: $f > 0$.'
      - nombre: "Distancia focal"
        tex: 'f = \dfrac{R}{2}'
      - nombre: "Aumento lateral"
        tex: 'M = \dfrac{y^{\prime}}{y} = -\dfrac{s^{\prime}}{s}'
      - nombre: "Espejo plano"
        tex: 's^{\prime} = -s'
        nota: 'Imagen virtual, derecha y del mismo tamaño.'
---

La óptica geométrica trata la luz como rayos que viajan en línea recta y cambian de dirección al reflejarse o al cambiar de medio. En el examen oficial estas preguntas pertenecen al bloque «Vibraciones y ondas», y casi siempre piden dos cosas: **cálculo** con las ecuaciones y **trazado de rayos**.

## Reflexión y refracción

La luz viaja más despacio en un medio material que en el vacío. El **índice de refracción** mide cuánto: $n = c/v$. Al pasar de un medio a otro la frecuencia no cambia (el color es el mismo), pero la velocidad y la longitud de onda sí.

Cuando un rayo llega a la superficie que separa dos medios, parte se refleja y parte se refracta. Todos los ángulos se miden respecto a la **normal**, la recta perpendicular a la superficie:

- **Reflexión**: el ángulo de reflexión es igual al de incidencia.
- **Refracción** (ley de Snell): $n_1\operatorname{sen}\theta_1 = n_2\operatorname{sen}\theta_2$.

Para recordar hacia dónde se desvía el rayo: al entrar en un medio de **mayor** índice se **acerca** a la normal, y al pasar a uno de menor índice se aleja.

En ese segundo caso hay un ángulo de incidencia para el que el rayo refractado sale rasante, a 90°. Es el **ángulo límite**:

$$\operatorname{sen}\theta_L = \frac{n_2}{n_1}$$

Para ángulos mayores no hay rayo refractado y toda la luz se refleja: **reflexión total**. Es el principio de la fibra óptica. Solo puede ocurrir al pasar de un medio a otro de índice menor, por ejemplo del vidrio al aire, nunca al revés.

En una **lámina de caras paralelas** el rayo se refracta dos veces y sale paralelo al rayo incidente, pero desplazado. En un **prisma**, las dos refracciones lo desvían en el mismo sentido; como el índice depende ligeramente del color, la luz blanca se dispersa.

## Criterio de signos

En el examen de Madrid se usa la norma DIN, y todas las fórmulas de esta página están escritas con ella:

- La luz viaja de izquierda a derecha.
- Las distancias se miden desde el centro de la lente (o el vértice del espejo): **positivas hacia la derecha** y negativas hacia la izquierda.
- Las alturas son positivas hacia arriba.

Con este criterio, un objeto real colocado delante de la lente tiene siempre $s < 0$. Olvidar ese signo es el fallo más frecuente del bloque.

## Lentes delgadas

La posición de la imagen y su tamaño salen de dos ecuaciones:

$$\frac{1}{s'} - \frac{1}{s} = \frac{1}{f'} \qquad\qquad M = \frac{y'}{y} = \frac{s'}{s}$$

Una lente **convergente** tiene $f' > 0$ y una **divergente**, $f' < 0$. El resultado se interpreta así:

- $s' > 0$: la imagen se forma al otro lado de la lente, donde realmente se cruzan los rayos. Es **real** y se puede recoger en una pantalla.
- $s' < 0$: la imagen está en el mismo lado que el objeto. Es **virtual**: se ve mirando a través de la lente.
- $M < 0$: imagen invertida. $|M| > 1$: mayor que el objeto.

Para el **trazado de rayos** bastan dos de estos tres rayos que salen del extremo del objeto:

1. El que llega paralelo al eje sale pasando por el foco imagen $F'$.
2. El que pasa por el centro de la lente no se desvía.
3. El que pasa por el foco objeto $F$ sale paralelo al eje.

En una lente convergente, lo que ocurre depende de dónde esté el objeto:

| Posición del objeto | Imagen |
|---|---|
| Más lejos que $2f'$ | Real, invertida y menor |
| Entre $2f'$ y $f'$ | Real, invertida y mayor |
| Entre el foco y la lente | Virtual, derecha y mayor (lupa) |

Una lente divergente da siempre una imagen virtual, derecha y menor.

Con **dos lentes**, se resuelve por pasos: la imagen de la primera hace de objeto para la segunda, midiendo la nueva $s$ desde la segunda lente. El aumento total es el producto de los aumentos.

## Espejos

Las ecuaciones se parecen a las de las lentes, con dos cambios de signo:

$$\frac{1}{s'} + \frac{1}{s} = \frac{1}{f} \qquad\qquad M = \frac{y'}{y} = -\frac{s'}{s}$$

La distancia focal es la mitad del radio, $f = R/2$. Un espejo **cóncavo** tiene el centro de curvatura delante, a la izquierda, y por tanto $R$ y $f$ negativos; uno **convexo**, positivos.

En los espejos la luz vuelve hacia la izquierda, así que la interpretación de $s'$ es la contraria que en las lentes: la imagen es **real si $s' < 0$** (delante del espejo) y virtual si $s' > 0$ (detrás).

Un espejo convexo da siempre una imagen virtual, derecha y menor, y por eso se usa en retrovisores y cruces. El espejo plano da una imagen virtual, del mismo tamaño y a la misma distancia por detrás.

## El ojo e instrumentos ópticos

El ojo funciona como una lente convergente (el cristalino) que forma una imagen real e invertida sobre la retina. Para enfocar a distintas distancias cambia su curvatura.

- **Miopía**: la imagen de los objetos lejanos se forma delante de la retina. Se corrige con lentes **divergentes**.
- **Hipermetropía**: la imagen de los objetos cercanos se formaría detrás de la retina. Se corrige con lentes **convergentes**.
- **Presbicia** (vista cansada): el cristalino pierde capacidad de acomodación con la edad. Lentes convergentes para ver de cerca.

La **lupa** es una lente convergente con el objeto colocado entre el foco y la lente. El microscopio y el telescopio combinan dos lentes y se analizan como un sistema de dos lentes.

## Cómo plantear un problema

1. Haz un esquema con el eje, la lente o el espejo, los focos y el objeto.
2. Escribe los datos **con su signo** antes de sustituir.
3. Resuelve la ecuación para la incógnita y calcula el aumento.
4. Interpreta: real o virtual, derecha o invertida, mayor o menor.
5. Haz el trazado de rayos y comprueba que coincide con las cuentas.
