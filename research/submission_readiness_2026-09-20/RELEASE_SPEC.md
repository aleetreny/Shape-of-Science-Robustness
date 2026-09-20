# Especificación propuesta del paquete público

Fecha: 20-09-2026. Estado: diseño comprobado contra los archivos locales; publicación y licencias pendientes. No es un depósito ni un manifiesto definitivo de archivos autorizados.

## Qué debe poder hacer un lector

| Recorrido | Entrada | Salida y criterio de aceptación | Estado |
| --- | --- | --- | --- |
| Documento | Fuentes LaTeX, tablas y figuras | Reconstruir artículo y suplemento. | Ya probado en la revisión de primera lectura. |
| Cifras | Valores por modelo, área y repetición; reglas congeladas | Obtener los resúmenes, denominadores y categorías publicados. | Demostración comprobada para parte de Figura 4; resto pendiente. |
| Análisis | Vectores congelados, metadatos y selecciones exactas | Recalcular medidas, listas de vecinos y controles usados en las conclusiones. | Datos locales disponibles; paquete independiente pendiente. |
| Representaciones | Entradas textuales históricas, recetas y revisiones de modelos | Volver a obtener vectores y evaluar la tolerancia numérica entre equipos. | Acceso/condiciones del texto y ejecución portable pendientes. |

No equiparar los cuatro recorridos. Un `manifest.json` que indica «completo» demuestra el estado histórico, pero no que una ejecución nueva haya repetido el cálculo.

## Registros propuestos

**Código:** repositorio GitHub actualizado y una versión archivada con DOI. Incluir todos los módulos científicos citados por el manuscrito, las copias de fuentes usadas en cada fase, configuraciones, protocolos, dependencias, instrucciones, comprobadores y una cita de software. Elegir licencia para el código propio antes de publicar la versión.

**Datos:** un registro Zenodo con archivos agrupados por componente, un índice ligero visible antes de descargar y enlaces a la versión de código. Citar el DOI de versión; mantener el enlace al DOI general solo como ayuda para descubrir versiones posteriores. Si la cuota disponible exige más de un registro, separarlos por contenido científico y enlazarlos, conservando un manifiesto general.

El tamaño de 57,576 GB es el total lógico de las carpetas de embeddings y análisis inventariadas. Incluye derivados y duplicados; algunas carpetas contienen texto. **No es una lista de permiso de publicación ni una orden de comprimir `data/` completa.** El tamaño final se obtendrá después de seleccionar archivos y revisar su procedencia.

## Componentes que deben quedar identificados

| Componente | Fuente local vigente | Preparación necesaria |
| --- | --- | --- |
| Identidad de los 500.000 artículos | `data/analysis_ready_v1/metadata.parquet` (45,397 MB) | Diccionario de columnas y correspondencia `row_index`/`work_id`. Revisar las notas de calidad de texto libre. Mantener base/complemento, fechas, etiquetas, duplicados y huellas. |
| Vectores principales y recetas | `data/embeddings_v1/` (27,533 GB; 26,881 GB de `.npy`) | Agrupar por modelo; conservar `rows.parquet`, commits de bloques, manifiestos, orden y revisiones exactas de pesos/adaptadores. |
| Fragmento común de 52.000 y MiniLM 512 | `data/analysis_v1/controls/` (3,775 GB) | Conservar selección, correspondencias y vectores; separar textos de fragmentos y comprobar condiciones antes de incluirlos. |
| Título/resumen/ambos de 52.000 | `data/robustness_v2/inputs/` (8,727 GB) | Conservar las tres entradas y recetas necesarias. La de título + resumen reutiliza vectores previos: deduplicar solo con correspondencias comprobadas. |
| Primera prueba de 26.000 | `data/checklist_v1/inputs/` y comparaciones relacionadas | Incluir lo necesario para reproducir los recuentos históricos que sigue citando el artículo. No borrar el piloto del registro ni presentarlo como muestra independiente. |
| Selecciones y universo de búsqueda | `data/analysis_v1/`, `data/robustness_v2/`, `data/prepaper_v1/`, `data/morphology_pilot_v1/`, `data/robustness_closure_v1/` | Selecciones de IDs y candidatos, cuotas, semillas y correspondencias por fase. Explicitar qué 52.000 se usan en cada control. No reconstruir selecciones solo a partir de una semilla sin comprobar el orden de entrada. |
| Valores individuales y resultados finales | Carpetas anteriores; `reports/robustness_closure_v1/`; otros `reports/` citados por el manifiesto de presentación | Separar medidas por condición de resúmenes finales. Mantener originales, alertas y resultados que quedan sin resolver. |
| Fuentes y entornos | `source_snapshot/`, manifiestos de ejecución, `requirements-*.txt`, `config/` | Registro de versión/hardware y entorno instalable verificado. Los embeddings originales se ejecutaron con MPS; no prometer igualdad bit a bit al regenerarlos en otro hardware. |
| Textos y procedencia | `data/corpus_clean_v1/embedding_input.parquet`, `corpus.parquet` y respuestas históricas | Revisar qué se puede compartir y con qué condiciones. Un enlace a la API actual no es un sustituto de estas entradas exactas. |

No incluir por defecto pesos, entornos, secretos, `.env`, cachés, copias completas de literatura, registros ajenos al estudio o todas las carpetas históricas. Las licencias de dependencias y materiales de terceros no se sustituyen por la licencia del código propio.

## Cobertura mínima del artículo

| Resultado | Insumos y programas que debe cubrir la prueba independiente |
| --- | --- |
| Figura 1: centros y estructura interna | Vectores, metadatos y selecciones; fases `sos_analysis`, `sos_deep` y `sos_closure.centres`. Incluir grupos aleatorios, omisiones y 2.628/8.235 alertas locales. |
| Vecinos y Figura 2: especialidad/área | Candidatos y consultas exactos, fechas, emparejamiento de los 50 artículos y elecciones de los otros 206; `sos_deep` y atlas. Reproducir 127/217, 90/217 y el cambio medio. |
| Figura 3: texto frente a modelo | Entradas del mismo conjunto de 52.000, recetas, selecciones de 1.000 candidatos por área y programa del contraste de `sos_closure.headline`. Incluir medias por modelo y receta, no solo la media general. |
| Figura 4: comparaciones entre áreas | Selecciones de morfología, vectores, fórmulas y fuentes de `sos_morphology`, `sos_pair_summary`, `sos_closure.morphology` y resumen. Comprobar las 26 condiciones, cortes, alternativas y conservación de modelos opuestos. |
| Calidad, tiempo, familias, atlas y controles del suplemento | Las fases correspondientes de `sos_analysis`, `sos_followup`, `sos_deep`, `sos_review` y `sos_closure.quality`; índices de casos y datos por condición. La cobertura se debe cerrar fila por fila en el manifiesto de tablas/figuras. |

Esta tabla establece cobertura, no afirma que todos los comandos sean ya portables. La selección final de archivos debe resolver las dependencias de cada ejecutor y comprobarse en una carpeta nueva.

## Interfaz deseable

Se recomienda añadir un ejecutor separado de los programas científicos congelados, con estas funciones. **Los nombres siguientes son una propuesta; no son comandos implementados hoy.**

```text
verify_inputs       comprobar tamaños, SHA-256, esquema, filas e IDs
reproduce_summaries recalcular cifras y figuras desde medidas por condición
reproduce_analyses  recalcular desde los vectores depositados
audit_outputs       comparar recuentos, tablas, tolerancias y cobertura
```

El único comando nuevo implementado en esta revisión es `python3 -I -S reproduce.py`, dentro de `replication_demo/`. Es autónomo, usa la biblioteca estándar y no debe confundirse con el futuro ejecutor completo.

## Prueba de aceptación

1. Fijar un manifiesto por archivo, con ruta relativa, tamaño, SHA-256, etapa, procedencia y condiciones de reutilización. No crear enlaces de datos hasta que existan.
2. Extraer el paquete a un directorio limpio; permitir acceso solo a sus archivos. Durante esta prueba no se deben leer rutas del proyecto original, cachés personales ni salidas anteriores.
3. Comprobar orden, filas y conjuntos de IDs antes de cualquier operación numérica. Verificar aparte los dos conjuntos distintos de 52.000 y la inclusión de los 26.000 del piloto de texto.
4. Recalcular las cuatro figuras y todos los recuentos esenciales del suplemento. Registrar discrepancias sin ajustar umbrales científicos para hacerlas desaparecer.
5. Exigir igualdad en IDs, clases y recuentos discretos. Para valores en coma flotante, justificar y fijar tolerancias numéricas antes de la comparación; investigar cualquier cambio de clase cerca de un corte. Para inferencia en otro hardware, declarar el alcance comprobado.
6. Guardar comandos, versiones, duración, memoria máxima y tamaño de descarga. No se ha medido todavía el coste del paquete completo; no se ofrece una duración inventada.
7. Tras la autorización del depósito, verificar también que una descarga pública limpia coincide con el paquete probado. Actualizar entonces las referencias y la declaración de disponibilidad, sin prometer resultados de una prueba aún no realizada.

## Declaración de disponibilidad que habrá que redactar

La declaración final debe identificar el DOI de código y el de datos, sus versiones, el alcance de la reproducción desde vectores, las instrucciones y cualquier restricción real de las entradas textuales. Debe decir expresamente si se comprobó también la generación de embeddings o solo los análisis posteriores.

No se incluye una declaración que diga «todos los datos están disponibles» porque aún no se ha realizado el depósito. La declaración actual del artículo sigue siendo fiel al estado de hoy. Un DOI reservado sin publicar no debe presentarse como acceso público.
