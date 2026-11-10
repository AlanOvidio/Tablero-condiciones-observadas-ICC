# Guía de usuario

Tablero de condiciones meteorológicas observadas de la Red Meteorológica del ICC. Muestra los datos observados y los compara con el histórico.

## Filtros comunes (panel derecho)

| Filtro | Qué hace |
|---|---|
| **País, Región climática, Estrato altitudinal, Cuenca** | Limitan las estaciones. Una región o un estrato son las agrupaciones predeterminadas. |
| **Estación** | Elegir una o varias estaciones. **Ctrl + clic** para agregar varias; un clic simple reemplaza la selección. |
| **Variable** | En las páginas con varias variables (p. ej. temperatura media, máxima o mínima). |
| **Año de análisis** | Año que se compara contra el histórico. Sin selección: el año del último dato. |
| **Periodo histórico** | Rango de años del histórico. Solo ofrece años anteriores al de análisis. |
| **Añadir años** | Hasta 4 años para dibujar como líneas punteadas. |
| **Mostrar** | Capas de la gráfica: año actual, media histórica (apagada por defecto), rangos históricos, años adicionales y anomalías. |

**Sin ninguna estación elegida se usa toda la red** (o las estaciones que dejen los filtros).

## Cómo se combinan varias estaciones

- **Lluvia, ETo, balance y radiación:** se suma por estación y luego se promedia. Ej.: 3 estaciones con 200, 300 y 400 mm en el mes → **300 mm**.
- **Temperaturas y sensación térmica:** promedio entre estaciones (en máximas y mínimas, del extremo de cada estación).
- Solo cuentan las estaciones que tienen dato en ese periodo.

## Comparativos históricos (gráficas tipo R)

- **Título:** la estación, el estrato o la región si esa es la selección; con otra combinación, la delimitación (p. ej. "Costa sur de Guatemala").
- **Subtítulo:** año de análisis y número de estaciones.
- **Banda clara:** rango histórico (mínimo–máximo); la leyenda indica los años con datos.
- **Banda oscura:** rango normal (percentiles 33–66). Un mes dentro de esta banda es "normal".
- **Línea gruesa con puntos:** año de análisis. **Línea punteada dorada:** media histórica.
- **Etiquetas:** anomalía respecto a la media (en lluvia y balance, positivo en azul; en temperatura, ETo y radiación, positivo en rojo).
- **Los meses en curso no se muestran** hasta que terminan; tampoco meses con menos de 80 % de días con dato.
- **Precipitación acumulada:** también ETo y radiación; el acumulado puede iniciar en enero (año calendario) o en noviembre (año hidrológico).
- **Balance hídrico:** la línea roja punteada marca el cero (arriba superávit, abajo déficit).

## Otras páginas

| Página | Uso |
|---|---|
| Comparativas por estación / por año / de temperaturas | Líneas mensuales por año (o por estación) para comparar campañas. |
| Comparación de radiación | Radiación media diaria por pentada frente a los niveles subóptimo, aceptable y óptimo (deslizables). |
| Precipitación diaria, mapas | Lluvia, radiación o sensación térmica por estación en el periodo elegido. |
| Balance hídrico por pentadas | Lluvia y ETo por pentada; clic en una pentada para ver sus fechas. |
| Comparación entre periodos | Dos periodos lado a lado y su acumulado día a día. |
| Notas metodológicas | Criterios de cálculo. |

## Exportar

En el servicio de Power BI: **Exportar → PDF** y marcar **Solo página actual**. Con licencia Pro no hay un botón dentro del reporte para exportar.
