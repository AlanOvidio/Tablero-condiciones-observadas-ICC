# Operación y mantenimiento

## Requisitos

- Power BI Desktop (octubre 2026 o posterior) con formato PBIP/TMDL.
- Visual **Deneb** (gratuito, AppSource) para los comparativos históricos.
- Licencia Power BI **Pro** para publicar.
- Acceso a `https://redmet.icc.org.gt` y al SharePoint de cuencas.
- Python 3.8+ (documentación automática y regiones) y R con `sf` (solo para regenerar regiones).

## Parámetros de Power Query

| Parámetro | Valor recomendado | Notas |
|---|---|---|
| `RangeStart` | `01-ene-2008 00:00` | Carga todo el histórico en Desktop (necesario para los comparativos). |
| `RangeEnd` | Fecha futura (p. ej. `01-ene-2030`) | Exclusivo. Con una fecha futura se carga hasta el último dato. |
| `InicioAnioHidrologico` | `01-nov` | Solo se usa el mes. |

En el **servicio** estos parámetros no se usan: cada tabla fija su rango con la actualización incremental.

## Actualizar en Desktop

1. **Fetch origin / Pull** en GitHub Desktop si se trabaja en más de un equipo.
2. Abrir `Condiciones_observadas.pbip` → **Inicio → Actualizar**.
3. Revisar la página oculta **Validación** (estaciones con datos, meses válidos, fechas).

## Publicar

1. **Publicar** al área de trabajo.
2. La primera vez, configurar credenciales (API anónima/básica según el servicio; SharePoint con cuenta de la organización) y hacer una **actualización completa**: crea las particiones de 19 años.
3. Programar la actualización diaria: solo se vuelven a descargar los últimos 7 días (diaria) y 2 meses (mensual).
4. Si se cambia la estructura de una tabla con actualización incremental, el servicio requiere una actualización completa.

## Tareas frecuentes

| Tarea | Cómo |
|---|---|
| Agregar o quitar una estación | Editar la lista en `TablaEstaciones_met`. Si es nueva: correr `tools/generar_regiones.R` y `python tools/aplicar_regiones.py` (Power BI cerrado) y agregar su cuenca en el Excel de SharePoint (`Hoja2`). |
| Cambiar límites del control de calidad | Editar `Limites` en `fxLimpiarDiario` (Power Query → función). |
| Cambiar colores, unidades o umbrales de anomalía | Editar la tabla calculada `Variables`. |
| Editar una gráfica tipo R | Visual → … → **Editar** (Deneb). Copias de las especificaciones en `deneb/`. |
| Regenerar la documentación | `python tools/generar_docs_modelo.py` (genera 02, 03 y 09). |

## Solución de problemas

| Síntoma | Causa y solución |
|---|---|
| Al abrir: "No se permite cambiar el tipo de partición…" | La caché local tiene la tabla con otro tipo de partición. Cerrar Power BI, borrar `.SemanticModel/.pbi/cache.abf` y actualizar. |
| `Missing_References` en visuales | Un visual usa un campo que no existe. En tablas calculadas el nombre de la columna debe coincidir con el de la expresión (si no, Power BI la renombra). |
| Mapa: `LocationAndLatLongGroup` | El mapa tiene un campo en *Ubicación* junto con latitud y longitud; dejar solo latitud y longitud. |
| Estación con "Sin cuenca" | No está (o está escrita distinto) en el Excel de SharePoint `Hoja2`. |
| Estación con "Sin región" | Fuera del shapefile de regiones; revisar coordenadas o el CSV. |
| Mes en curso no aparece | Comportamiento esperado: solo meses terminados con ≥ 80 % de días. |
| Gráfica Deneb vacía | Revisar que los nombres de los campos del visual no se hayan cambiado; si se rompió, pegar la especificación de `deneb/`. |
