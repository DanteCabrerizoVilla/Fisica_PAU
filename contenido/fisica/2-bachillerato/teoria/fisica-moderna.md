---
bloque: fisica-moderna
resumen: "Relatividad especial, efecto fotoeléctrico, dualidad onda-corpúsculo, núcleo atómico y radiactividad."
formulas:
  - grupo: "Relatividad especial"
    lista:
      - nombre: "Factor de Lorentz"
        tex: '\gamma = \dfrac{1}{\sqrt{1 - \dfrac{v^2}{c^2}}}'
        nota: 'Siempre mayor o igual que 1. Solo se aleja de 1 a velocidades cercanas a la de la luz.'
      - nombre: "Dilatación del tiempo"
        tex: '\Delta t = \gamma\,\Delta t_0'
        nota: '$\Delta t_0$ es el tiempo propio: el que mide quien ve los dos sucesos en el mismo lugar.'
      - nombre: "Contracción de la longitud"
        tex: 'L = \dfrac{L_0}{\gamma}'
        nota: '$L_0$ es la longitud en reposo. Solo se contrae en la dirección del movimiento.'
      - nombre: "Masa relativista"
        tex: 'm = \gamma\,m_0'
      - nombre: "Energía total y en reposo"
        tex: 'E = m\,c^2 = \gamma\,m_0\,c^2 \qquad E_0 = m_0\,c^2'
      - nombre: "Energía cinética"
        tex: 'E_c = E - E_0 = (\gamma - 1)\,m_0\,c^2'
        nota: 'A velocidades altas no vale $\tfrac12 m v^2$.'
  - grupo: "Física cuántica"
    lista:
      - nombre: "Energía de un fotón"
        tex: 'E = h\,f = \dfrac{h\,c}{\lambda}'
      - nombre: "Efecto fotoeléctrico"
        tex: 'h\,f = W_0 + E_{c,\text{máx}}'
        nota: '$W_0$ es el trabajo de extracción del metal.'
      - nombre: "Frecuencia umbral"
        tex: 'W_0 = h\,f_0 = \dfrac{h\,c}{\lambda_0}'
        nota: 'Por debajo de $f_0$ (o por encima de $\lambda_0$) no se emiten electrones.'
      - nombre: "Potencial de frenado"
        tex: 'E_{c,\text{máx}} = e\,V_f'
      - nombre: "Longitud de onda de De Broglie"
        tex: '\lambda = \dfrac{h}{p} = \dfrac{h}{m\,v}'
      - nombre: "Partícula acelerada por un potencial"
        tex: '\lambda = \dfrac{h}{\sqrt{2\,m\,|q|\,\Delta V}}'
        nota: 'Partiendo del reposo y sin efectos relativistas.'
      - nombre: "Principio de incertidumbre"
        tex: '\Delta x\,\Delta p \ge \dfrac{h}{4\pi}'
  - grupo: "Núcleo y radiactividad"
    lista:
      - nombre: "Defecto de masa"
        tex: '\Delta m = Z\,m_p + (A - Z)\,m_n - M_\text{núcleo}'
      - nombre: "Energía de enlace"
        tex: 'E = \Delta m\,c^2'
        nota: 'Dividida entre $A$ da la energía de enlace por nucleón, que mide la estabilidad.'
      - nombre: "Ley de desintegración"
        tex: 'N = N_0\,e^{-\lambda t}'
        nota: 'La misma forma vale para la masa y para la actividad.'
      - nombre: "Periodo de semidesintegración"
        tex: 'T_{1/2} = \dfrac{\ln 2}{\lambda}'
      - nombre: "Vida media"
        tex: '\tau = \dfrac{1}{\lambda}'
      - nombre: "Actividad"
        tex: 'A = \lambda\,N = A_0\,e^{-\lambda t}'
        nota: 'En becquerel (desintegraciones por segundo) si $\lambda$ está en $\mathrm{s^{-1}}$.'
      - nombre: "Número de núcleos de una muestra"
        tex: 'N = \dfrac{m}{M}\,N_A'
        nota: '$m$ es la masa de la muestra y $M$ la masa molar, en las mismas unidades.'
      - nombre: "Energía de una reacción nuclear"
        tex: 'Q = \left(\sum m_\text{reactivos} - \sum m_\text{productos}\right) c^2'
---

A principios del siglo XX la física clásica dejó de funcionar en tres terrenos: a velocidades cercanas a la de la luz (**relatividad**), a escala atómica (**cuántica**) y en el interior del núcleo (**nuclear**). Este bloque recorre los tres. Los problemas son cortos y directos, pero las unidades (eV, MeV, u, nm) exigen atención.

## Relatividad especial

Einstein partió de dos postulados:

1. Las leyes de la física son las mismas en todos los sistemas de referencia inerciales.
2. La velocidad de la luz en el vacío es la misma para todos los observadores, se muevan como se muevan.

De ahí se deduce que el tiempo y el espacio no son absolutos. Todo queda controlado por el factor $\gamma = 1/\sqrt{1 - v^2/c^2}$, que vale 1 a velocidades cotidianas y crece sin límite al acercarse a $c$.

- **Dilatación del tiempo**: un reloj en movimiento marcha más despacio. El tiempo propio $\Delta t_0$ (medido en el sistema donde los dos sucesos ocurren en el mismo sitio) es el más corto: $\Delta t = \gamma\,\Delta t_0$.
- **Contracción de la longitud**: un objeto en movimiento se mide más corto en la dirección en la que se mueve: $L = L_0/\gamma$.

La energía total de una partícula es $E = \gamma m_0 c^2$. Incluso en reposo tiene una energía $E_0 = m_0c^2$, y la energía cinética es la diferencia:

$$E_c = (\gamma - 1)\,m_0\,c^2$$

Ningún cuerpo con masa puede alcanzar la velocidad de la luz: haría falta una energía infinita.

[[sim:relatividad|Energía cinética clásica y relativista frente a la velocidad: mira a partir de dónde se separan.]]

## Efecto fotoeléctrico

Al iluminar un metal con luz de frecuencia suficientemente alta, se arrancan electrones. La física clásica no podía explicar lo que se observa:

- Existe una **frecuencia umbral**. Por debajo no sale ningún electrón, por muy intensa que sea la luz.
- La energía de los electrones depende de la **frecuencia** de la luz, no de su intensidad.
- Aumentar la **intensidad** hace que salgan más electrones, pero no más rápidos.

Einstein lo explicó suponiendo que la luz está formada por **fotones**, cada uno con energía $E = hf$. Cada fotón entrega toda su energía a un solo electrón:

$$h\,f = W_0 + E_{c,\text{máx}}$$

$W_0$ es el **trabajo de extracción**, la energía mínima para arrancar un electrón de ese metal, y define la frecuencia umbral: $W_0 = hf_0$. El resto se lo lleva el electrón como energía cinética.

El **potencial de frenado** es la diferencia de potencial que detiene a los electrones más rápidos: $E_{c,\text{máx}} = eV_f$. Por eso una energía cinética de 2 eV corresponde a un potencial de frenado de 2 V.

[[sim:fotoelectrico|Cambia la longitud de onda y la intensidad de la luz y comprueba las tres observaciones del principio.]]

Para las unidades: $1\ \mathrm{eV} = 1{,}6\cdot 10^{-19}\ \mathrm{J}$. Y si te dan la longitud de onda, $f = c/\lambda$.

## Dualidad onda-corpúsculo

Si la luz, que es una onda, se comporta también como partícula, De Broglie propuso lo simétrico: toda partícula tiene asociada una onda de longitud

$$\lambda = \frac{h}{p} = \frac{h}{m\,v}$$

Para objetos cotidianos esa longitud de onda es tan pequeña que no se puede observar. Para un electrón es del orden del tamaño de un átomo, y por eso los electrones se difractan.

El **principio de incertidumbre** de Heisenberg establece que no se pueden conocer a la vez con precisión arbitraria la posición y la cantidad de movimiento de una partícula: $\Delta x\,\Delta p \ge h/4\pi$. No es un defecto de los aparatos, sino una propiedad de la naturaleza.

## Núcleo atómico y energía de enlace

Un núcleo $^A_Z\mathrm{X}$ tiene $Z$ protones y $A - Z$ neutrones. Su masa es **menor** que la suma de las masas de sus partículas por separado. Esa diferencia es el **defecto de masa**, y equivale a la energía que se liberó al formarse el núcleo, la **energía de enlace**:

$$E = \Delta m\,c^2$$

La **energía de enlace por nucleón**, $E/A$, indica lo estable que es un núcleo. Es máxima para núcleos intermedios, cerca del hierro. Por eso se libera energía tanto al partir núcleos muy pesados (**fisión**) como al unir núcleos muy ligeros (**fusión**).

En cualquier reacción nuclear se conservan el número másico $A$ y la carga $Z$. La energía liberada sale de la diferencia de masas entre reactivos y productos. Para las unidades: $1\ \mathrm{u} = 1{,}66\cdot 10^{-27}\ \mathrm{kg}$, que equivale a unos 931,5 MeV.

## Radiactividad

Los núcleos inestables se desintegran emitiendo radiación:

| Tipo | Qué se emite | Efecto en el núcleo |
|---|---|---|
| Alfa ($\alpha$) | Un núcleo de helio, $^4_2\mathrm{He}$ | $A$ baja 4 y $Z$ baja 2 |
| Beta ($\beta^-$) | Un electrón | $A$ no cambia y $Z$ sube 1 |
| Gamma ($\gamma$) | Un fotón de alta energía | No cambian ni $A$ ni $Z$ |

La desintegración es un proceso al azar, pero con muchos núcleos sigue una ley exponencial:

$$N = N_0\,e^{-\lambda t}$$

$\lambda$ es la constante de desintegración. El **periodo de semidesintegración** $T_{1/2} = \ln 2/\lambda$ es el tiempo que tarda en reducirse a la mitad el número de núcleos; no hay que confundirlo con la **vida media**, $\tau = 1/\lambda$.

La **actividad** es el número de desintegraciones por segundo, $A = \lambda N$, y decae con la misma exponencial. Para pasar de la masa de una muestra al número de núcleos se usa el número de Avogadro.

Un atajo útil: tras $n$ periodos de semidesintegración queda una fracción $1/2^n$ de la muestra.

[[sim:desintegracion|Mira cómo la muestra se reduce a la mitad en cada periodo y practica el paso entre $T_{1/2}$, $\tau$ y $\lambda$.]]

## Partículas e interacciones

La materia está formada por dos familias de partículas elementales: los **quarks** (que forman protones y neutrones: un protón es *uud* y un neutrón *udd*) y los **leptones** (como el electrón y los neutrinos). Entre ellas actúan cuatro interacciones fundamentales: gravitatoria, electromagnética, nuclear fuerte (mantiene unido el núcleo) y nuclear débil (responsable de la desintegración beta).

## Cómo plantear un problema

1. Decide las unidades desde el principio: todo en SI, o energías en eV si el problema lo pone fácil.
2. Fotoeléctrico: energía del fotón, trabajo de extracción y balance de Einstein.
3. Radiactividad: calcula $\lambda$ con las mismas unidades de tiempo que vayas a usar en $t$.
4. Relatividad: calcula primero $\gamma$.
