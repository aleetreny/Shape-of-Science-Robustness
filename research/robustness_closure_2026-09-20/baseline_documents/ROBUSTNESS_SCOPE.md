# Cierre experimental ampliado, solicitado el 17-09-2026

Esta petición amplía las dos fases terminadas. **Meta completa verificada: R01–R12 cerrados.** Evidencia conjunta en `data/robustness_v2/final_audit/`, presentación en `reports/robustness_v2/final/` y cierre documental en `research/robustness_2026-09-17/closure_audit.json`. No equivale a empezar la redacción ni publicar. Se conservarán los resultados y programas anteriores; la ampliación tendrá salidas y configuraciones separadas.

## Petición íntegra del usuario

### Siguientes tareas

-  **Ampliar el experimento de input de 26k a 52k** manteniendo exactamente el mismo diseño estratificado.
-  Repetir para 52k las comparaciones `title / abstract / title+abstract`.
-  Recalcular CKA y kNN para esas tres condiciones.
-  Revisar si las **31 alertas** del piloto se reducen o persisten. 
-  Documentar definitivamente qué representa `mean`, `CLS` y `SEP`, y dejar trazabilidad de cuál se usa como receta principal.
-  Comprobar si la elección `mean / CLS / SEP` altera de forma relevante las conclusiones por modelo, Field e input. 
-  **Bajar de Field a Subfield** y repetir las comparaciones principales.
-  Comparar si el agreement cambia de forma sistemática entre:
  - Field
  - Subfield
  - paper neighborhood
-  Revisar si aparece una transición clara de mayor a menor robustez conforme aumenta el nivel de detalle.
-  Controlar el efecto del tamaño de cada Subfield.
-  Calcular **estabilidad por Subfield**.
-  Calcular **estabilidad por paper**.
-  Identificar qué papers/regiones conservan sus vecinos entre modelos.
-  Identificar qué papers/regiones cambian mucho según el embedding.
-  Ver si esas zonas estables/inestables se concentran en ciertas disciplinas, Subfields o periodos.
-  Revisar de nuevo el análisis temporal usando conjuntos de candidatos comparables.
-  Ver si la evolución temporal de CKA es consistente entre Fields y pares de modelos.
-  Mantener separado el efecto temporal del efecto de tamaño del conjunto de búsqueda, porque el signo de kNN cambia según ese control. 
-  Profundizar en **modelo × disciplina**.
-  Revisar por qué Medicina tiene menor agreement.
-  Revisar la hipótesis de diversidad/composición de Subfields.
-  Comprobar si los modelos biomédicos explican parte, pero no todo, del efecto. 
-  Profundizar en **familias de modelos**.
-  Separar, cuando sea posible:
  - arquitectura
  - corpus de entrenamiento
  - training objective
  - especialización de dominio
-  Revisar hasta qué punto los modelos de la misma familia realmente se parecen más entre sí.
-  Comprobar cómo cambia esa lectura con `mean / CLS / SEP`. 
-  Cerrar qué métricas se van a mantener como principales.
-  Revisar consistencia entre CKA, Procrustes y correlación de rangos.
-  Mantener kNN como análisis local y revisar sensibilidad a `k = 10, 25, 50`. 
-  Decidir si hace falta añadir alguna métrica geométrica adicional.
-  Si se añade morfología, estudiar por separado:
  - dispersión
  - dimensionalidad intrínseca
  - fragmentación/conectividad
-  Revisar las **50 alertas de estabilidad** de la fase principal.
-  Revisar las alertas nuevas del experimento de input.
-  Mantener identificados los casos donde pequeñas diferencias no son suficientemente estables. 
-  Formalizar cómo se reporta la estabilidad de muestreo.
-  Revisar el control de grupos aleatorios.
-  Revisar el control de texto común.
-  Revisar MiniLM 256 vs 512.
-  Revisar filtros de calidad y duplicados.
-  Revisar que las conclusiones principales no dependan de una única decisión técnica.
-  Actualizar la búsqueda de literatura relacionada antes de cerrar la parte experimental.
-  Comparar explícitamente resultados y diseño frente a:
  - Constantino et al.
  - Lamers et al.
  - *The Landscape of Biomedical Research*
  - Imel & Hafen
  - Xie & Waltman
  - trabajos recientes de cross-model robustness
-  Revisar si ha aparecido algo nuevo en 2025–2026 que se solape directamente con el enfoque.
-  Dejar todos los outputs bien auditados y reproducibles.
-  Congelar configuraciones, versiones de modelos y snapshot de OpenAlex.
-  Actualizar el inventario de datos/resultados una vez terminados estos análisis.

Hasta aquí llegaría antes de empezar a redactar el paper.

## Evidencia necesaria para cerrar la meta

| ID | Requisito comprobable | Evidencia que debe existir | Estado |
| --- | --- | --- | --- |
| R01 | 52.000 con mismo diseño, tres entradas, CKA/kNN y seguimiento de las 31 alertas | Selección anidada de 400 por área/período; 30 condiciones auditadas; comparaciones nuevas y tabla de transición de alertas | Comprobado: input_review, input_stability100 y auditoría independiente de las 30 condiciones |
| R02 | Significado exacto y trazabilidad mean/CLS/SEP; efecto por modelo/Field/input | Documento ligado al código/tokenizador y cruce completo de recetas sobre 52k, con casos que cambian | Comprobado: POOLING.md e input_recipes sobre 52k |
| R03 | Subfields, jerarquía de escalas y tamaño de candidatos | Comparaciones principales por Subfield, controles de tamaño compartido y cobertura/exclusiones explícitas | Comprobado: SCALES_AND_DISCIPLINES.md; subfields_native y subfield_controls |
| R04 | Estabilidad por Subfield y paper; zonas estables/inestables | Tablas por ID/grupo, controles de selección/tamaño, distribución por disciplina/Subfield/período | Comprobado: SCALES_AND_DISCIPLINES.md; regions_native y paired_neighbor_scales |
| R05 | Tiempo con candidatos comparables y consistencia de CKA | Trayectorias por Field/pareja y resúmenes de heterogeneidad; consultas/candidatos emparejados y tamaños separados | Comprobado: TEMPORAL_REVIEW.md; temporal_review y candidate_check |
| R06 | Medicina y composición de Subfields; parte atribuible a biomédicos | Comparaciones dentro de Subfields y composiciones equilibradas, con y sin los dos biomédicos; límites causales | Comprobado: SCALES_AND_DISCIPLINES.md; medicine_composition y structural_review_v3 |
| R07 | Familias: arquitectura, corpus, objetivo y dominio; dependencia de receta | Fuentes verificadas, rasgos separados, rango/identificabilidad del diseño, asociaciones y sensibilidades | Comprobado: MODEL_FAMILIES.md; family_traits |
| R08 | Métricas principales, consistencia y decisión de morfología | CKA/Procrustes/rangos sobre mismos IDs; k=10/25/50; decisión justificada sobre métricas nuevas y separación si se añaden | Comprobado: METRICS.md; control_review_v2 |
| R09 | Alertas iniciales/nuevas y reporte formal de estabilidad | Seguimiento de las 50 y 31 alertas, incertidumbre de selección explícita, casos pequeños identificados sin cambiar umbrales retrospectivamente | Comprobado: SAMPLING_STABILITY.md; 50 originales conservadas, 31 claves trazadas y 100 selecciones en ambos tamaños |
| R10 | Controles aleatorios/texto/MiniLM/calidad/duplicados y conclusiones | Revisión trazable de cada control y matriz de conclusiones que resisten o cambian | Comprobado: CONCLUSION_CONTROLS.md; control_review_v2 y controles emparejados |
| R11 | Literatura y antecedentes nombrados, incluidos 2025–26 | Búsqueda fechada, fuentes primarias y tabla comparativa de cada antecedente y solapamientos | Comprobado: research/robustness_2026-09-17/RELATED_WORK_UPDATE.md |
| R12 | Auditoría, reproducción, versiones y snapshot, inventario | Configuraciones y manifiestos congelados, datos de origen preservados, catálogo actualizado y verificación requisito por requisito | Comprobado: final_audit, provenance, catálogo, revisión visual y cierre documental |

Un resultado heredado solo satisface un requisito tras comprobar su alcance actual. Una tabla parcial, un proceso lanzado o un test que pasa no cierran por sí solos estos requisitos. Las conclusiones negativas o no identificables se documentarán; no se inventarán separaciones causales que estos diez modelos no permitan.
