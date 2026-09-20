# Qué cambia de la forma al cambiar de modelo

**Sí: este piloto aporta algo útil al artículo.** Permite pasar de «los mapas cambian» a mostrar **qué descripciones cambian**: cuánto se abre una nube y cómo reparte su variación entre direcciones. También muestra por qué sería precipitado resumir la «fragmentación» en una sola cifra.

Piloto terminado el 18-09-2026: diez modelos, los mismos **52.000 artículos** en el análisis principal, 2.000 por área y 400 por período. Se reutilizaron los vectores guardados. Hay 16.884 conjuntos de medidas con controles; no son 16.884 experimentos independientes ni artículos nuevos.

## El resultado que merece entrar en el paper

Cambiar de modelo **puede invertir una afirmación sobre dos disciplinas**, incluso cuando repetir la selección de artículos no la cambia.

Ejemplo ilustrativo, elegido después de ver los resultados. Cuanto mayor es el ángulo, más abierta queda la nube:

| Modelo y receta principal | Artes y Humanidades | Medicina | Qué parece más abierto |
| --- | ---: | ---: | --- |
| SPECTER | 48,0° | 59,2° | Medicina |
| BERT, media de posiciones | 37,3° | 30,9° | Artes y Humanidades |

**Las dos conclusiones opuestas se repiten en las 20 medias muestras y las cinco selecciones adicionales de igual tamaño.** También mantienen su signo al mirar pares cercanos, pares alejados o distancia al centro. Eso descarta, en estas comprobaciones, que la inversión sea solo una selección afortunada o la elección de la mediana. No demuestra qué modelo representa mejor las disciplinas.

Tablas: [inversión ilustrativa](reports/morphology_pilot_v1/illustrative_reversal.csv), [todas las áreas](reports/morphology_pilot_v1/field_summary.csv). [Mapa de posiciones por modelo](reports/morphology_pilot_v1/02_field_rank_maps.png).

## Qué medidas resultan aprovechables

| Rasgo | Qué comprobamos | Resultado y uso recomendado |
| --- | --- | --- |
| **Apertura** | Separación angular de los artículos; centro y distintos tramos de distancias como alternativas. | Muy repetible al cambiar artículos. El orden de las áreas depende bastante del modelo y de cómo se obtiene/procesa el vector. Incluir esa dependencia como resultado, sin llamar «diversidad temática» a la apertura. |
| **Reparto entre direcciones** | Si la variación se concentra en pocas direcciones o se reparte entre muchas. PR principal; entropía y D80 como alternativas. | Bastante repetible. Cuatro de 260 casos conservan alertas en las medias muestras. Las medidas alternativas concuerdan de forma amplia, pero no dan puestos idénticos. Incluir como descripción geométrica, no como número de temas. |
| **Conexión / posible separación** | Varias reglas para unir puntos; conexiones débiles, distancias de unión y puntos aislados. | Útil para diagnosticar, **todavía no como una medida general de fragmentación**. Una nube alargada o unos pocos extremos pueden producir señales parecidas a grupos separados. Mantener las comprobaciones y el resultado negativo en material adicional. |

La estabilidad de una cifra no garantiza que su interpretación sea correcta. Las nubes simuladas lo muestran con claridad: [contraejemplos](reports/morphology_pilot_v1/04_fragmentation_counterexamples.png). Definiciones y justificación previa: [protocolo](MORPHOLOGY_PROTOCOL.md).

## Cambiar artículos y cambiar modelo producen cosas distintas

Esta tabla compara **el orden de las 26 áreas**, no porcentajes de ciencia correcta. Uno significa el mismo orden; cero, poca relación entre ordenaciones. Son medianas descriptivas; los pares de modelos comparten modelos y no son independientes.

| Propiedad | Cambiar solo los artículos, manteniendo 2.000 por área | Cambiar de modelo sobre los mismos artículos |
| --- | ---: | ---: |
| Apertura | 0,992 | 0,319 |
| Direcciones efectivas, PR | 0,989 | 0,552 |
| Conexión con 25 vecinos | 0,950 | 0,714 |

Las cifras absolutas también cambian. La apertura media entre áreas va de **10,0° con PubMedBERT a 83,0° con MiniLM**; las direcciones efectivas medias, de **24,9 con BERT a 69,9 con MiniLM**. Parte de ello es la geometría general del encoder, no una propiedad de la disciplina. Por eso miramos también posiciones relativas y una referencia global de cada modelo. [Resumen de modelos](reports/morphology_pilot_v1/model_summary.csv) y [figura](reports/morphology_pilot_v1/01_model_properties.png).

## Qué controles cambian la lectura

- **Más artículos:** al pasar de 2.000 a 4.000, el cambio mediano de apertura es −0,03% y el de PR, +1,14%. El mayor cambio absoluto de PR es 4,07%. Esto apoya el tamaño del piloto para estas comparaciones; no certifica el tamaño correcto para toda pregunta o población.
- **Selección:** pasan la criba de amplitud y desplazamiento 260/260 aperturas y 256/260 PR en veinte medias muestras. En cinco muestras nuevas de 2.000 pasan ambos rasgos en 260/260. Cinco repeticiones no borran las cuatro alertas anteriores: PubMedBERT en Economía/Psicología y BioBERT en Economía/Inmunología.
- **Mismo fragmento para todos:** conserva bastante el orden dentro de cada modelo, pero **no hace desaparecer el desacuerdo entre modelos**. El acuerdo mediano entre modelos pasa de 0,319 a 0,285 en apertura y de 0,549 a 0,480 en PR en este control emparejado independiente.
- **Forma de obtener el vector:** importa mucho en los cuatro BERT. Cambiar media por CLS o SEP puede reordenar las áreas. Esto forma parte del resultado; no escogemos después la receta que mejor coincida.
- **Dirección común del encoder:** quitarla cambia especialmente la apertura. El acuerdo entre modelos sobre el orden de áreas sube de 0,333 a 0,694 en la muestra emparejada de 1.000. Por tanto, la apertura no es una descripción independiente del procesamiento. PR cambia bastante menos de orden con este control.
- **Texto, marcas de calidad y extremos:** quitar solo el título modifica poco el orden; quedarse solo con el título modifica más. Reponer artículos con marcas de calidad y retirar extremos frente a retirar puntos aleatorios altera poco los patrones generales. Esto **no valida las etiquetas temáticas de OpenAlex**.
- **MiniLM 512:** no cambia la lectura general del piloto. El acuerdo del orden de áreas respecto a MiniLM 256 es 0,973 en apertura y 0,987 en PR; se conserva 256 como principal.

[Todos los controles](reports/morphology_pilot_v1/paired_controls.csv), [estabilidad](reports/morphology_pilot_v1/selection_stability.csv), [figura de controles](reports/morphology_pilot_v1/05_control_rank_agreement.png).

## Lo que podemos decir de áreas concretas

Con las recetas principales, **Odontología** está entre las dos nubes menos abiertas en los diez modelos. Con texto común ocupa el puesto más bajo en todos. **Energía** está entre las tres áreas con PR más bajo en todos los modelos: su variación queda concentrada en relativamente pocas direcciones.

Pero los límites son reales: con otras recetas de los BERT, Odontología puede subir hasta el puesto 8 por apertura y Energía hasta el 10 por PR. Incluso con las recetas principales, D80 coloca a Energía hasta el puesto 7,5, mientras PR la sitúa entre 1 y 3. **No debemos vender un puesto exacto o una jerarquía universal de disciplinas.** [Comprobaciones de los ejemplos](reports/morphology_pilot_v1/illustrative_case_checks.csv).

## Por qué no cerraría todavía «fragmentación»

Los grafos unión quedan conectados en **260/260 casos** tanto con 10 como con 25 o 50 vecinos. Contar componentes se satura. Al exigir vecinos mutuos aparecen puntos aislados y el componente principal contiene entre 91,35% y 100%: otra regla, otra descripción.

La fuerza de conexión es menor que en las 780 referencias gaussianas construidas a partir de cada nube. Hay estructura que una referencia simple no reproduce, pero eso no identifica por sí solo grupos temáticos. Esas referencias conservan media/covarianza solo en expectativa antes de normalizar; el desajuste de PR llega al +19,8% en un caso. No son una prueba estadística ni un control perfecto.

La sensibilidad al tamaño tiene además una explicación concreta. Al duplicar de 2.000 a 4.000 y mantener 25 vecinos, la fuerza de conexión baja una mediana de 22,2%. Si también duplicamos los vecinos a 50, el cambio es +3,3%. Se registró esta comprobación adicional durante la ejecución. Las comparaciones principales ya usan tamaños iguales; **no confundir cambiar la regla de conexión con descubrir un cambio de la ciencia**. Hay 51/260 alertas de conexión en las cinco selecciones adicionales de igual tamaño. [Detalle](reports/morphology_pilot_v1/connectivity_fixed_fraction.csv).

## Tiempo y encaje en el artículo

Entre 2000–04 y 2020–24 baja la apertura en 203/260 combinaciones modelo–área y PR en 207/260. La dirección se mantiene en al menos nueve de diez selecciones reducidas en 183 y 144 de esos descensos, respectivamente. Son resultados exploratorios del corpus: no prueban que la ciencia se esté estrechando. Cambian textos, composición de temas y cobertura; faltaría aislar esos factores para una afirmación histórica nueva.

**Recomendación:** incorporar una ampliación acotada sobre la fiabilidad de las descripciones geométricas. Una figura de posiciones de las áreas, el ejemplo de inversión y los controles principales aportan una consecuencia comprensible de cambiar de encoder. Dejar las cifras completas, tiempo y diagnósticos de conexión como material adicional. No convertir este piloto en otro paper de clasificación de temas ni sustituir las comparaciones anteriores de forma/vecinos.

La literatura ya estudia geometría de embeddings y densidad científica; las medidas no son nuevas. El interés está en mostrar, con los mismos artículos y alternativas explícitas, qué afirmaciones resisten y cuáles dependen de decisiones de construcción. [Antecedentes y límites](research/morphology_2026-09-18/LITERATURE.md). Esto hace más concreto el trabajo; no garantiza aceptación en QSS.

Registro técnico y reproducción: [METHODS_MORPHOLOGY.md](METHODS_MORPHOLOGY.md). Corpus, vectores y cierres anteriores conservados. No se ha empezado el manuscrito ni publicado esta ampliación.
