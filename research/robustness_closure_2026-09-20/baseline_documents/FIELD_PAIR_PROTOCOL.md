# Resumen final de las 325 parejas de áreas

18-09-2026. El usuario acepta hacer este último resumen con resultados existentes antes de organizar el manuscrito. Protocolo fijado antes de calcular los nuevos recuentos. Es una ampliación exploratoria posterior al piloto de morfología; ya conocemos resultados generales y el caso Artes/Medicina. No es un preregistro ciego ni una nueva muestra poblacional.

## Pregunta y universo completo

¿Cuántas comparaciones entre disciplinas mantienen una dirección en los diez modelos y cuántas contienen direcciones opuestas que resisten cambiar los artículos?

Se incluyen todas las 325 parejas no ordenadas de los 26 Fields, sin escoger por el resultado. Dos propiedades principales ya fijadas: apertura angular mediana (`angle_p50`) y dimensión efectiva lineal (`pr`). Apertura no significa diversidad temática; PR no cuenta temas. La conexión no se incorpora como fragmentación.

Se leen exclusivamente `data/morphology_pilot_v1/metrics.parquet` y los registros/tablillas de procedencia del piloto. No se leen de nuevo vectores para calcular medidas, no se ejecutan modelos ni se descarga nada. Las fuentes originales y el cierre anterior se conservan; derivados nuevos en `data/field_pair_summary_v1/` y `reports/field_pair_summary_v1/`.

## Dirección, magnitud y repetición

Para una pareja A/B ordenada por identificador, diferencia positiva significa que **B tiene mayor valor que A**. Se conserva la diferencia en unidades originales y la diferencia relativa simétrica `2*(B-A)/(A+B)`. Las dos propiedades son positivas. Esta última permite describir tamaños relativos sin favorecer un encoder por su escala absoluta; no vuelve equivalentes las dos propiedades ni fija importancia científica.

Principal: mismos 2.000 artículos/área por modelo, con recetas vigentes. Cada comparación se repite emparejando el mismo número de repetición de A/B en las veinte medias muestras de 1.000 y las cinco selecciones de 2.000 del corpus congelado. Se usan los 26 valores (principal + 20 + 5), no se combinan todas las permutaciones de repeticiones. Los modelos comparten exactamente las selecciones. «Externa» se refiere al conjunto fijo de 52k, no a otra población ni a independencia.

Una dirección de un modelo es **persistente en estas comprobaciones** si todos los valores mantienen el mismo signo. Si el recorrido toca o cruza cero, se deja sin dirección resuelta. Tolerancia numérica de 1e−10 en diferencia relativa, muy inferior a las escalas científicas. Se conservan el mínimo, máximo, cuantiles, frecuencia de signos y magnitud. Es una regla descriptiva conservadora, no una prueba de significación ni intervalo de confianza; depende del número/diseño de repeticiones.

Clases exhaustivas, disjuntas, por pareja y propiedad:

1. **Acuerdo de todos:** los diez mantienen la misma dirección.
2. **Contradicción persistente:** al menos uno mantiene A>B y otro mantiene B>A. Los demás pueden quedar sin resolver; no se exige que los diez estén enfrentados.
3. **Sin conclusión común clara:** todos los casos restantes, incluidos acuerdos parciales. No se equipara a empate, ausencia de efecto o equivalencia.

Una diferencia minúscula puede ser persistente. Por eso se repite el resumen exigiendo que todas las diferencias relativas superen, en valor absoluto, **0%, 1%, 5% y 10%**. Cero es la pregunta de dirección principal; los demás son sensibilidades explícitas, no umbrales universales de relevancia ni elegidos por el recuento. Al subir el umbral, los casos pasan a no resueltos; no se borran del denominador 325. Se conservan magnitudes continuas.

También se muestran reglas con solo principal, principal + medias muestras, y principal + cinco selecciones de igual tamaño. Esto distingue tamaño de grupo/número de repeticiones. No se usa el diseño que produzca más contradicciones como resultado principal.

## Alternativas y controles que ya existen

- Apertura: cuantiles 10/90 de ángulos y ángulo mediano al centro. Las tablas efectivamente conservan estas tres alternativas en todas las veinte medias muestras y cinco selecciones. Se verifica cobertura antes de resumir.
- PR: rango efectivo por entropía y D80. Solo tienen cobertura completa en principal, media muestra 0 y selección adicional 0. Se comprueba coherencia con esas alternativas **sin atribuirles 25 repeticiones inexistentes**. D80 admite empates exactos. Las tres medidas derivan del mismo espectro, no son validación temática independiente.
- La lectura conjunta exige que **el mismo modelo** mantenga su dirección con la medida principal y todas sus alternativas disponibles. Una contradicción conjunta necesita dos modelos con direcciones contrarias cada uno bajo todo ese conjunto; no se sustituyen por testigos distintos para cada medida. Se presenta como una criba adicional, separada del resultado principal y sin exigir igual tamaño relativo entre medidas distintas.
- Controles puntuales emparejados: título/resumen, CLS/SEP solo en los cuatro BERT, texto común frente a sus propios textos nativos, centrado global, marcas de calidad, retirada de extremos frente a retirada aleatoria, MiniLM512 y tamaños 500/4.000. Se calculan las direcciones en las mismas 325 parejas. Son controles sin repetición propia; no heredan estabilidad de muestreo por estar disponibles.
- Para cada control se distingue cambio de dirección dentro del mismo modelo de cambios de la clase agregada. Si se examina si una contradicción persiste, deben seguir existiendo **los mismos dos modelos testigo** con sus signos anteriores; no basta que la pareja permanezca contradictoria por otros modelos.
- Panel principal de diez modelos fijos; sensibilidad con los seis entrenados para similitud de documentos/frases (SPECTER, SPECTER2, SciNCL, MPNet, MiniLM, SimCSE) y dejando fuera cada modelo por turno. Los cuatro BERT de palabras siguen en el principal. Menos modelos ofrecen menos oportunidades de contradicción: no atribuir causalmente al entrenamiento la diferencia de proporciones. Los modelos ni las 325 parejas son independientes.
- No se vuelve a analizar el tiempo: ya tiene informe propio y no es necesario para responder a este resumen.

## Verificación, presentación y límite de parada

Pruebas de clasificación con casos conocidos: acuerdo, oposición, igualdad, cambio de signo, diferencia pequeña, permutación de modelos y reversión de A/B. Comprobación independiente de los recuentos directamente desde los números guardados. Verificar 325 parejas únicas por propiedad, denominadores, ausencia de datos faltantes, correspondencia de selecciones y conservación de fuentes/cierres.

Presentar tabla de tres clases, sensibilidad al tamaño mínimo de diferencia, cuadro de las 325 parejas, resultados por modelo y controles. Como ejemplos mantener Artes/Medicina y elegir cualquier caso adicional mediante regla explícita de cobertura/magnitud, mostrando su condición exploratoria. No seleccionar solo los ejemplos favorables ni sugerir que todos los modelos pesan como observaciones independientes.

El cierre es este resumen, sus controles ya disponibles y una propuesta de cómo integrarlo con el resto del trabajo. No ampliar modelos, métricas, inferencia, corpus o fragmentación; no redactar ni publicar automáticamente. La aceptación editorial, la verdad temática y la representatividad mundial no se deducen de estos recuentos.
