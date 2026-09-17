# Estado actual: revisión previa al manuscrito terminada

**17-09-2026.** Cierre experimental R01–R12 conservado; auditoría, atlas de casos, referencias y organización completados. No hay cálculos activos. El manuscrito no se ha empezado.

## Punto exacto para continuar

1. Leer [PREPAPER_REVIEW.md](PREPAPER_REVIEW.md): comprobaciones y errores de la fuente detectados.
2. Revisar [ROBUSTNESS_RESULTS.md](ROBUSTNESS_RESULTS.md), [CONCLUSION_CONTROLS.md](CONCLUSION_CONTROLS.md) y [CASE_ATLAS.md](CASE_ATLAS.md): resultados generales y ejemplos concretos.
3. Redactar solo cuando se solicite, siguiendo [PAPER_OUTLINE.md](PAPER_OUTLINE.md), los métodos de las tres fases y [references/RELATED_WORK.md](references/RELATED_WORK.md). Usar [references/references.bib](references/references.bib).
4. Antes de enviar, completar [QSS_CHECK.md](docs/QSS_CHECK.md) y el [depósito de datos/código](docs/DATA_RELEASE.md). El usuario ha autorizado commit y push de código/documentación/tablas/figuras a GitHub. El corpus y los vectores siguen locales; no hay depósito permanente, licencia general elegida ni envío a revista.

## Límites que deben acompañar las conclusiones

- Corpus de 500k: 400k base + 100k complemento; inglés, abstract disponible, 2000–2024 y clasificación OpenAlex. No representa toda la producción mundial.
- Tres entradas en 52k, con el piloto de 26k incluido; el control de fragmento común de 52k es otra selección. Mean principal para cuatro BERT; CLS/SEP como controles.
- Se conservan cinco alertas de entrada en 52k/100 selecciones, las 50 originales y las de Subfields. No son intervalos poblacionales ni tareas que se resuelvan cambiando umbrales.
- No hay caída universal de acuerdo al pasar a especialidades. Los candidatos condicionan la comparación: ambos ámbitos incluyen las 50 consultas del Subfield en sus 256 candidatos.
- Los casos muestran errores de OpenAlex y un aviso no detectado. Se mantuvieron con notas. La pequeña sensibilidad a 82 títulos genéricos no estima el error temático total ni limpia los candidatos.
- Atlas: 217 especialidades, 183 comparadas bajo 27 condiciones; 10.850 consultas con diez selecciones y 531.650 relaciones siempre elegibles. Los ejemplos son exploratorios. Centros de especialidades: 23.436 parejas, receta principal; sin control de receta adicional.
- Consenso no es calidad. CKA no es porcentaje de ciencia correcta; 45 pares no son independientes. Familias/Medicina no identifican causas; el cambio temporal no demuestra convergencia causal.
- La biblioteca tiene 45 entradas comprobadas. Ya existen trabajos cercanos sobre forma, vecinos, entrada, categorías y familias; defender aportación concreta, sin primacía absoluta.

## Dónde está cada entrega

| Material | Ubicación |
| --- | --- |
| Nueva revisión y atlas | `reports/prepaper_v1/`, `data/prepaper_v1/`, `research/prepaper_2026-09-17/` |
| Resultados ampliados, 50 tablas y siete figuras | `reports/robustness_v2/final/` |
| Auditoría de 15 componentes | `data/robustness_v2/final_audit/` |
| Comparación inicial sobre 500k | `reports/analysis_v1/final/` |
| Piloto histórico de 26k | `reports/checklist_v1/final/` |
| Catálogo e índice de documentos | `DATA_CATALOG.md`, `docs/INDEX.md` |

Usar `control_review_v2` y `structural_review_v3`; versiones anteriores y vistas provisionales se conservan como historial. Las fuentes científicas y sus salidas tienen huellas/copia. No editarlas y reanudar como si fueran la misma versión.

## Un comando para reconstruir solo la presentación del atlas

```sh
VECLIB_MAXIMUM_THREADS=4 .venv-analysis/bin/python -m sos_review.report
```

No ejecuta modelos ni vecinos. Después hay que revisar visualmente las figuras reconstruidas. Más opciones y requisitos en [REPRODUCING.md](docs/REPRODUCING.md).

Los datos grandes siguen locales y fuera de Git. No relanzar `start_embeddings.sh`, descargas ni ejecutores ya terminados. Las automatizaciones anteriores permanecen pausadas. Una ampliación futura debe responder a una afirmación concreta que aún no tenga apoyo suficiente.
