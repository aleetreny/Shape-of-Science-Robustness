# Revisión final y preparación de la siguiente fase

**Revisión terminada el 17-09-2026.** Los diez resultados completos, el corpus y los controles técnicos pasaron las comprobaciones. Informe: `EMBEDDINGS_AUDIT.md`. Organización: `DATA_CATALOG.md`. Propuesta siguiente: `ANALYSIS_PROPOSAL.md`. Las instrucciones siguientes conservan el plan ejecutado; no hay que reiniciar el seguimiento.

**Petición del usuario, 16-09-2026:** comprobar progreso y dejar un recordatorio para revisar todo al finalizar, ordenar los datos y preparar la siguiente fase. Autoriza la revisión y organización técnica. No implica cambiar decisiones científicas todavía abiertas ni iniciar experimentos nuevos por defecto.

## Estado histórico al programar la revisión, 16-09-2026

A las 23:31 del 16 de septiembre, hora de Madrid, hay siete modelos completos: SPECTER, SPECTER2, SciNCL, SciBERT, BERT, MPNet y MiniLM. Sus validaciones guardadas declaran 500.000 filas y coinciden con sus manifiestos; sus programas y configuraciones permanecen sin cambios. PubMedBERT lleva 209.920 filas y está activo. BioBERT y SimCSE no han comenzado.

Estimación orientativa: 7–9 horas adicionales de cálculo continuo. Se combinan la velocidad de los veinte bloques recientes de PubMedBERT con los tiempos de las pruebas de BioBERT/SimCSE. No es una garantía, y la revisión final añade tiempo. Evidencia: `research/embedding_review_2026-09-16/progress_snapshot.json`.

Esta comprobación es de avance y procedencia. La revisión completa de todos los vectores se hará al acabar. No se han cambiado los datos ni el programa en ejecución.

## Procedimiento de seguimiento ya ejecutado

1. Leer `AGENTS.md`, `DECISIONS.md`, `progress.md` y `task_plan.md`. Revisar el estado actual de la automatización para no duplicar el trabajo.
2. Consultar `./embed.sh status --scope full`, los procesos reales y `data/embeddings_run.log`. Un estado guardado «running» no prueba que siga activo. Comprobar que los bloques avanzan; una pausa del usuario no autoriza reiniciar el cálculo.
3. Si sigue trabajando sin problemas, esperar a la siguiente comprobación. No modificar, mover ni borrar `sos_embed/`, configuración, entorno, pesos, corpus o bloques de resultados. No lanzar otra instancia. Si hay una parada o error, comprobarlo y avisar con una acción concreta.
4. Cuando estén los diez completos y la cola haya terminado, empezar la revisión siguiente. No anunciar «todo listo» basándose solo en el contador.

## Revisión final autorizada

- Ejecutar `./prepare.sh preflight` y `./embed.sh verify --scope full`, guardando las salidas en una carpeta nueva de auditoría. Son comprobaciones; no calculan otra vez los embeddings.
- Comprobar diez modelos, 500.000 filas en cada uno, mismos IDs/orden/huellas de los textos, dimensiones esperadas, ausencia de valores inválidos y bloques completos sin huecos. Mantener media/CLS/SEP como variantes de cuatro modelos, no como modelos independientes.
- Contrastar pesos, revisiones, programa, dependencias y manifiestos con lo fijado. Conservar la evidencia original y las copias del programa. Ante un fallo, aislar el diagnóstico sin sobreescribir resultados o reiniciar horas de cálculo automáticamente.
- Preparar un catálogo de archivos y modelos con rutas, filas, variantes, dimensiones, versiones y resultado de validación. Organizar mediante índices y documentación; conservar las rutas congeladas y evitar copias grandes innecesarias. Si se necesita un archivo derivado, crearlo por separado y documentar su origen.
- Resumir cuánto texto recortó cada modelo, en total y por área/período. Conservar el vínculo con año, grupo base/complemento, calidad y duplicados. No transformar esas marcas en exclusiones nuevas sin decisión.
- Verificar el control técnico de fragmento común y su alineación con la prueba nativa. Sus 1.300 artículos siguen siendo una prueba técnica, no el tamaño científico definitivo del control.
- Crear un informe final breve con lo comprobado, incidencias, límites y rutas. Actualizar `EMBEDDINGS_READY.md`, `NEXT_STEPS.md`, `DECISIONS.md`, `findings.md`, `progress.md` y `task_plan.md`.

## Dejar preparada la fase de comparación

Preparar el acceso a la misma colección de artículos desde todos los modelos, en bloques y sin cargar todo en memoria. Conservar separados los 400.000 de base y los 100.000 de complemento. Si hace falta código auxiliar, crearlo aparte del programa congelado y comprobar solo su lectura/alineación; no iniciar comparaciones científicas nuevas.

Dejar una propuesta corta y opciones claras para las decisiones pendientes: medida principal, tratamiento de la longitud de los vectores, forma principal de resumir los cuatro BERT de palabras, tamaño del control de texto común y comprobaciones de estabilidad/calidad. Pedir al usuario esas decisiones antes de cerrarlas, salvo nueva delegación explícita. No elegirlas mirando qué resultados quedan más atractivos.

Al terminar la auditoría y esta preparación técnica, avisar al usuario en español sencillo y desactivar el seguimiento temporal. Si solo queda una decisión suya, entregar lo preparado y preguntar de forma concreta; no mantener comprobaciones automáticas sin utilidad.
