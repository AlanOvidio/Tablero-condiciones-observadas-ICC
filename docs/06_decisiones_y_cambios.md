# Decisiones y cambios

Bitácora del proyecto. Una entrada por cambio lógico (coincide con un commit).

## 2026-11-04 · Línea base y plan
- Se crea el repositorio Git. **Commit 1** = versión heredada sin modificaciones (`20260108 - Power BI Guatemala.pbip`).
- Se agregan `README.md`, `docs/01_plan_reformulacion.md` y esta bitácora.
- `.gitignore` excluye `cache.abf`, `localSettings.json` y los scripts R con credenciales (`otros_archivos/*.R`).
- Decisión: **arquitectura nueva** (modelo propio basado en `Tablero-semanal-ICC`), no reporte delgado sobre el modelo semanal.
- Decisión: la apariencia sigue a los scripts R (`script_figs_zonasclima_.R`, `script_nuevo.R`); agrupación dinámica por **estación, estrato altitudinal o región climática** para todas las variables.

## 2026-11-04 · Decisiones D1–D11 y esqueleto del modelo nuevo
- Decisiones registradas en el plan (D1–D11).
- `tools/generar_regiones.R` ya no filtra `redmet == 1` (todas las estaciones) y agrega la columna `redmet`.
- Nuevo proyecto `Condiciones_observadas.pbip` (generado una sola vez con `tools/construir_v2.py`): 15 tablas, 3 relaciones, 39 medidas en `_Medidas` (contexto, diario, mensual, histórico, anomalías, acumulados, periodos, textos). El reporte tiene una página vacía de validación.
- `tools/aplicar_regiones.py` copia `config/estaciones_region.csv` al bloque `<regiones>` de `Estaciones_met`.

## 2026-11-04 · Regiones de todas las estaciones
- `config/estaciones_region.csv` regenerado con todas las estaciones de la API (101); `tools/aplicar_regiones.py` lo copió a `Estaciones_met`. Las 61 estaciones del modelo tienen región (Pacífico 29, Bocacosta 18, Altiplano Central 5, Pacífico SV 6, Montañosa SV 3).
- **Error del tablero heredado:** la consulta "Chaparrastique" pedía `estacionid=4` (Bonanza), así que mostraba datos de Bonanza. En el modelo nuevo se agrega el ID 40 (Chaparrastique real) a `TablaEstaciones_met`: 61 estaciones.
- Corrección: en `Fact_Mensual_met` (tabla calculada con SUMMARIZE) las columnas agrupadas conservan su origen, por lo que `sourceColumn` debe ser `Fact_Diaria_met[estacionid]`, `Fact_Diaria_met[Anio]` y `Fact_Diaria_met[Mes]`. El nombre corto impedía crear la relación con `Estaciones_met` (error PFE_TM_RELATIONSHIP_END_COLUMN_INVALID al abrir).

## 2026-11-04 · Limpieza del repositorio
- Se elimina `tools/construir_v2.py` (generador de un solo uso del esqueleto; desde ahora el modelo se edita en Power BI Desktop / Tabular Editor).
- `.gitignore`: se ignoran `.Rproj.user/` y los índices espaciales `*.sbn`/`*.sbx`; se quita la regla de PDF heredada del semanal.
- README actualizado con la estructura actual.

## 2026-11-04 · Fases 3–4: medidas y páginas
- 74 medidas. Nuevas: años adicionales (hasta 4: `Anio_Comp_k`, `Valor_Comp_k`, `Acum_Comp_k`), `Grupo_Etiqueta` (nombre del grupo para Deneb), colores por variable, etiquetas de anomalía, `Color_Mapa` (5 clases relativas), umbrales de radiación (12 y 20 MJ/m² por defecto, editables), acumulados de Periodo A/B por día, medidas por año para ejes de pentada, títulos dinámicos.
- `Anio_Analisis` usa `ALLSELECTED ( Calendario )`: toma el año del segmentador aunque el visual tenga fechas en el eje.
- `Var_Sel`: sin selección toma la primera variable visible en la página (cada página filtra su grupo de variables).
- `Valor_Mensual` usa siempre el año de análisis.
- Se quitan `Valor_Mensual_Anio_Comp` y `Acum_Mensual_Anio_Comp` (reemplazadas por las de años adicionales).
- Tablas nuevas: `Umbral_Rad_Sub`, `Umbral_Rad_Opt`, `Dias_Periodo`.
- Reporte con 8 páginas: Precipitación y agua · Radiación · Temperatura, humedad y viento (mapa por clases, serie diaria y matriz de calor grupo × día) · Climatología mensual (Deneb + matriz de anomalías) · Acumulados (Deneb + acumulado diario) · Balance hídrico (Deneb + pentadas) · Comparación entre periodos · Notas metodológicas.
- Tema `TemaICC.json` con la paleta de los scripts R. Especificaciones Vega-Lite de Deneb guardadas en `deneb/` (respaldo y control de versiones).

## 2026-11-04 · v3: emulación del tablero heredado y gráficas tipo R
- Corrección: `Var_Nombre`, `Var_Unidad`, `Var_Regla`, `Color_*` y `Color_Mapa` evaluaban `[Var_Sel]` dentro de `FILTER` (transición de contexto por fila) y devolvían la variable equivocada (p. ej. "Velocidad del viento" con "W/m²").
- Variables reducidas a las del tablero heredado: precipitación, ETo, ETo media diaria (nueva columna `Fact_Mensual_met[ETo_Dia]`), balance, radiación, irradiancia, temperaturas máxima/media/mínima y sensación térmica. Se quitan viento, humedad y amplitud.
- Parámetro de campo `Agrupar_por`: los visuales ahora incluyen `fieldParameters` (antes mostraban el texto del parámetro).
- Mapas Azure con latitud/longitud explícitas (antes geocodificaba números y ubicaba estaciones en Europa).
- Tabla `Capas` = banderas de los scripts R (`mostrar_ribbons`, `mostrar_media`, `mostrar_actual`, `mostrar_anios`, anotaciones); por defecto como en R (media apagada).
- Gráficas Deneb reescritas para reproducir `script_figs_estrato_v3.R`: eje de meses numérico, bandas, año actual, años adicionales punteados con etiqueta al final, anomalías arriba/abajo con colores por variable, leyenda inferior y unidades en el eje.
- 22 páginas: emulación de las páginas heredadas + comparativos tipo R por variable, acumulados, balance mensual, notas y "Validación" (oculta).

## 2026-11-09 · v4: tabla mensual desde la API y una página por variable
- `Fact_Mensual_met` ya no es tabla calculada: se construye en Power Query desde el endpoint diario (día → mes por estación, como `mensual_por_estacion()` de R) con actualización incremental mensual (19 años, se refrescan los últimos 2 meses). `Mes_Completo` = el mes terminó antes de hoy (hora de Guatemala).
- Sin parámetro de campo: la selección de estaciones (todas por defecto, o filtradas por región/estrato, o elegidas en las fichas) se promedia desde el pool estación-mes. Se quitan `Agrupar_por`, `Base_Inicio/Fin`, `Periodo_A/B`, `Dias_Periodo`, `Umbral_Rad_*` y la página de comparación de periodos.
- Año de análisis en tabla propia (`Anio_Sel`, orden descendente) y periodo histórico como rango (`Anios_Base`); el histórico nunca incluye el año de análisis.
- Título dinámico: estación individual, estrato, región o delimitación; subtítulo con año, número de estaciones y años reales del histórico de la selección.
- `Capas`: año actual, media histórica, rangos, años adicionales y anomalías (las anomalías solo aparecen con el año actual).
- Medidas reescritas desde cero (79). Gráfica Deneb única por página con título, subtítulo, eje y leyenda dinámicos.
- Páginas: precipitación mensual, precipitación acumulada (con ETo y radiación), temperaturas, balance hídrico (mensual + pentadas con fechas), evapotranspiración, sensación térmica, radiación (MJ/m² o W/m²), notas y validación (oculta).
- Se eliminó `cultures/es-GT.tmdl` (metadatos lingüísticos con tablas borradas; Power BI lo regenera).
- Al cambiar `Fact_Mensual_met` de tabla calculada a consulta M hay que borrar la caché local (`.pbi/cache.abf`): Power BI no permite cambiar el tipo de partición sobre datos ya cargados. La caché se regenera al actualizar.

## 2026-11-09 · v5: se recuperan las páginas heredadas
- Corrección de `Missing_References`: en tablas calculadas el nombre de la columna debe coincidir con el de la expresión (`isNameInferred`); Power BI había renombrado `Anios_Comparacion[Año]` a `Anio` y lo mismo pasaría con `GENERATESERIES` (`Value`). Ahora todas usan `SELECTCOLUMNS ( …, "Año", … )`.
- Se recuperan las páginas que emulan el tablero heredado (comparativas por estación y por año, temperaturas, radiación por pentadas con niveles, precipitación diaria, mapas de precipitación, radiación y sensación térmica, balance por pentadas, comparación entre periodos), adaptadas al modelo sin parámetro de campo. El rediseño tipo R aplica solo a los comparativos históricos.
- Balance hídrico separado: "Comparativo histórico: balance hídrico" (mensual) y "Balance hídrico por pentadas" (con tabla de fechas).
- Tablas recuperadas: `Umbral_Rad_Sub`, `Umbral_Rad_Opt`, `Periodo_A`, `Periodo_B`, `Dias_Periodo`. 99 medidas, 19 páginas.

## 2026-11-09 · v6: ajustes de revisión
- Control de calidad diario en Power Query (`fxLimpiarDiario`, compartida por las tablas diaria y mensual): fuera de rango → nulo. Temperaturas −5–50 °C, lluvia 0–400 mm, ETo 0–15 mm, radiación ≤ ~40 MJ/m², sensación térmica −5–70 °C.
- `Fact_Diaria_met` solo con las variables usadas (se quitan humedad, viento y amplitud) y con sensación térmica media/mínima/máxima. `Fact_Mensual_met` agrega `IC_Media` e `IC_Min_Abs`.
- Sensación térmica con tres variables (media, máxima, mínima) y paleta naranja propia.
- "Año civil" → "Año calendario"; subtítulo "Año 2026 (calendario)" o "(hidrológico)"; el periodo histórico solo va en la leyenda.
- El segmentador de periodo histórico solo ofrece años anteriores al de análisis (`Base_Disponible`).
- Umbrales de radiación como controles deslizables de valor único (parámetros what-if) con el encabezado del color del nivel.
- Segmentadores de selección múltiple: varias opciones solo con Ctrl.
- Gráficas tipo R: cuadrícula horizontal restaurada (la regla del cero iba como primera capa y la anulaba); línea del cero roja, punteada y gruesa solo en balance; etiquetas de anomalía con halo blanco, separadas del punto y reubicadas para no salir del área.
- Respaldo del estado v5 en `_respaldo_v5/` (ignorado por Git).

## 2026-11-09 · Fechas y mapas
- `Calendario`: jerarquía "Jerarquía de fechas" (Año → Trimestre → Mes → Día) y columnas de texto `Fecha_Larga` ("5 noviembre, 2025") y `Fecha_Abrev` ("5-nov-2026"), ordenadas por `Fecha`. La columna `Fecha` no cambia. Con la fecha automática desactivada, la jerarquía debe declararse en la tabla de fechas.
- Mapas Azure: la estación no puede ir en *Ubicación* junto con latitud/longitud (`DataViewMappingError_LocationAndLatLongGroup`); se corrigió en Desktop dejando solo latitud y longitud.

## 2026-11-10 · Documentación
- Documentación al estilo del tablero semanal: 01 arquitectura, 02 diccionario (automático), 03 catálogo de medidas (automático), 04 guía de usuario, 05 operación, 06 decisiones y cambios (antes 02), 07 repositorio, 08 plan (antes 01), 09 inventario de visuales (automático).
- `tools/generar_docs_modelo.py` adaptado del tablero semanal (agrupa las medidas por carpeta).
