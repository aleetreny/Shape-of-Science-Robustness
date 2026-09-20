# Métodos del resumen final de parejas de Fields

18-09-2026. Derivado exploratorio de las medidas del piloto de morfología, autorizado tras conocer el ejemplo Artes/Medicina y los resultados generales. Protocolo y configuración escritos antes de los nuevos recuentos: [FIELD_PAIR_PROTOCOL.md](FIELD_PAIR_PROTOCOL.md), `config/field_pairs_v1.json`. No se interpreta como preregistro de todo el estudio.

## Datos y correspondencia

Entrada única de valores: `data/morphology_pilot_v1/metrics.parquet`, verificada con el manifiesto/auditoría anterior. Los nombres y las 26 claves de áreas se recuperan de la tabla principal auditada. Código nuevo `sos_pair_summary/`; no importa ejecutores anteriores ni carga embeddings para medirlos. Antes de anotar esta fase se conservaron los 18 documentos sellados del cierre anterior con sus huellas en `research/field_pair_summary_2026-09-18/baseline_documents/`.

Se enumeran exactamente las combinaciones no ordenadas de 26 Fields, 325, con A<B por ID OpenAlex. Dos medidas: ángulo mediano entre pares de artículos (`angle_p50`) y participation ratio de la covarianza centrada de vectores unitarios (`pr`), tal como se calcularon en el piloto. No se cambia su definición, muestra, receta o normalización. Nombres de la figura en español son abreviaciones de presentación; las tablas mantienen nombres originales e IDs.

Cada modelo y pareja dispone de 26 condiciones guardadas: principal de 2.000 artículos por área, veinte medias muestras de 1.000 y cinco selecciones de 2.000 del mismo corpus de 500k. Se empareja la repetición r de A con r de B. Los hashes de selección por área/repetición deben coincidir en los diez modelos. Las selecciones se solapan y las adicionales no provienen de una población nueva. Diseño principal equilibrado por área y por período; no ponderación por tamaño mundial de disciplinas.

## Regla y magnitud

Se guarda `B-A` en unidades originales y `d=2(B-A)/(A+B)`. Un valor positivo indica B>A. La diferencia simétrica es invariante a multiplicar ambos valores por una escala positiva; no elimina efectos del origen, de recetas o del encoder. Los valores de las propiedades son finitos y positivos; se rechazan entradas no válidas.

Dirección persistente para modelo m, pareja p, mínimo t: `min(d)>t+1e-10` da +1; `max(d)<-t-1e-10` da −1; el resto, 0. Mínimo/máximo sobre las 26 condiciones. No es un intervalo de confianza ni se asigna significación. Los cuantiles 5/95, las frecuencias de signos y las magnitudes quedan en la tabla, sin sustituir el rango completo por un intervalo favorable.

Por pareja: todos +1 o todos −1 = `unanimous`; al menos un +1 y un −1 = `contradiction`; resto = `unresolved`. Estas tres clases son disjuntas y exhaustivas. La tercera permite coincidencia parcial; no equivale a igualdad. Una contradicción puede existir con modelos no resueltos; no implica diez conclusiones diferentes.

Principal t=0, pregunta sobre dirección. Sensibilidades t=0,01/0,05/0,10, escritas antes de contar. Son cortes operativos sin justificación de relevancia universal y no se elige uno como óptimo. Se conservan 325 en todos los denominadores. Un mayor corte solo puede retirar direcciones, nunca invertirlas. El porcentaje es sobre la media de las dos propiedades, no un porcentaje del ángulo completo, del corpus, de errores o de ciencia conservada.

Comparadores: principal solo, principal + veinte medias muestras, principal + cinco selecciones de igual tamaño. Al reducir condiciones disminuye la posibilidad de detectar un cambio; no se atribuye su diferencia solo al tamaño. Esas reglas no reemplazan retrospectivamente la principal.

## Alternativas, panel y controles

Las alternativas angulares (cuantiles 10/90, mediana respecto al centro) tienen 26 condiciones. Las espectrales (rango de entropía y D80) tienen tres: principal, media muestra 0 y selección adicional 0. La disponibilidad se verifica sobre valores guardados; D80 es discreto y admite empates.

Para el resumen conjunto, la dirección persistente principal de cada modelo solo se conserva si todas sus alternativas disponibles tienen esa misma dirección. Dos modelos opuestos deben superar por separado ese conjunto: no se eligen testigos distintos por medida. Para el control t>0, el mínimo se exige en la medida principal; las alternativas deben conservar signo, no superar el mismo porcentaje. Las alternativas no son validaciones temáticas independientes.

Panel principal fijo de diez, sensibilidad de seis (SPECTER, SPECTER2, SciNCL, MPNet, MiniLM, SimCSE) y diez omisiones individuales. Misma regla y mismo denominador de áreas. El panel pequeño contiene menos oportunidades de oposición; no prueba un efecto causal del entrenamiento. Los 45 pares de modelos y 325 pares de áreas se solapan. No se les aplica un test como observaciones independientes ni se estima una tasa mundial de contradicciones.

Once controles puntuales: título, resumen, CLS/SEP, fragmento común, centrado global, marcas de calidad, extremos, MiniLM512 y tamaños 500/4.000. La receta cambia solo en los cuatro BERT de palabras; MiniLM512 solo en MiniLM. Los demás modelos conservan el panel de referencia correspondiente. Comparaciones de entrada/receta/centrado usan media muestra 0; común usa su propio `common_native`; extremos usa retirada aleatoria del mismo tamaño; MiniLM512/tamaños usan principal. Calidad/extremos/tamaño cambian IDs según su diseño; las demás comparaciones comprueban IDs idénticos. Los controles diferentes de tamaño deben mantener el mismo n que su referencia.

Se distinguen: reversión de dirección dentro de cada modelo afectado; cambio de clase del panel; presencia de una contradicción original en la referencia emparejada; conservación de **los mismos dos modelos con sus signos originales en referencia y variante**. El código intersecta identidades de testigos antes de contar, evitando sustituir un desacuerdo por otro. Las comprobaciones puntuales no certifican estabilidad bajo 25 repeticiones propias y no se agregan como réplicas.

## Cifras y verificaciones

Resumen principal: 42/262/21 para apertura y 54/221/50 para PR (unanimidad/oposición/no resuelto). A 5%: 10/96/219 y 36/177/112. Alternativas conjuntas: 28/225/72 y 8/196/121. Estos conteos son sobre 325, no sobre 6.500 decisiones modelo–pareja–propiedad.

Once pruebas de reglas con casos conocidos, incluyendo cambio de signo aislado, empate, escala, campos invertidos, modelos permutados y testigos sustituidos. Auditoría independiente sin importar la función de clasificación: usa `B/A > (2+t)/(2-t)` para confirmar signo y tamaño de diferencia. Comprueba 10.400 filas de sensibilidad, 6.500 decisiones individuales, 7.150 controles de parejas al corte principal, 96 resúmenes de panel y 442.000 diferencias guardadas. Verificación exacta de diferencias originales, fuentes/copiados y cierre anterior. Las figuras se inspeccionan después de exportar; el código de presentación se mantiene separado.

## Archivos y reproducción

- `data/field_pair_summary_v1/manifest.json`: fuentes/configuración/protocolo/padres, con copias en `source_snapshot/`.
- `contrasts.npz`, `contrast_index.json`: 442.000 diferencias guardadas, ejes pareja/modelo/condición y cobertura de las siete medidas.
- `audit.json`, `independent_audit.json`: completitud y contraste independiente.
- `reports/field_pair_summary_v1/`: doce tablas CSV, dos figuras PNG/PDF/SVG, resumen y catálogo de huellas.
- `research/field_pair_summary_2026-09-18/`: protocolo de continuidad, copias previas, pruebas, revisión visual y cierre.

El resumen ya está terminado. Para verificar sin recalcular morfología:

```bash
.venv-analysis/bin/python -m sos_pair_summary.audit
```

Reconstruir solo figuras:

```bash
.venv-analysis/bin/python -m sos_pair_summary.report
```

El ejecutor del resumen es `.venv-analysis/bin/python -m sos_pair_summary.analyze`; verifica sus fuentes y omite la ejecución si ya terminó. Nuevos criterios científicos necesitan otra versión. La repetición de pruebas de reglas se puede solicitar con `-m sos_pair_summary.tests`. La auditoría de entrega está en `research/field_pair_summary_2026-09-18/closure_audit.py`; no repetir ningún extractor o cálculo de embeddings.

Las diferencias se reconstruyen desde medidas locales guardadas; la reproducción integral pública sigue requiriendo el depósito autorizado del material esencial. Este cierre no distribuye datos, elige licencia ni redacta el manuscrito. Las alertas de fases anteriores y los errores de etiquetas de OpenAlex permanecen; integridad numérica no equivale a verdad temática.
