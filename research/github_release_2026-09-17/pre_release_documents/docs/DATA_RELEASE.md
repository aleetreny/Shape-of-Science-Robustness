# Preparación del material para compartir

**Estado: preparado localmente, sin depósito público ni DOI.** Este documento organiza la entrega futura; no anuncia que ya esté disponible. El permiso actual no incluye publicar, subir datos ni elegir una licencia en nombre de autores o terceros.

## Paquete mínimo para repetir los resultados

| Material | Contenido necesario | Estado |
| --- | --- | --- |
| Código y decisiones | Programas, versiones, requisitos, configuraciones, protocolos, reglas de selección y copias de fuentes de cada fase. | Local; tablas/figuras y documentación listas. Falta versión pública identificable. |
| Identidad del corpus | IDs OpenAlex, año, Field/Subfield, base/complemento, marcas, huellas del texto y procedencia/fecha de las respuestas. | 500k locales; separar de los textos completos. |
| Selecciones | IDs de controles de 52k, tamaños, consultas/candidatos repetidos y cuotas temporales. | Guardados. El control de fragmento común y el de entradas son selecciones distintas. |
| Vectores | Revisiones/modelos/recetas, archivos con filas alineadas, controles y manifiestos. | Locales, decenas de GB. Son necesarios para repetir comparaciones sin recalcular inferencia. |
| Resultados y comprobaciones | Tablas, vecinos/centros donde hagan falta, catálogo de huellas y figuras con pies. | Entregas de las tres fases más atlas y auditoría nueva. |
| Texto de entrada | Título, abstract y fragmentos exactos. | Local. Antes de distribuirlos, verificar condiciones aplicables a los textos. No deducir permiso ilimitado de reutilización de todo abstract por obtenerlo mediante OpenAlex. |

El inventario legible principal es [DATA_CATALOG.md](../DATA_CATALOG.md). `research/prepaper_2026-09-17/release_inventory.csv` cuenta rutas/tamaños locales por componente, sin empaquetar ni subir nada.

## Qué hacer cuando se autorice el depósito

1. Elegir un archivo permanente con capacidad suficiente, versión y DOI, y comprobar qué archivos se pueden distribuir.
2. Congelar una versión pública del código. Añadir la licencia de nuestro código que decidan sus titulares; conservar avisos de dependencias. Hoy el repositorio no tiene una licencia general elegida.
3. Preparar paquetes de metadatos/selecciones y de vectores/derivados, con hashes, diccionario y comandos. Separar los textos cuya distribución no esté resuelta; explicar cualquier restricción real.
4. Probar la reconstrucción desde el material depositado, en un directorio limpio. Un archivo local y un enlace al API actual no sustituyen esa comprobación.
5. Escribir la declaración de disponibilidad con enlaces reales. Incluir limitaciones concretas si algo imprescindible no puede compartirse, conforme a las normas de la revista.

No incluir claves, `.env`, pesos descargados de terceros sin revisar condiciones, entornos locales, archivos de editor ni PDFs completos de literatura en una subida automática. Las fuentes de consulta se citan mediante enlaces; sus copias de lectura permanecen locales.
