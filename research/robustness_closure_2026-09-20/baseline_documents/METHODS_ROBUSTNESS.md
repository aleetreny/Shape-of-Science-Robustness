# Métodos del cierre experimental ampliado

Especificación reproducible del 17-09-2026. La pregunta sigue siendo la dependencia del mapa científico respecto a la representación. No se entrenaron modelos nuevos, no se amplió OpenAlex y no se alteraron el corpus ni los vectores originales. La ampliación usa `sos_deep/`, `config/*` específicos y `data/robustness_v2/`.

## Población, pesos y correspondencia

Corpus fijo: 500.000 IDs únicos, 400.000 base general y 100.000 complemento, 26 Fields, 2000–2024. Inglés según el proceso documentado, tipos article/review/conference-paper y abstract de al menos 50 palabras, junto con los filtros de `CORPUS_PROTOCOL.md` y `CLEANING.md`. Es una población de publicaciones elegibles y accesibles en OpenAlex, no toda la ciencia mundial.

Comparaciones por grupo y resúmenes dan el mismo peso a cada grupo/par según su tabla; no ponderan automáticamente por producción mundial. El complemento mejora cobertura y no se interpreta como muestra proporcional. `row_index`, `work_id` y huellas de texto unen exactamente los mismos artículos entre modelos.

## Entradas: ampliación anidada de 26.000 a 52.000

Configuraciones: `input52_v1.json`, `input52_recipes_v1.json`, `input_stability100_v1.json`. Misma semilla SHA de selección que el piloto; se pasa de 200 a 400 artículos por cada una de las 130 celdas Field×período. Se conservan los 26.000 y se añaden 26.000. La unidad de forma agrupa cinco períodos: 2.000 por Field, 400 en cada período.

Tres condiciones: título literal, abstract literal y combinación habitual título+abstract. En las entradas sencillas no se añade un separador por un campo vacío. Cada tokenizador conserva símbolos especiales y límite oficial. La combinación completa reutiliza exactamente los vectores originales. Las dos entradas sencillas reutilizan el piloto donde coincide el ID y solo infieren las filas nuevas. Diez modelos y 18 variantes guardadas, con las tres recetas de los cuatro BERT de palabras.

La auditoría independiente reconstruye texto formateado, secuencia de tokens, truncamiento, IDs y orden; comprueba bit a bit cada vector reutilizado, incluidas recetas alternativas. La prueba real de reanudación de MiniLM conservó el primer bloque; las diferencias de reejecución individual quedaron dentro de la tolerancia numérica declarada. Las huellas de código y entorno impiden reanudar con otra receta.

**Efecto de modelo:** desde título+abstract en un modelo, media de 1 menos acuerdo con los otros nueve modelos en esa misma entrada. **Efecto de entrada:** 1 menos acuerdo entre título+abstract y título solo o abstract solo dentro del mismo modelo. Se resta el segundo al primero sobre la misma medida y mismos IDs. Valor positivo: cambiar modelo mueve más esa medida; negativo: cambiar entrada mueve más. No es una comparación con verdad externa.

Se conserva también un resumen simétrico de todas las transiciones de entrada y cambios de modelo, evitando depender solo del anclaje completo. CKA y rangos describen forma; vecinos exactos usan k=10/25/50, candidatos comunes de 2.000 por Field y exclusión del propio documento. La principal de los cuatro BERT es mean; CLS/SEP cambian esos cuatro a la vez como escenarios alternativos. Por ello también varía la referencia con otros modelos: no atribuir toda diferencia de escenario a la receta de un único modelo.

## Estabilidad y alertas

Entradas: 20 y 100 selecciones sin reemplazo en **ambos** tamaños, manteniendo igual cantidad de cada período. Submuestras de 500 por área en 26k y 1.000 en 52k. Las primeras 20 se reproducen contra los archivos anteriores. Se guardan todos los IDs, valores, percentiles 2,5/97,5, diferencia de mediana, signo y cruce de cero.

Regla operativa heredada: cambio absoluto de mediana ≤0,02 y amplitud central ≤0,04. Se mantienen las 31 claves originales y cuatro estados: persiste, desaparece, nueva, sin alerta. Duplicar muestra y aumentar repeticiones se comparan por separado. «Sin alerta» no implica que el contraste sea distinto de cero.

Las 50 alertas de la fase de 500.000 se reconstruyen desde los valores brutos de 20 selecciones de 1.024/2.048 en cada celda. No se recalculó la regla ni se cambiaron umbrales. Son otra unidad y no se suman con las alertas de entrada o Subfields.

Subfields: 20 selecciones anidadas de hasta 256/512 desde cada grupo; tamaños limitados por disponibilidad. Grupos de menos de ocho sin diagnóstico de dos tamaños. Si la selección grande usa todo el grupo, su rango nulo se marca explícitamente. No se declara que eso produzca certeza poblacional. Detalles y límites en `SAMPLING_STABILITY.md`.

## Escalas y regiones

Comparación nativa en 252 Subfields agrupando años: CKA corregida con n≥4; vecinos cuando existe un universo informativo. Casos n=k+1 tienen todos los otros artículos como vecinos y no se consideran evidencia útil de acuerdo. Los 500.000 IDs se preservan.

Tamaños iguales 128/256/512 por área o especialidad; prefijos anidados de un orden SHA fijo, mismos IDs entre modelos/recetas. 183 Subfields compartidos por los tres tamaños. Control temporal separado: 125 especialidades con al menos 128 artículos en cada período; se conservan las mismas en las cinco fechas.

Centros: media de vectores de artículos con longitud uno; control directo de equivalencia entre sumar centros ponderados y calcular centros de área. Se estudian originales y 256 por grupo, 20 repartos aleatorios que preservan cantidades por período, y 20 selecciones de una especialidad por área para igualar a 26 centros. Los centros no son una proyección 2D. Comparar su acuerdo no equivale a comparar el interior de un grupo.

Vecindarios emparejados: 50 consultas fijas por cada una de 217 especialidades; 256 candidatos incluyendo las consultas, mismos conteos de fechas en búsqueda de especialidad y área. Diez selecciones por grupo. Se guardan candidatos, consultas, vecinos exactos por modelo y cuentas compartidas por par y k. Una consulta por modelo/selección/grupo/ámbito se contrasta con una ordenación independiente: 43.400 comprobaciones.

Aclaración de la revisión previa al manuscrito: las 50 consultas del mismo Subfield forman parte de ambos grupos de candidatos; solo los 206 restantes se sortean del ámbito correspondiente. La comparación amplia está condicionada por esas consultas y no equivale a 256 artículos libres del Field. Esta aclaración no cambia el cálculo congelado. Las etiquetas OpenAlex también pueden estar equivocadas: casos comprobados contra la fuente en [PREPAPER_REVIEW.md](PREPAPER_REVIEW.md).

Las puntuaciones por artículo de los universos completos incluyen omisión de cada modelo y de familias, sensibilidad a k y marcas de calidad. El control repetido de candidatos cubre 10.850 consultas, no los 500.000. Las colas empíricas localizan ejemplos; no son etiquetas universales de artículo estable/inestable.

## Tiempo, Medicina y familias

Tiempo: reconstrucción de las trayectorias por área/par, cambios entre extremos, pendiente y signos de los cuatro pasos, con controles de 2.048 candidatos, calidad y receta. La variación por seleccionar consultas se separa exactamente de cambiar candidatos. No inferir causas históricas, ni tratar 45 pares como independientes.

Composición: 2.048 por área; cuotas de fechas 410/410/410/409/409, diez repeticiones. Universo elegible común por área tras asegurar cuotas por especialidad en las cinco fechas; selección observada frente a reparto igual por especialidad. Se evalúan todos los pares, sin biomédicos, un biomédico y pareja biomédica. No se atribuye causalidad a la diferencia ni se igualan conceptos entre áreas. Energía y Enfermería tienen una única especialidad elegible: composición no contrastable ahí.

Familias: rasgos separados de arquitectura/configuración, linaje, grupo de fuentes de entrenamiento, objetivo y dominio; indicador de misma receta. Ajuste descriptivo de los 45 valores medios, rango del diseño, 5.000 permutaciones simultáneas de etiquetas de modelos, omisión de cada modelo y recetas mean/CLS/SEP. Coeficientes no identificables se guardan vacíos. Las categorías de corpus no miden solapamiento exacto de documentos. `MODEL_FAMILIES.md` detalla la interpretación.

## Medidas y orden de decisiones

`METRICS.md` fija el cierre: CKA corregida y vecinos k25 principales, Procrustes/rangos/k10/k50 como comprobaciones. No se añade dispersión, dimensión intrínseca o conectividad; son preguntas diferentes que necesitarían hipótesis y parámetros propios. Nunca se transforma CKA en porcentaje correcto.

Los protocolos de cada cálculo nuevo se fijaron antes de inspeccionar su resultado correspondiente, pero se diseñaron con conocimiento de fases previas. Los controles nuevos de composición/escala/rasgos son seguimientos; no presentar toda la ampliación como registro previo ciego. `DECISIONS.md`, manifiestos y copias de programas conservan el orden.

## Reproducción y origen

Cada ejecución científica conserva configuración, versiones, archivos fuente, huellas de entradas, selecciones, bloques y auditoría. Los originales se vuelven a verificar en `data/robustness_v2/provenance/`: 6.139 respuestas únicas comprimidas, recogidas el 15-09 entre 10:13 y 14:02 UTC; 4.890 bloques y 8.802 archivos de vectores originales. Estas páginas congeladas **no son una instantánea global simultánea de OpenAlex**. El enlace de preparación a páginas originales se conserva.

La auditoría de cierre revisa también los archivos de centros, matrices de vecinos, fuentes congeladas y cuotas reales de candidatos. Las pruebas separadas en los entornos apropiados cubren reutilización, reanudación, pequeños grupos, equivalencia numérica, omisiones y emparejamiento de fechas. No se actualizaron paquetes durante los cálculos.

La entrega se reconstruye desde las salidas auditadas, sin descargar ni inferir:

```sh
VECLIB_MAXIMUM_THREADS=4 .venv-analysis/bin/python -m sos_deep.report
```

Solo usar después de que `data/robustness_v2/final_audit/audit.json` marque todo completo. No ejecutar versiones fallidas o superadas del exportador estructural; la vigente es `structural_review_v3`. No mezclar el primer resumen MiniLM con el vigente `control_review_v2`, que separa la comparación consigo mismo. Los archivos grandes quedan locales y fuera de Git; un push del código no sería una copia de seguridad del corpus.
