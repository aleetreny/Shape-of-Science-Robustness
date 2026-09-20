# Registro técnico del piloto de morfología

18-09-2026. Complemento exploratorio posterior a los resultados principales y al atlas. No altera las hipótesis, criterios o programas de los cierres anteriores. Lectura sencilla: [MORPHOLOGY_RESULTS.md](MORPHOLOGY_RESULTS.md).

## Diseño y procedencia

El usuario autoriza este piloto y las decisiones necesarias para realizarlo. Protocolo/configuración fijados antes de sus nuevos resultados reales: `MORPHOLOGY_PROTOCOL.md`, `config/morphology_pilot_v1.json`. Las pruebas de nueve nubes simuladas y quince referencias precedieron a los resultados reales. Revelaron fallos de interpretación de fragmentación que se conservaron; no se eligieron medidas en función de su separación entre modelos reales.

Principal: selección existente `data/robustness_v2/inputs/native_input.parquet`, 52.000 IDs, 26 Fields × cinco períodos × 400. Recetas y modelos vigentes, sin inferencia. `NativeData` verifica manifiestos, archivos y alineamiento con los 500k. Los controles de entradas y fragmento común comprueban archivos y textos/IDs mediante `Store.scan`; el fragmento común usa otra selección y se compara con sus propios originales.

Se preserva el diseño de cuotas iguales por Field/período. Dentro de cada celda se reutiliza la selección por identificador fijada en el estudio anterior; las nuevas selecciones usan permutaciones deterministas de IDs. No ponderación poblacional en este piloto. No es una muestra representativa del tamaño mundial de cada área. Son artículos elegibles en inglés con resumen y etiquetas de OpenAlex; los errores de fuente detectados antes siguen siendo límites materiales.

Hay 1.406 arrays de selección en `data/morphology_pilot_v1/selections.npz`, emparejados entre modelos. La muestra de 4.000 contiene los 2.000 principales más 400 artículos adicionales por período. Las cinco selecciones externas se extraen del **mismo corpus congelado de 500k**, no de nueva extracción ni de una población externa. «Externa» significa externa al conjunto fijo de 52k. Todos los grupos principales conservan su tamaño; el control de calidad repone por celda, y los controles de extremos/retirada aleatoria usan 950.

## Operacionalización

Se trabaja en float64, con cada vector normalizado a longitud uno. No se proyecta para medir. Los componentes especiales de la receta mean siguen incluidos según `POOLING.md`; no se redefine la representación. MiniLM tiene 384 coordenadas, los otros 768. PR es invariante al añadir coordenadas nulas: comparar números de direcciones activas no equivale a dividir por el número de coordenadas. Las diferencias de capacidad/entrenamiento permanecen confundidas entre estos diez modelos fijos.

**Apertura.** Mediana del ángulo entre todos los pares distintos; grados, no coseno mal llamado ángulo. A partir de la distancia de cuerda d se calcula 2 asin(d/2). Se conservan cuantiles 10/90 y ángulo mediano respecto a la dirección del centro. La media de distancia coseno y norma del centro son algebraicamente redundantes, se usan para verificación, no como evidencia independiente. No se llama isotropía ni diversidad semántica a esta propiedad.

**Direcciones.** Se resta el centro de la nube unitaria y se obtiene su covarianza muestral. PR = (tr C)² / tr(C²). Entropía efectiva = exp(−Σ p log p), p = autovalores de C / tr C. D80 es el número mínimo de autovalores ordenados que acumula 80%; PC1 es la mayor proporción. Roy/Vetterli se aplica aquí a la matriz C, no a los valores singulares de la matriz de documentos. No se estima dimensión intrínseca no lineal ni número de temas. PR, entropía y D80 ponderan de forma distinta el mismo espectro; su correlación no valida su significado externo.

**Conexión.** Vecinos exactos por distancia euclídea de vectores unitarios, equivalente en orden al coseno. Se excluye el propio punto. Empates exactos por orden global de ID. Unión de enlaces dirigidos: matriz A sin pesos. Laplaciano normalizado L = I − D^(−1/2) A D^(−1/2). Se toma su segundo autovalor; cero cuando el grafo está desconectado. k25 principal y k10/50 alternativos. Solver disperso con inicio determinista, tolerancia 1e−8 y residuo verificado <1e−6. No se convierte en número de grupos.

La alternativa ponderada conserva el soporte unión-k25 y afinidad exp(−d²/(σᵢσⱼ)), σᵢ = distancia al vecino 25. Es una aplicación de escala local, no el algoritmo completo de Zelnik-Manor/Perona. El grafo mutuo exige el enlace en ambas direcciones; se reportan tamaño del componente mayor y número de componentes, incluyendo aislados.

Enlace simple sobre la matriz completa produce la misma filtración de componentes que un árbol de expansión mínimo. Se registra el primer radio que une 50/90/95/99/100% de puntos en el mayor componente, dividido por distancia mediana entre pares; también cocientes de radios y de arista máxima/mediana. Los cocientes no son medidas universales de fragmentación. El Gini de ocurrencias como vecino k25 es diagnóstico de desigualdad, sin interpretación de importancia científica.

## Controles y número de conjuntos

| Bloque | Conjuntos de medidas |
| --- | ---: |
| Principal, veinte medias muestras, cinco selecciones de igual tamaño, 500/4.000 y mezcla global | 7.290 |
| Cinco períodos y diez medias muestras de cada extremo temporal | 6.500 |
| Entradas, recetas, fragmento común, calidad, extremos, centrado, gaussianas y MiniLM512 | 3.094 |
| **Total** | **16.884** |

Las veinte selecciones internas tienen 1.000 artículos/área (200/período); las cinco externas, 2.000. Se calculan todas las alternativas en la primera repetición y en los principales/controles; en las demás se conservan PR, apertura, conexión k25, componentes, radios y desigualdad. No afirmar veinte repeticiones de todo el espectro o de cada alternativa. Las medias muestras temporales son 200 artículos y solo en los períodos extremos, diez repeticiones cada uno.

Calidad: nueve marcas existentes, unión de idioma ambiguo/posible mezcla, resumen 50–79 o >2.000 palabras, DOI/texto duplicado, posible aviso/acceso y revisión de contenido. Se retienen los elegibles de la media muestra inicial y se reponen hasta 200 por período desde los 52k. No se excluyen manualmente los ejemplos desfavorables, no se incorporan todas las posibles etiquetas erróneas ni se estima su prevalencia.

Extremos: distancia euclídea al centro de los vectores unitarios; se retiran los diez más alejados de cada período de la media muestra. Comparador: diez retirados al azar del mismo período. Ambas salidas tienen 950. Es una sensibilidad, no una declaración de que esos puntos sean errores.

Centrado global: media de los 52k unitarios, equilibrados por Field/período; se resta a cada vector y se vuelve a normalizar. Cambia explícitamente la representación. La referencia global para cocientes de medidas usa exactamente 2.000 artículos, con 15/16 por cada una de las 130 celdas; se distingue de ese centro global.

Gaussianas: tres realizaciones por modelo/área, n1.000, con media/covarianza de la nube unitaria en expectativa antes de proyectar a la esfera. Se conservan diferencias realizadas de PR/apertura tras normalizar. No se asume coincidencia exacta de momentos ni distribución nula calibrada; sin p-valores. La mediana del error de PR es +0,10%, rango −10,47% a +19,78%; apertura −0,87%, rango −4,69% a +4,60%.

El control adicional de proporción de vecinos reutiliza k25/k50 al duplicar n. Se registró durante la ejecución, antes de inspeccionar las curvas completas, y se conserva como adición posterior al protocolo: `research/morphology_2026-09-18/INTERPRETATION_ADDENDUM.md`. No reemplaza el principal ni introduce inferencia nueva.

## Estabilidad, alternativas y límites de las inferencias

La amplitud central 90% de las repeticiones se divide por el valor principal n2.000; igual para el desplazamiento mediano. Cribas relativas fijadas: 5% apertura, 10% PR y 20% conexión. Denominador mínimo 1e−9 para no dividir por cero; los 260 valores principales de conexión son positivos. Son cribas de sensibilidad, no estándares de QSS, pruebas de significación ni intervalos poblacionales. Con cinco repeticiones los cuantiles son poco precisos: se conservan los valores individuales y no se borran alertas de otro diseño.

La estabilidad de rangos usa Spearman sobre las 26 áreas, por modelo y selección; el desacuerdo entre modelos usa los mismos artículos y las 45 parejas. No se tratan esas parejas como independientes. Los puntos de las figuras son resúmenes descriptivos de diez modelos fijos y áreas etiquetadas; no se presenta un modelo ganador, p-valores o efectos causales.

Se calculan correlaciones entre medidas por modelo y por Field. PR–entropía da mediana 0,956 al ordenar Fields, frente a 0,821 para PR–D80. Conexión k25–ponderada da 0,982, pero k25–componente mutuo solo 0,358 y k25–cociente de radios 0,441. La orientación de alternativas que significan mayor separación se invierte al correlacionarlas con conexión. Los resultados negativos y la saturación se conservan.

Descomposición descriptiva equilibrada de los 260 valores: efectos medios de modelo, área y residuo/interacción, sin prueba de independencia. En apertura bruta, 98,94% de la suma de cuadrados corresponde al efecto medio del modelo; al dividir por su mezcla global baja a 15,64%. **No es «98,94% de la forma de la ciencia» ni un efecto causal.** Para PR bruto: 72,64% modelo, 14,71% área, 12,65% interacción. Se incluye log(PR) y omisión de MiniLM. Su función es identificar escalas globales, no explicar entrenamiento/arquitectura.

Relación con CKA: para cada Field se correlacionan diferencias absolutas de la propiedad entre encoders con 1−CKA de los mismos 2.000 artículos/recetas. Medianas descriptivas de correlación entre Fields: apertura 0,271; PR 0,173; conexión 0,066. Estos rasgos **no son una descomposición causal o exhaustiva de CKA**. Añaden descripciones distintas. Sin pruebas sobre las 45 parejas como si fueran independientes.

Tiempo: contraste de extremos dentro de modelo/área y acuerdo del signo en diez selecciones reducidas. El tamaño igual controla una parte de la comparación, no cambios de composición, longitud de texto/cobertura o contenido. Las conclusiones históricas nuevas necesitarían esos controles específicos; los resultados no se promocionan a tendencia poblacional o causal.

Los casos de Odontología/Energía se eligieron después de los resultados por menor peor puesto entre modelos en las propiedades principales; el contraste Artes/Medicina es ilustrativo posterior. Se comprueban alternativas/recetas y se muestran fallos (D80, CLS/SEP), sin convertir esa selección en evidencia de frecuencia general.

## Auditoría, archivos y reproducción

- `data/morphology_pilot_v1/manifest.json`: fuentes, configuración, entorno y padres; copias en `source_snapshot/`. `execution_manifest.json` añade el coordinador de tres procesos. Funciones científicas congeladas intactas durante la ejecución.
- `parts/`: treinta bloques con valores y huellas. `metrics.parquet`: todos los conjuntos. `selection_audit.json`: cruces de IDs y hashes de las 1.406 selecciones. `audit.json`: completitud y rangos.
- `synthetic/`: nueve nubes, quince referencias, tamaño/dimensión y auditoría. Rotación/escala verificadas; contraejemplos preservados.
- `independent_audit.json`: seis comprobaciones reales n128 de ángulos/SVD/matriz espectral densa/MST; tres n2.000 contra cifras guardadas; errores <1e−8, coordenadas nulas y entradas degeneradas. Fuentes/padres sin cambios.
- `reports/morphology_pilot_v1/`: tablas completas derivadas, cinco figuras en PNG/PDF/SVG, resumen y catálogo con hashes. `sos_morphology/report.py` separado del cálculo científico.
- `research/morphology_2026-09-18/`: revisión dirigida, registros de nueve referencias nuevas, cinco advertencias bibliográficas conservadas, auditoría de cierre y copias documentales del commit anterior. Biblioteca canónica: 54 entradas.

Reconstruir tablas y figuras, usando las salidas locales completas:

```bash
OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 OMP_NUM_THREADS=1 \
  .venv-analysis/bin/python -m sos_morphology.report
```

Reanudar solo si falta un bloque del piloto, sin cambiar fuentes/configuración:

```bash
OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 OMP_NUM_THREADS=1 \
  .venv-analysis/bin/python -m sos_morphology.parallel_run --workers 3
```

**El cálculo ya terminó; no hace falta lanzarlo de nuevo.** El coordinador verifica bloques completos y usa un bloqueo único. El bloque secuencial inicial de SPECTER se conservó al cambiar la organización de ejecución; no se cambiaron decisiones científicas. Nuevas fórmulas/configuraciones requieren otra versión/salida. El entorno existente quedó intacto y los datos/vectores siguen fuera de Git. La reproducción completa desde un repositorio público aún requiere el depósito autorizado de los materiales esenciales, pendiente en el proyecto general.

Verificar la entrega local sin recalcular los experimentos:

```bash
.venv-analysis/bin/python research/morphology_2026-09-18/closure_audit.py
```

Esta auditoría comprueba archivos, cifras, fuentes, enlaces y el registro de inspección visual. No sustituye una validación temática externa.
