# Ejemplo local de reproducción: comparaciones entre áreas

Este paquete recalcula ocho clasificaciones de las 325 parejas de áreas y comprueba qué parejas de modelos conservan respuestas opuestas después del centrado. Parte de las **13.520 medidas por modelo, área, selección y representación** guardadas al cerrar el estudio. No se limita a volver a dibujar una tabla final.

```sh
python3 -I -S reproduce.py --output reproduced.json
```

Usa Python 3.10 o posterior y solo su biblioteca estándar. No instala bibliotecas, accede a internet, utiliza modelos ni importa el repositorio. Se puede ejecutar desde una copia de esta carpeta en otro directorio.

`metrics.csv.gz` conserva las cifras de `data/robustness_closure_v1/morphology/metrics.parquet`, sin títulos ni resúmenes de artículos. `provenance.json` registra su origen y huellas. `expected.json` procede de las tablas finales congeladas; el programa obtiene de nuevo los resultados desde las medidas individuales y los compara con esas tablas. Reproduce los cortes 0 y 5 %, las clases unánime/opuesta/sin resolver y la conservación de los mismos modelos con sus mismas direcciones al corte 0.

**Límite:** es una demostración de una parte de la Figura 4. No calcula las medidas a partir de vectores, no genera embeddings y no reproduce todo el artículo. La futura entrega debe incluir los vectores, selecciones, programas y demás datos necesarios para esas etapas. Esta carpeta es preparación local; no tiene un DOI ni una licencia elegida por el autor y no se ha publicado.
