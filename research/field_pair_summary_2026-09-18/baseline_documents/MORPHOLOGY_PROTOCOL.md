# Piloto de propiedades de la forma

18-09-2026. Exploración solicitada después del cierre del estudio. Diseño fijado antes de calcular estos resultados reales; **no es un preregistro de todo el proyecto**. Se conserva `METRICS.md` como decisión histórica. Configuración exacta: [morphology_pilot_v1.json](config/morphology_pilot_v1.json).

## Pregunta y alcance

¿Cambiar de encoder modifica cuánto se abre una nube, cómo reparte su variación entre direcciones y cómo se conecta? ¿Cambia también el orden relativo de las 26 áreas? No se busca declarar un modelo ganador ni convertir una propiedad geométrica en diversidad, calidad o fragmentación temática verdaderas.

Diez modelos, vectores ya calculados. Principal: título + resumen y recetas vigentes, mismos 52.000 artículos (2.000 por Field, 400 por período). Igual tamaño y fechas favorecen la comparación entre áreas; no representan su peso mundial. Subfields no pasan a ser la unidad principal. Sin extracción ni inferencia nueva.

## Medidas y alternativas

| Propiedad | Medida principal | Comprobaciones | Límite |
| --- | --- | --- | --- |
| Apertura angular | Mediana del ángulo entre todos los pares, en grados. | Cuantiles 10/90, ángulo mediano al centro; referencia global equilibrada y centrado global separado. | El origen y la receta del encoder importan; no es isotropía ni diversidad temática. Ángulo/cuerda/coseno son transformaciones relacionadas, no tres evidencias independientes. |
| Reparto entre direcciones | PR: cuadrado de la suma de autovalores de covarianza centrada dividido por suma de sus cuadrados. | Entropía efectiva de **covarianza**, D80 y primera dirección; tamaños 500/1.000/2.000/4.000. | Son resúmenes distintos del mismo espectro, no conteos de temas ni dimensión intrínseca verdadera. El número de coordenadas y la muestra condicionan el valor. |
| Conexión | Segundo autovalor del Laplaciano normalizado del grafo unión de 25 vecinos; cero si desconectado. Mayor valor significa conexión más fuerte. | k=10/50; pesos por escala local; grafos de vecinos mutuos; curva de componentes por distancia mediante enlace simple/MST; radios de conexión al 50/90/95/99/100% y arista máxima. | Alargamiento, pocas direcciones, densidad, puentes y extremos pueden simular separación. **No se le llama fragmentación temática.** |

Se normaliza cada vector a longitud uno en float64. Distancia de cuerda euclídea para grafos y enlace simple; el orden es el del coseno. Ángulo = 2 asin(cuerda/2). El centro se resta solo para covarianza, salvo el control explícito de centrado global. Distancias en todas las coordenadas: ninguna se mide sobre UMAP/PCA2D. Empates ordenados por índice global. No se combinan medidas en una nota total.

## Controles fijados

- Pruebas anteriores a resultados: nubes redondas, estrechas/abiertas, alargadas, de pocas direcciones, dos/cuatro grupos, puentes y extremos. Rotaciones, escala positiva, traslación donde corresponda, cálculo independiente por SVD y MST. Resultados numéricos y fallos de interpretación se conservan.
- Selección: 20 medias muestras estratificadas de 1.000 dentro de los 52k, idénticas entre modelos. Cinco selecciones adicionales de 2.000 desde los 500k congelados. No son muestras de encoders ni intervalos poblacionales. Comprobar tamaños 500, 1.000, 2.000 y 4.000; el último procede del corpus completo y cambia también los IDs.
- Misma selección de 1.000 para entradas título/resumen/ambos y CLS/SEP de los cuatro BERT; repetir las medidas alternativas. Texto común: los 52k independientes del control anterior, comparados con su propio título+resumen sobre IDs idénticos. MiniLM512 separado, mismos IDs que el principal.
- Marcas de calidad: conservar los artículos elegibles de la media muestra y reponer por orden aleatorio fijado dentro de cada celda hasta mantener 200 por período. No corrige ni cuantifica errores temáticos de OpenAlex. Retirar además 5% de puntos alejados por período y comparar con retirar 5% aleatorios; nunca cambiar el corpus.
- Restar el centro global equilibrado de cada modelo y volver a normalizar, como sensibilidad explícita a su dirección común. No sustituye el uso habitual.
- Tres referencias gaussianas por modelo/área a 1.000: media/covarianza iguales **en expectativa antes de normalizar**. Guardar el desajuste de apertura/dimensión tras normalización. Son referencias geométricas descriptivas, no nulos semánticos ni pruebas con p-valores. No afirmar que aíslan perfectamente fragmentación.
- Tiempo: cinco períodos de 400; diez selecciones de 200 en cada extremo (2000–04, 2020–24). Comparación emparejada y tamaños iguales; no explicaciones causales ni precisión sobre la población mundial.

## Reglas de lectura

Se muestra sensibilidad continua, inversión de orden, concordancia entre métricas y comparación de la variación por muestra frente a las diferencias de modelos/áreas. Cribas operativas: amplitud central 90% y cambio mediano relativo 5% en apertura, 10% en PR, 20% en conexión. Referencia de ordenación: mediana de Spearman ≥0,90 y decil inferior ≥0,80. No son estándares de publicación ni evidencia de validez temática; no se modifican después para hacer pasar resultados. No convertir saturación en estabilidad informativa.

La descomposición modelo/área/interacción será descriptiva, con pesos iguales y sin tratar los 45 pares de modelos como independientes. No llamar causal a una asociación con familia, año o área. Si las medidas de conexión discrepan o no distinguen alargamiento de grupos en controles, se informa y no se promociona una conclusión genérica sobre fragmentación. La recomendación de incluir esta ampliación en el paper dependerá de lo que resista, no de lo llamativo del resultado.

## Antecedentes que justifican las precauciones

- [Rudman et al., 2022](https://aclanthology.org/2022.findings-acl.262/): separar isotropía de la dirección media y exigir invariancias. Aquí se mide apertura y espectro por separado; no se etiqueta el coseno medio como isotropía.
- [Roy y Vetterli, 2007](https://www.eurasip.org/Proceedings/Eusipco/Eusipco2007/Papers/a5p-h05.pdf): entropía del espectro; se especifica que aquí es el espectro de covarianza. PR y D80 no son métodos independientes de ese espectro.
- [von Luxburg, 2007](https://www.tml.cs.uni-tuebingen.de/team/luxburg/publications/Luxburg07_tutorial.pdf) y [Zelnik-Manor y Perona, 2004](https://proceedings.neurips.cc/paper_files/paper/2004/hash/40173ea48d9567f1f393b20c855bb40b-Abstract.html): construcción y escala del grafo condicionan conectividad; comprobar varias reglas y escala local.
- [Rolle y Scoccola, 2024](https://www.jmlr.org/papers/v25/21-1185.html): estabilidad de estructuras de agrupación no autoriza a ignorar parámetros/densidad/ruido. Este piloto no implementa su método ni reclama sus garantías.
- [Erba et al., 2019](https://www.nature.com/articles/s41598-019-53549-9): estimadores locales pueden fallar con muestreo escaso. Se evita presentar PR como dimensión intrínseca verdadera.
- [Imel y Hafen, 2025](https://arxiv.org/html/2506.23366v1): antecedente directo de geometría local en literatura científica; nuestra pregunta es dependencia de las descripciones respecto al encoder, no predecir citas.

Las herramientas de búsqueda/metadatos siguen la procedencia ya registrada: [Kassis et al., 2026, v2](https://arxiv.org/abs/2609.00065v2). No constituyen validación de las medidas. No se garantiza aprobación por revisores.
