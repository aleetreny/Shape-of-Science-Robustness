# Comprobación adicional al interpretar tamaño y conexiones

Añadida durante la ejecución, antes de inspeccionar las curvas de tamaño completas. No forma parte del protocolo inicial congelado; no cambia medidas ni muestras. Se deriva de los valores k=25/50 ya previstos.

Mantener k=25 mientras se duplica n reduce a la mitad la proporción de posibles vecinos que se conectan. Por ello una variación del grafo con n no puede leerse exclusivamente como error de estimación. Se compararán también 500/k25 con 1.000/k50, 1.000/k25 con 2.000/k50 y 2.000/k25 con 4.000/k50. Es una proporción aproximadamente igual (el propio punto está excluido del denominador). Se mostrarán ambas versiones para las diez cámaras y las 26 áreas.

No se elige la versión que parezca más estable ni se reemplaza el principal k25. Los grupos del análisis principal ya tienen el mismo n. La comprobación sirve para explicar qué parte de la sensibilidad corresponde a la definición del grafo. No garantiza una escala temática común entre encoders. Evidencia: `reports/morphology_pilot_v1/connectivity_fixed_fraction.csv`.
