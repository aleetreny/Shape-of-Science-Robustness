# Protocolo de ejemplos concretos

17-09-2026. Seguimiento exploratorio solicitado después de conocer resultados generales. No es un registro previo a todo el estudio. Reutiliza vectores y vecinos ya calculados; no cambia la principal ni añade modelos. Configuración exacta: `config/case_atlas_v1.json`.

## Especialidades

Todas las 217 con 256 artículos aparecen en la tabla principal. Para evaluar persistencia se mantienen las mismas 183 que permiten 128/256/512, tres recetas y k10/25/50. En cada combinación se ordenan por acuerdo medio entre pares de modelos. Se conservan sus mejores/peores posiciones relativas. Se muestran seis que siguen relativamente altas incluso en su condición menos favorable y seis que siguen relativamente bajas incluso en su mejor condición. Los empates se resuelven por ID, no por una historia atractiva. CKA y alertas de selección se muestran como información separada: no fusionarlas en un índice nuevo sin significado.

## Artículos

Se usan las 10.850 consultas ya fijadas, con diez selecciones de 256 candidatos dentro de cada especialidad. Se ordena cada artículo por su peor coincidencia media de vecinos para los ejemplos altos, y por su mejor coincidencia para los bajos. Se muestran seis de cada extremo, máximo uno por especialidad y dos por área. Para ilustración se evitan las marcas de calidad/duplicados existentes; la tabla completa mantiene todas las consultas. Se conservan k10/k50, omisiones de modelos y comparación con búsqueda nativa. «Estable» describe una relación entre estos modelos y candidatos, no una propiedad intrínseca del artículo.

## Relaciones

Para medir una relación artículo→artículo, ambos deben poder ser elegidos en todas las repeticiones. Se usan las 50 consultas fijas de cada especialidad: cada una de sus 49 compañeras está siempre entre los 256 candidatos. Para cada relación se guarda cuántos de los diez modelos la incluyen entre sus vecinos y cuánto persiste al cambiar candidatos. Se conserva dirección; cercanía no equivale a citación ni a una relación causal. No contar la ausencia de un candidato como desacuerdo.

Para cada artículo ilustrado se muestran la relación más persistente y la más dependiente del modelo, con frecuencias por modelo, títulos e IDs. La elección es determinista. Se leerán los textos para describir lo que tienen en común, sin fingir una validación temática experta ni generalizar un ejemplo a todo un campo.

Las relaciones entre centros de especialidades se analizarán por separado, sobre las mismas muestras de 256, con rangos dentro de cada modelo y sensibilidad a receta/conjunto cuando esté disponible. No comparar directamente magnitudes de coseno de modelos diferentes ni atribuir al promedio entre centros el mismo significado que un vecindario documental.

Para la tabla ilustrativa de centros se guardan todas las parejas y se muestran ocho por extremo. Relaciones recurrentes: mayor número de modelos que las colocan mutuamente en sus cinco primeras posiciones; desempatar por ese mismo número usando todos los artículos, peor rango y finalmente IDs. Dependientes: mayor distancia entre mejor y peor rango mutuo; desempatar por IDs. El control con todos los artículos conserva las mismas 217 especialidades candidatas. No existe aún un control de receta para esos centros: se indica como límite. Los límites de diversidad de ejemplos de artículos se aplican al conjunto de doce, empezando por los seis altos.

## Conservación y revisión

Salidas en `data/prepaper_v1/case_atlas/`; entrega legible separada. Guardar configuración, fuentes, IDs, huellas y reglas de selección. Verificar cuentas de relaciones y vecinos con una reconstrucción independiente. Los ejemplos sirven para localizar dependencia, no para escoger un encoder «verdadero». Las limitaciones que permanezcan pasan al informe previo al manuscrito.
