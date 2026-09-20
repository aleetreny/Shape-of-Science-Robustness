# Protocolo del cierre final, 20-09-2026

Fijado tras auditar implementaciones y recuentos, **antes de calcular o leer las nuevas comparaciones**. Son controles posteriores a los resultados originales, no un preregistro del estudio. Alcance: `ROBUSTNESS_CLOSURE_SCOPE.md`. Configuración ejecutable: `config/robustness_closure_v1.json`.

## Centros

Se mantiene la receta: normalizar cada artículo, promediar dentro del grupo, normalizar cada centro y aplicar la CKA corregida existente. Siempre coinciden los IDs entre modelos. Para 26 áreas y las mismas 217 subáreas elegibles se hacen 50 selecciones de 256 artículos. Cada grupo conserva exactamente sus cinco recuentos de período de la selección original; solo cambian los artículos dentro de cada período.

El control de tamaño usa las mismas 26 áreas y las mismas 183 subáreas con al menos 512 artículos. Hay 50 selecciones anidadas de 128, 256 y 512 por grupo. Los recuentos a 512 proceden del prefijo original por hash; los tamaños menores se obtienen por reparto proporcional entero (restos mayores, desempate por período). Se conserva así una composición común, salvo el redondeo inevitable. Este control tiene su propia composición; no se confunde su 256 con el 256 del análisis anterior.

Cada diseño tiene 50 referencias aleatorias, una por selección: los mismos artículos se reasignan entre grupos dentro de cada período, conservando los recuentos de cada grupo. Son referencias descriptivas del efecto de promediar, no una distribución nula para pruebas de significación. Se comparan distribuciones de medias y, por separado, las 45 parejas concretas.

Se omite cada área a partir de los centros originales y de las 50 nuevas selecciones; se guarda el cambio por pareja de modelos. La comparación restringida usa 50 elecciones de una subárea por área, con diez selecciones de artículos para cada elección. Todas mantienen las cuotas de período originales de su subárea. Se distingue la dispersión entre las 50 medias de selección de subáreas y la dispersión de artículos dentro de cada elección; no se presenta como una descomposición causal ni poblacional. Se añade una referencia aleatoria emparejada por cada repetición.

## Modelo frente a quitar el resumen

Sobre los mismos 52.000 artículos de las tres entradas se hacen 50 selecciones de 200 artículos por área/período: 26.000 en cada repetición y 1.000 candidatos/consultas por área. El resultado original de 52.000 se conserva como comparación de tamaño, no se sustituye. Los vecinos se buscan exactamente dentro de cada selección, excluyendo el propio artículo. Se reutiliza el orden completo de similitudes para filtrar candidatos; se contrasta esta implementación con búsquedas directas.

Se compara cambiar de modelo con título+resumen (45 parejas) frente a pasar de título+resumen a título en cada modelo (diez contrastes). Cada área y cada modelo tienen el mismo peso. Diferencia: **cambio al quitar resumen menos cambio al cambiar modelo**. Se guardan valores por repetición/área/pareja/modelo, k=10/25/50 con receta principal y k=25 con CLS/SEP para los cuatro BERT. Se publican media, mediana, percentiles 2,5/97,5, extremos y frecuencia de signo contrario al resultado completo de esa misma receta y k. Ningún margen de equivalencia se introduce a posteriori.

## Forma y medidas alternativas

Se reutilizan sin cambiar las 26 selecciones guardadas: principal, veinte mitades y cinco selecciones de 2.000 artículos. Por modelo, la referencia global es la media de los vectores unitarios del panel equilibrado original de 52.000. A cada vector unitario se resta esa misma referencia y se vuelve a normalizar. La referencia no se recalcula por área o selección. Se calculan apertura angular y PR en todas las selecciones.

En las representaciones originales se completan dimensión por entropía y D80 en esas mismas 26 selecciones. Se reutilizan y verifican valores ya disponibles. No se añade otra medida. Se mantienen las 325 parejas, diez modelos, fórmula relativa `2*(B-A)/(A+B)`, tolerancia 1e-10 y cortes 0/1/5/10 %. Persistencia exige la misma dirección en las 26 selecciones. Un empate D80 es no resuelto. Se conserva la identidad y dirección de cada pareja de modelos que daba respuestas opuestas; se diferencia retener esos testigos de encontrar otros distintos.

## Calidad y vecinos

Se reutiliza **exactamente** `strict_quality`: siete indicadores y componentes de DOI/texto normalizado idéntico. Quedan 448.886 registros. No se añade una regla de similitud textual ni se afirma haber eliminado todo duplicado o error temático.

1. Búsqueda completa: todos los artículos conservados como consultas y candidatos dentro de las 130 celdas. Comparación con los vecinos originales de **esas mismas consultas**, además de mostrar el promedio original con todas las consultas. Se separa así cambiar consultas de cambiar candidatos. k=10/25/50.
2. Tamaño fijo: 2.048 candidatos en las 63 celdas que lo permiten después del filtro; además 1.024 en las 130, para no basar el control general solo en las celdas grandes. Cien consultas limpias fijas, presentes en ambos grupos; se completan candidatos por orden aleatorio determinista en corpus original o filtrado. Este control está condicionado a las mismas consultas y no es una muestra libre de candidatos. k=10/25/50.
3. Entradas: el mínimo limpio es 235 de 400 por celda. Se usan 200 candidatos por período y área en ambos brazos (1.000 por área), con veinte consultas limpias por período, cien por área. Se conserva la misma consulta y la misma cantidad y fechas de candidatos en corpus original/filtrado; candidatos idénticos entre modelos y entradas dentro de cada brazo. Se comparan modelos y título/resumen/ambos con k=10/25/50. No hace falta inferencia adicional.

Se muestran cambios con signo y absolutos en puntos porcentuales, por área y pareja de modelos. Se distingue la sensibilidad al filtro de la calidad temática que no mide.

## Conservación, evidencia y cierre

Programas y configuraciones se sellan por rama antes de su ejecución. Cada archivo de selección, resultado y programa tiene huella; se conservan semillas y versiones. Reiniciar verifica las partes completadas; no mezcla versiones. Las pruebas de identidad, fórmula, empates y búsqueda se hacen antes de interpretar resultados. Los rangos son descriptivos dentro de este corpus, no intervalos poblacionales. No se presupone independencia de modelos, parejas o muestras solapadas.

Se publicará el recuento vigente de alertas locales (2.628/8.235) junto a la estabilidad del promedio. Solo tras congelar todas las ramas se auditan once afirmaciones, se actualizan ambos idiomas, se generan los informes solicitados y se comprueban los cuatro PDF. No se añade otro experimento salvo un error concreto que impida cerrar estas comprobaciones.
