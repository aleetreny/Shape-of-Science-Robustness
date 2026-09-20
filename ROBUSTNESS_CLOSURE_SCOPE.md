# Último cierre de robustez, 20-09-2026

**Terminado.** Los nueve puntos se han completado. [Informe y entregables](ROBUSTNESS_CLOSURE_REPORT.md) · [Cambios del manuscrito](ROBUSTNESS_MANUSCRIPT_CHANGELOG.md) · [Auditoría final](research/robustness_closure_2026-09-20/closure_audit.json). Lo que sigue conserva el alcance fijado antes de ejecutar. No reiniciar estas pruebas por retomar el proyecto.

El autor acepta el tono claro actual y delega aplicar la revisión independiente: «aplicala como consideres». Petición completa conservada en `research/robustness_closure_2026-09-20/REQUEST.txt`.

Se autoriza comprobar las implementaciones y ampliar los controles con los vectores existentes. No se cambian los resultados anteriores, ni se eligen criterios para sostener una conclusión. Nuevas salidas en `data/robustness_closure_v1/` y `reports/robustness_closure_v1/`; programas separados en `sos_closure/`. El manuscrito se actualizará **después** de congelar todos los resultados nuevos. Se conserva la entrega actual con sus huellas.

## Comprobaciones que deben terminar

1. Auditar medidas, IDs, normalización, controles aleatorios y selecciones originales.
2. Repetir centros de áreas y subáreas; comparar tamaños, asignaciones aleatorias, exclusión de áreas y elección de subáreas frente a artículos.
3. Repetir la comparación entre cambiar de modelo y quitar el resumen, incluidos vecinos 10/25/50 y recetas de los cuatro BERT.
4. Completar el cambio de referencia global en las 26 selecciones de forma; conservar direcciones y testigos concretos.
5. Completar las dos alternativas de dimensión en esas mismas selecciones.
6. Medir el efecto del filtro de calidad existente sobre vecinos, con artículos comparables y tamaños controlados.
7. Explicar la diferencia entre estabilidad del promedio y de cada comparación local.
8. Auditar cada afirmación, congelar resultados y actualizar artículo/suplemento en inglés y español.
9. Entregar `ROBUSTNESS_CLOSURE_REPORT.md`, `ROBUSTNESS_MANUSCRIPT_CHANGELOG.md`, datos de las comprobaciones y cuatro PDF revisados.

Los rangos entre selecciones describen este corpus; no son intervalos de confianza de toda la ciencia. Los pares de modelos tampoco son observaciones independientes. Los resultados adversos se incorporarán al texto principal cuando afecten a sus conclusiones. No se añaden modelos, extracción, envío ni publicación. La aprobación personal del manuscrito sigue pendiente.
