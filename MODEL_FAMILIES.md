# Qué significa que dos modelos sean de la misma familia

**Compartir entrenamiento suele importar, pero nuestros diez modelos no permiten separar cada causa de forma limpia.** No hay diez experimentos donde se cambie una sola pieza: varios rasgos cambian juntos.

Se documentaron por separado arquitectura, linaje, fuente de entrenamiento, objetivo y dominio. Tabla exacta, revisiones, configuración y vocabularios: `data/robustness_v2/family_traits/model_traits.csv`. Las fuentes oficiales corresponden a los modelos fijados, no a una versión actual descargada después.

| Modelos | Parentesco que usamos | Diferencias que conservamos |
| --- | --- | --- |
| SPECTER, SPECTER2, SciNCL | Linaje SciBERT y aprendizaje de relaciones entre documentos apoyado en citas | Muestreo/entrenamiento distintos; SPECTER2 añade adaptador. No son tres semillas independientes del mismo modelo. |
| SciBERT | Linaje científico, objetivo de predecir palabras | No tiene el mismo ajuste documental que los tres anteriores. |
| MPNet, MiniLM | Ajuste de pares de frases, fuentes de Sentence-Transformers | Arquitecturas y tamaños diferentes. MiniLM tiene 6 capas/384 posiciones numéricas de salida; MPNet, 12/768. |
| BERT, BioBERT, SimCSE | Linaje amplio BERT | BioBERT continúa con textos biomédicos; SimCSE añade aprendizaje contrastivo mediante dropout; BERT conserva su objetivo de palabras. |
| PubMedBERT | Modelo entrenado desde cero con vocabulario y textos biomédicos | No es simplemente BERT al que se ha añadido BioBERT; la variante fijada usa abstracts y texto completo. |

Las categorías de corpus son fuentes documentadas, **no una medición de cuántos artículos de entrenamiento comparten realmente**. El dominio «general» no significa ausencia de ciencia. La arquitectura se comprobó en las configuraciones guardadas: MPNet no se etiquetó como BERT porque tenga también 768 números.

Hay una peculiaridad conservada de SPECTER: el tokenizador declara linaje SciBERT cased, pero su configuración fijada convierte a minúsculas. Se registra su vocabulario y configuración reales; no se corrigió como si fuera un fallo nuevo ni se recalcularon sus vectores.

## Análisis y límite

Se ajustaron asociaciones de seis indicadores entre pares, con permutaciones simultáneas de nombres de modelos y omisión de uno cada vez. Son descripciones de este panel fijo; los 45 pares no se trataron como 45 observaciones independientes. La refinación de estos rasgos es **posterior** al primer resultado y se documenta así.

Con mean principal, compartir objetivo y linaje tiene asociación positiva y mantiene su signo al omitir cada modelo. La asociación con objetivo también es positiva con CLS cuando el ajuste es identificable. Con SEP cambia mucho: su signo deja de ser consistente. Por tanto, una explicación de familias que omita la receta sería incompleta.

El ajuste describe aproximadamente el 74% de la variación entre los 45 valores medios de CKA con mean, 46% con CLS y 26% con SEP. Esos porcentajes son del ajuste descriptivo en estos diez modelos: **no son porcentajes de geometría causados por el entrenamiento**, ni de ciencia bien representada. La condición de rango completo del ajuste no elimina factores confundidos. Algunas omisiones con CLS/SEP dejan coeficientes sin identificar; aparecen vacíos, no inventados.

Los coeficientes negativos para compartir arquitectura o ciertas fuentes no justifican afirmar que compartirlas perjudique el mapa. Dependen del panel, otras variables y receta. No se elige un ganador por pertenecer al grupo con mayor consenso.

Resultados, rangos de omisiones y controles de calidad/tamaño: `family_traits/` y `structural_review_v3/family_trait_omission_ranges.csv`, bajo `data/robustness_v2/`. Antecedente metodológico directo: [Caspari et al. (2024)](https://arxiv.org/html/2407.08275v1), que ya estudia CKA, recuperación y familias. Nuestro valor añadido debe estar en localizar la dependencia de decisiones al mapear ciencia, no en atribuirnos esa combinación de medidas.
