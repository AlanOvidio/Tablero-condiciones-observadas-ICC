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

## 2026-11-10 · Versión v1.0
- Fusión de la rama `v2` en `main` (Pull Request #1) y etiqueta `v1.0`.
- Se conserva temporalmente la versión heredada como referencia.
- Pendientes (en ese momento): completar cuencas; decidir si se unen las comparativas por estación, por año y de temperaturas; retirar la versión heredada.

## 2026-11-11 · Ajustes posteriores a v1.0
- Validación contra los scripts R realizada por el responsable: cifras correctas. El tablero está publicado en el servicio.
- Los scripts R de figuras son solo la base de referencia y no forman parte del repositorio; se retiraron de la documentación las menciones a versionarlos.
- Segmentadores desplegables (país, estrato, región, cuenca, estación, años de comparación, capas): selección múltiple sin Ctrl. Los segmentadores de mosaico con nombres de estación mantienen la selección con Ctrl; los de selección única (variable, año, modo) no cambian.
- Cuencas: se mantienen como están; a futuro se prevé una columna en `config/estaciones_region.csv` cuando exista la capa de cuencas.
- Nueva pestaña **Comparativas mensuales** (las páginas originales se conservan hasta decidir cuáles retirar): selector de variable, vista Mensual / Acumulado mensual (tabla `Vista_Comp`; el acumulado solo aplica a variables acumulativas), botones con marcadores para alternar «Comparar años» y «Comparar estaciones», y matriz de valores por mes. Medidas nuevas: `Comp_Valor`, `Comp_Valor_Anio`, `Comp_Acum` y títulos `Titulo_Comp*`.
- Estaciones: se mantiene la lista fija de 61 estaciones del tablero heredado (todas de Guatemala y El Salvador). Las RLS Acarigua, Tres Ríos, El Rosario y Motagua no se incluyen.
- Comparativas mensuales: cada botón tiene una versión activa (azul) y otra inactiva (gris) que los marcadores alternan, para que se vea cuál modo está seleccionado. Mini mapa de las estaciones seleccionadas junto a la tabla de valores.

## 2026-11-12 · Interacción y anomalías en las gráficas tipo R
- Gráficas Deneb: cursor como en los visuales nativos (línea vertical en el mes más cercano y tooltip con año actual, media, rango normal, mínimo–máximo, anomalía y años adicionales). Especificaciones en `deneb/` actualizadas (nuevo `balance.json`).
- Etiquetas de anomalía sin decimales (las variables con decimales, como temperaturas y ETo diaria, conservan uno, y también las anomalías menores que 1 en valor absoluto); porcentaje sin decimales y calculado sobre el valor absoluto de la media.
- Balance hídrico: la anomalía muestra también el porcentaje; línea del cero en rojo oscuro (#8B0000); paleta pizarra (#1B2A49 / #6B7A99 / #C9CED8) para distinguirla de la lluvia.
- Precipitación diaria: se aclara en el subtítulo que la línea es el acumulado desde el 1 de enero, promedio de las estaciones seleccionadas.
- Corrección del cursor: el tooltip se arma con campos calculados en la capa (con `nearest` el *datum* de un tooltip de marca es el del voronoi y salía `undefined`). Muestra mes, año actual, media, rango normal y rango histórico (separador «a» para no confundir con el signo negativo); la anomalía queda solo en la anotación y los años adicionales no se incluyen.
- Capas: «Rangos históricos» se separa en «Rango histórico (mín–máx)» y «Rango normal (P33–P66)». `Mostrar_Rangos` devuelve 1 (histórico), 2 (normal) o 3 (ambos); la leyenda solo muestra las capas visibles.
- Balance hídrico por pentadas: título dinámico (`Titulo_Pentada`), subtítulo con año, delimitación y número de estaciones (`Subtitulo_Seleccion`) y eje Y abreviado («P y ETo (mm)»).
- Delimitación por defecto: «Red meteorológica ICC (Guatemala y El Salvador)» en lugar de «Red ICC».

## 2026-11-12 · Segmentadores de fecha en la versión web
- En «Publicar en la web» el informe se reduce y el segmentador «Entre» apila las cajas de inicio y fin; con 58 px de alto la fecha final quedaba oculta. Precipitación diaria, Mapa de precipitación y Mapa de radiación: segmentador de fecha de 100 px y sin deslizador. Comparación entre periodos: Periodo A y B colocados lado a lado.

## 2026-11-13 · Faltantes y estaciones solo de precipitación
- Diagnóstico (consulta DAX): las RLS reportaban temperatura (medias mensuales de 6–9 °C, sin sentido físico) y LVS-RLS tenía 133 días con 0 °C; además LVS-RLS tenía 589 días sin lluvia registrada pero 65 meses "válidos", porque la completitud contaba filas y no días con dato.
- `TablaEstaciones_met`: lista `SoloPrecipitacion` (42, 69, 76, 77) y columna `Solo_Precip`; en `fxLimpiarDiario` esas estaciones conservan solo la precipitación.
- `fxLimpiarDiario`: día con temperatura media, mínima y máxima en 0 → sin dato (también sensación térmica); radiación diaria 0 y ETo 0 → sin dato.
- `Fact_Mensual_met`: completitud por variable; cada valor mensual se anula si su variable tiene dato en menos del 80 % de los días. Se actualizó también la expresión de la política de actualización incremental.
- Mes en curso preliminar: `Fact_Mensual_met[Mes_Preliminar]`; la completitud del mes en curso se mide contra los días hasta el último dato descargado (antes: hasta hoy, lo que en Desktop, con RangeEnd fijo, nunca alcanzaba el 80 %). Gráficas tipo R: punto hueco y el tooltip indica "preliminar, datos al …"; en variables acumulativas no se anota anomalía (el total aún está incompleto) y en las comparativas mensuales no se muestra. Los acumulados siguen hasta el último mes cerrado y el periodo histórico excluye el año de análisis.
- `N_Estaciones`: cuenta solo las estaciones con dato de la variable seleccionada en el año de análisis (una RLS ya no suma en temperatura); el título de estación individual usa el mismo criterio.

## 2026-11-13 · Exclusión de estaciones, títulos y acumulados con faltantes
- Las estaciones ILU, El Carmen y las RLS se excluyen en el modelo (se quitan de la lista de `TablaEstaciones_met`; quedan anotadas en un comentario) en lugar de un filtro de informe: el filtro sobre `Estación` hacía que `ISFILTERED` fuera siempre verdadero y el título nunca mostraba el estrato o la región. Se quitó el filtro de `report.json`. Quedan 43 estaciones.
- `Titulo_Seleccion`: con estaciones elegidas a mano muestra "Estaciones A, B, C" (hasta 3) o "Estaciones seleccionadas" (el número va en el subtítulo), y añade "— Estrato X" y/o "— Región Y" según lo que compartan. Estaciones, estratos, regiones y país se toman de las estaciones con dato de la variable en el año de análisis.
- Acumulados (`Acum_Mensual`, `Acum_Comp_1–4`, `Acum_Mes_Por_Anio`): una estación entra al promedio del grupo solo si tiene todos los meses del acumulado; antes los meses faltantes se omitían y la curva se quedaba en el último valor (caso El Carmen).
- Títulos (ajuste): con dos o más estaciones elegidas a mano el título es "Estaciones seleccionadas"; el subtítulo (`Subtitulo_Detalle`) indica n estaciones y, por cada estrato y región presentes, n/N (N = estaciones de esa delimitación con dato de la variable en el año; con más de 3 se resume como "4 estratos"). Con solo segmentadores de estrato o región el título no cambia ("Estrato X — Región Y").
- Delimitación: "Red meteorológica ICC Guatemala", "… El Salvador" o "… Guatemala y El Salvador" según los países con dato (se elimina "Costa sur de Guatemala"). En el subtítulo de estrato o región solo va el país o países (`Paises_Txt`).
- Cuenca: título "Cuenca X" si se elige una cuenca en el menú (sin estaciones a mano); subtítulo con país, n estaciones y n/N por estrato y región presentes. Una sola estación conserva "Estación X".
- Precipitación diaria: el acumulado desde el 1 de enero solo incluye estaciones con dato todos los días hasta la fecha (antes los días faltantes dejaban tramos planos).
- Se retira la versión heredada (`20260108 - Power BI Guatemala.pbip`); queda en el historial y en la etiqueta `v1.0`.
- Acumulados (ajuste): si el periodo incluye el inicio del registro de una estación, se acumula desde su primer mes válido (años incompletos al inicio del histórico sí se muestran, también como años adicionales); un hueco posterior sí corta la curva. En agregados, la estación no aporta antes de su inicio.
- Estaciones (ajuste del responsable): se vuelven a incluir El Carmen (46) y las RLS (42, 69, 76, 77; solo precipitación). Quedan fuera las ILU. Total: 48 estaciones.

## 2026-11-13 · Método de anomalías para agregados
- Diagnóstico: en el estrato Alto conviven estaciones de 300–350 m con muchos años (Cengicaña, Lorena, Concepción) y de 1 200–2 300 m con pocos años; la media histórica reflejaba casi solo las bajas mientras el año actual ya incluía las altas (Alto aparecía siempre más frío y seco). En Bajo, Litoral y Medio las diferencias en temperatura eran < 0.6 °C.
- Agregados (más de una estación): media del grupo = promedio de las medias de cada estación en el periodo base (Jones y Hulme, 1996); valor del grupo en un año = media del grupo + anomalía media (valor − media propia) de las estaciones con dato ese año. De esa serie salen P33, P66, mínimo y máximo. Aplica al año de análisis, años adicionales, históricos mensuales y acumulados. Medidas: `_B_Normal`, `_B_Grupo`; históricos `Hist_*` con tabla estación × año.
- Mínimo de años por estación en el periodo base: 3 (`Min_Anios_Base`). Las estaciones con menos no entran a los agregados ni al contador; individualmente se muestran con sus años.
- Una sola estación: mismo resultado que antes (su media y sus años).
- Observación pendiente de revisar con la red: la radiación (y por ello la ETo) de las estaciones con más años es 3–6 % menor que la de las nuevas; puede ser deriva o calibración de los radiómetros.
- Precipitación en agregados: anomalía relativa (valor ÷ media propia de la estación) en lugar de diferencia; con diferencias, en meses secos una estación lluviosa con anomalía negativa grande llevaba la serie del grupo a valores negativos. Se recomienda así en Jones y Hulme (1996).
- Gráficas tipo R: las etiquetas de los años adicionales se ordenan por su valor final y se separan con una distancia mínima (6 % del rango del eje) para que no se traslapen.
- Etiquetas de anomalía: si el valor absoluto es menor que 1 se muestra con un decimal (evita "0 mm (+12 %)").

## 2026-11-13 · Exclusión en agregaciones y método de validación
- Se incluyen de nuevo todas las estaciones (61; ILU incluidas). Lista `ExcluirAgregados` en `TablaEstaciones_met` (ILU 81–93 y RLS 42, 69, 76, 77) → columna `Estaciones_met[Excluir_Agregados]`. Esas estaciones no entran a los cálculos de grupo (estrato, región, cuenca, país o red completa); sí entran si se eligen a mano en el segmentador de estaciones, y se ven individualmente (mapas, una sola estación).
- Comparación con los scripts R: diferencias por (1) método de agregación, (2) estaciones del histórico (R solo usa las que tienen dato en el año actual; se descarta replicarlo), (3) faltantes (R suma sin completitud: meses sin dato = 0), (4) periodo base, (5) fuente/QC de 15 min, (6) conjunto de estaciones y meses. En Alto, R muestra 2026 entre 2 y 4.7 °C bajo la media y la lluvia 40–80 % bajo: efecto de mezclar estaciones de 300 m y > 1 200 m, que el método de anomalías corrige. En Pacífico, R muestra la radiación de 2026 sobre la media todo el año, coherente con la diferencia de radiómetros nuevos y antiguos.
- Método oficial: anomalías. Solo en la página Validación hay un segmentador "Método de agregación" (`Metodo_Agregacion`, medida `_Metodo_Directo`) para comparar con el promedio directo de los scripts R.
- Si ninguna estación de la selección tiene el mínimo de años en el periodo base (p. ej., varias ILU elegidas a mano), el grupo se calcula con promedio directo y todas cuentan (`_Sin_Elegibles`); antes quedaba en blanco con 0 estaciones.

## 2026-11-13 · Tipos de estación y combinaciones a mano
- `Estaciones_met[Tipo]`: B = ILU 81–93 (lista `TipoB` en `TablaEstaciones_met`); A = el resto, RLS incluidas.
- Agregados predefinidos (estrato, región, cuenca, país, red): solo Tipo A meteorológicas (sin RLS ni B), como antes.
- Selección a mano: A y RLS se combinan entre sí; B solo entre B. Si se eligen A y B a la vez, la gráfica queda en blanco; título "Selección no combinable" y subtítulo "Estaciones tipo A (n) y tipo B (n)".
- Grupos B (y cualquier grupo sin estaciones con el mínimo de años): promedio directo; cuando alcanzan el mínimo siguen la misma ruta que las A (anomalías).
- Mínimo de años por estación (≥ 3 años con dato en el periodo base, en cualquier mes), ya no mes a mes: una estación elegible aporta todos los meses y su media de cada mes usa los años que tenga ese mes (caso La Confianza, que solo mostraba la segunda mitad del año). Los años adicionales incompletos se siguen mostrando como antes.

## 2026-11-13 · Opción "Mes preliminar"
- Nueva capa "Mes preliminar" en el menú Mostrar (`Mostrar_Preliminar`) para las gráficas tipo R. Por defecto: activada en temperaturas, sensación térmica y variables acumulativas; desactivada en precipitación, radiación, evapotranspiración y balance hídrico (en las páginas de radiación y evapotranspiración el valor por defecto sigue la variable inicial; para irradiancia o ETo media diaria se activa a mano).
- Acumulados: con la opción activada, el acumulado del año llega al mes en curso (punto hueco y aviso en el tooltip; sin anomalía en ese punto, porque se compara con la media acumulada al fin de mes).

## 2026-11-16 · Optimización de las medidas históricas
- En el servicio aparecía `rsQueryMemoryLimitExceeded` (límite de memoria por consulta). Causa: las medidas del método de anomalías evaluaban `_Mes_Est` celda por celda (estación × año × mes) y lo repetían en cada medida y mes; en los acumulados se multiplicaba por los meses acumulados.
- `Hist_*`, `_B_Grupo` y `_Anios_Base_Est` leen ahora la tabla mensual una sola vez (estación × año × mes con la columna de la variable) y hacen el resto en memoria. Mismo resultado, mucha menos memoria. `_B_Grupo` resuelve también el caso de una estación o promedio directo; se elimina `_B_Normal`.
- Mes preliminar en el servicio: la tabla mensual descarta el día en curso y las fechas futuras, y el último dato de referencia nunca es posterior a ayer (en el servicio, con RangeEnd al fin de mes, una fecha adelantada dejaba la completitud del mes en curso por debajo del 80 %).
- Acumulados con ETo: el título del eje Y ("Evapotranspiración potencial (ETo) acumulada (mm)") era más largo que el alto de la gráfica y desplazaba el título fuera del visual; se acorta a "Evapotranspiración (ETo) acumulada (mm)" en `Eje_Y_Acum`.
