# Protocolo del cierre experimental ampliado

17-09-2026. Alcance íntegro en `ROBUSTNESS_SCOPE.md`. Las decisiones de esta fase se toman después de conocer los resultados anteriores, y se describirán así. Lo siguiente se fija antes de inspeccionar los nuevos resultados correspondientes. No se alteran originales, modelos ni versiones anteriores.

## Entradas de 52.000 y recetas

Misma semilla y orden por huella del ID que en 26k. Se toman los primeros 400 en cada Field×período, manteniendo los 200 anteriores: 52.000, con 2.000 por Field. Se conserva literalmente título, abstract y formato habitual de ambos. La condición combinada se copia de los originales; las otras dos preservan exactamente todos los vectores del piloto y solo infieren los 26.000 añadidos. Se mantienen media principal de los cuatro BERT, CLS/SEP como controles, límites, pesos, adaptadores y tokenizadores. Configuración congelada: `config/input52_v1.json`.

Se repiten CKA corregida, rangos de distancias y kNN exactos k=10/25/50 sobre candidatos idénticos por área. El contraste modelo–entrada conserva su definición. Las alternativas de receta se cruzan con modelo, Field e input, sin convertirlas en modelos nuevos ni elegir una receta por mayor acuerdo. La documentación explicará posiciones especiales y que CLS no significa el pooler denso de BERT.

La comparación directa de alertas mantiene los 20 subconjuntos a la mitad del tamaño: 1.000 por Field, 200 por período; umbrales originales de cambio mediano ≤0,02 y amplitud central ≤0,04. Se seguirán las 31 claves originales aunque desaparezca su alerta. Para reducir el ruido de solo 20 repeticiones se añadirá, en una salida separada, una comprobación de 100 repeticiones en ambos tamaños, con la misma regla y semillas declaradas. No se presentará ese cambio de repeticiones como efecto de duplicar la muestra.

## Subfields, escalas y cobertura

La auditoría de tamaños previa encuentra 252 Subfields y 1.255 combinaciones no vacías con período. Sus tamaños van de 3 a 17.974 agrupando fechas. No se impondrá al corpus entero el tamaño del más pequeño y no se inventarán medidas para grupos que no pueden admitirlas.

- Comparación principal por Subfield agrupando fechas: mismos documentos y diez modelos, CKA, correlación de rangos y vecinos exactos. CKA requiere al menos cuatro filas; k=10/25/50 requiere más de k candidatos. Marcar por separado cada medida no calculable y los grupos pequeños; no convertirlos en cero o quitarlos de la cobertura.
- Control de tamaño entre Field y Subfield: 256 candidatos por grupo, con controles de 128 y 512 sobre el subconjunto común de grupos elegibles. El tamaño 256 cubre 217 de 252 Subfields y 495.828 artículos del corpus. Incluir todos los grupos en las tablas de cobertura, también los excluidos del control. Usar mismas selecciones para todos los modelos y las tres recetas.
- Repetir selecciones emparejadas para medir sensibilidad de cada Subfield. Separar diferencias entre modelos de variación por selección. Reportar tamaño, cambio mediano, amplitud y dirección, sin llamar a los rangos intervalos poblacionales.
- Comparar centros de Field, centros de Subfield y organización interna/local con medidas del mismo tipo cuando sea posible. Una puntuación sobre centros y otra sobre artículos son objetos distintos: no suponer que existe una ley de caída al aumentar detalle. El control de tamaño y referencias de grupos aleatorios deben acompañar la interpretación.

La composición por período será visible. En el análisis temporal de Subfields se conservarán grupos pequeños y cobertura de cada fecha; los controles comunes deben restringirse a grupos elegibles en todas las fechas comparadas. La unidad principal Field se conserva.

## Estabilidad por artículo y regiones

Cada artículo conserva su ID. Se resumirá su coincidencia entre los 45 pares de modelos, con sensibilidad k=10/25/50 y omisión de modelos/familias, separando búsqueda dentro de Field×período y de Subfield. La puntuación continua es principal. Los extremos por deciles sirven para localizar casos, no para inventar un umbral universal de artículo estable.

Mostrar distribución por Field, Subfield y período, tamaños de búsqueda y marcas de calidad/duplicado. Los grupos menores que k+1 se marcan sin medida; no se les asigna estabilidad perfecta. La coincidencia de vecinos entre modelos y la incertidumbre por muestreo son conceptos distintos y se documentarán por separado.

## Tiempo, Medicina y familias

Reutilizar y verificar todas las trayectorias por Field/pareja, no solo la media de cinco fechas. Mantener consulta/candidatos emparejados y dar cobertura de aumentos, descensos y no monotonía. No atribuir cambios a convergencia histórica causal ni usar el crecimiento de la búsqueda como si fuera tiempo.

La hipótesis de composición en Medicina se comprobará dentro de Subfields y con composiciones equilibradas frente a las distribuciones observadas, manteniendo tamaño y fechas cuando sean comparables. Describir cuánto cambia la diferencia al retirar BioBERT/PubMedBERT; no atribuirles el resto ni llamar causal al residuo. Las etiquetas OpenAlex no son verdad externa.

Documentar por separado arquitectura, linaje/pesos iniciales, corpus, señal/objetivo de ajuste y especialización. Son diez modelos fijos con factores confundidos; comprobar rango e identificabilidad antes de separar coeficientes. Si una causa no puede aislarse, declararlo y conservar asociaciones descriptivas, permutaciones de nombres y omisiones. Repetir la lectura con las tres recetas.

## Medidas, controles, literatura y cierre

Conservar por ahora CKA corregida principal; Procrustes y correlación de rangos como comprobaciones sobre los mismos IDs, kNN para lo local. La revisión de consistencia decidirá explícitamente si una medida adicional resuelve una carencia concreta. No añadir morfología por acumular índices; si se añade, dispersión, dimensionalidad y conectividad serán resultados distintos y no sinónimos de robustez.

Revisar individualmente las 50 alertas iniciales y las nuevas, con sus reglas originales y más repeticiones cuando ayuden a precisar su diagnóstico. Auditar controles aleatorios, texto común, MiniLM 256/512, calidad y duplicados. Una matriz de conclusiones indicará cuáles resisten cada control y cuáles cambian.

Actualizar búsqueda fechada y comparar explícitamente los antecedentes solicitados, con nivel de acceso. Congelar las respuestas originales recibidas de OpenAlex y el corpus derivado mediante huellas, aclarando que una extracción paginada no es una instantánea global simultánea del servicio. Las versiones de los diez modelos siguen fijadas. Cerrar solo con auditoría requisito por requisito de R01–R12 y catálogo actualizado.

## Precisiones fijadas antes de los nuevos controles correspondientes

- Tamaños y repeticiones de Subfields: `config/subfield_controls_v1.json`; 20 selecciones anidadas de hasta 256 y 512 desde cada grupo completo. Se conserva el rango y el cambio al duplicar, con grupos de menos de ocho sin diagnóstico de dos tamaños. La comparación de grupos usa 256 como principal; 128/512 se contrastarán solo sobre grupos comunes. La fecha por Subfield usa 128 y requiere los cinco períodos elegibles.
- Composición: `config/medicine_composition_v1.json`. Diez selecciones de 2.048 por Field; cuotas temporales 410/410/410/409/409. Se compara la mezcla observada con cuotas iguales de Subfield dentro del mismo conjunto elegible. Se conservan 485.119 filas como universo elegible; se informan descartes. Energía y Enfermería tienen un solo Subfield elegible y no identifican un efecto de reequilibrar especialidades. Este control no iguala conceptos entre áreas ni identifica una causa.
- Familias: `config/family_traits_v2.json`. Refinamiento posterior a resultados previos, con configuraciones reales de arquitectura y grupos documentados de linaje/corpus/señal/dominio separados. El grupo de corpus es una categoría de fuentes, no una lista de los artículos compartidos durante entrenamiento. Rango completo del diseño no elimina confusión causal, panel pequeño o sensibilidad a omitir un modelo.
- Cien selecciones de entradas: `config/input_stability100_v1.json`. Primeras veinte verificadas contra cada padre y mismas reglas. Guardar las transiciones de todas las alertas y si el rango del contraste cruza cero; estabilidad del valor y signo distinto de cero no son lo mismo.
