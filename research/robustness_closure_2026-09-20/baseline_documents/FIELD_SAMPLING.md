# Reparto decidido para la primera preparación

**Decisión tomada por delegación explícita del usuario el 14-09-2026.**

Prepararemos **500.000 trabajos válidos y con IDs distintos**:

- **400.000 elegidos al azar** entre los trabajos que cumplen los filtros, para representar su reparto real.
- **100.000 adicionales** para reforzar las combinaciones de área y período con menos papers. El reparto lo calcula una regla automática: primero completa las combinaciones menos numerosas, sin recortar las grandes.

Habrá **26 Fields y cinco períodos de cinco años**, desde 2000–2004 hasta 2020–2024. Dentro de cada período se conserva la selección aleatoria de años; no se imponen 200 papers por año.

Con los recuentos previos a limpiar, se proyectan unos 76.600 para Medicina, 65.700 para Ingeniería, 32.500 para Informática y 11.000 para Veterinaria. Los números definitivos por área se obtendrán de la base limpia. El objetivo total sí es 500.000.

**La base de 400.000 se usa para la comparación general.** Los 500.000 juntos refuerzan deliberadamente las áreas pequeñas: no se deben presentar sin corrección como si conservaran las proporciones reales. Para cada área y período, se utilizan también sus trabajos de refuerzo.

Los filtros, el procedimiento, los costes medidos y los controles están en [CORPUS_PROTOCOL.md](CORPUS_PROTOCOL.md). Las decisiones y dudas pendientes están en [DECISIONS.md](DECISIONS.md). El corpus completo todavía no se ha extraído.

La propuesta original de 5.000 por Field y la posterior sin tamaño fijado quedan sustituidas. Se conservan como historial:

- [Primera propuesta](research/FIELD_SAMPLING_initial_proposal.md).
- [Revisión previa a la delegación](research/FIELD_SAMPLING_review_proposal.md).

Los [recuentos locales e históricos](FIELD_COUNTS.csv) y los [recuentos actuales de OpenAlex](OPENALEX_COUNTS.md) siguen disponibles. El filtro ahora decidido añade revisiones y congresos y excluye preprints; sus nuevos recuentos, **67.202.824 candidatos antes de limpiar**, están en la [evidencia de esta decisión](research/feasibility_2026-09-14/proposed_population_fields.json).
