# Plan de reformulación — Tablero de condiciones observadas

> Estado: **borrador para aprobación** (2026-11-04). Marcar cada tarea al completarla y registrar el detalle en [02 · Decisiones y cambios](02_decisiones_y_cambios.md).

## Objetivo

Reconstruir el tablero con una arquitectura nueva que:

1. **Muestre la información meteorológica observada** (uso principal) y permita compararla con el histórico (apoyo a decisiones).
2. Conserve **todas las acciones** del tablero heredado (ver tabla de paridad).
3. Permita **agrupar de forma dinámica** por *estación*, *estrato altitudinal* o *región climática* **para todas las variables**.
4. Tenga la **apariencia de los gráficos de los scripts R** (`otros_archivos/`), y produzca los **mismos números** que esos scripts.
5. Reutilice lo probado en `Tablero-semanal-ICC` (funciones de API, calendario, dimensión de estaciones, actualización incremental, documentación).

## Diagnóstico de la versión heredada (resumen)

| Área | Problema | Consecuencia |
|---|---|---|
| Consultas | 60 tablas, una por estación (mismo M copiado), unidas en `Anexar1` con 57 pasos | Agregar una estación exige editar dos lugares; actualización lenta |
| Fechas | ~60 `LocalDateTable` automáticas; medidas dependen de `[Días].[NroMes]` | Modelo pesado; no hay calendario común |
| Pasos residuales | Columnas `Rad Min/Med/Max` constantes, `Nombre = "Cengicaña"`, `Día - Copia`, filtros `each true`, nombres con espacio final | Ruido y errores de mantenimiento |
| Radiación | `suma / 97 × 0.0864` | Subestima ~1 % (son 96 lecturas); peor con datos faltantes |
| Dimensiones | `Cuencas` y `Cuencas_real` desde Excel de 2020 en SharePoint, relación bidireccional; consultas sin uso | Datos desactualizados, ambigüedad de filtros |
| Medidas | ~50 medidas copiadas por variable × estadístico | Difícil de mantener |
| Históricos | "PROMEDIO" es la mediana; percentiles de valores **diarios** comparados con medias **mensuales** (Tmax, Tmin, Rad, ETPd, sensación térmica) | Banda normal demasiado ancha: el año actual casi siempre luce "normal" |
| Índice de calor | Columna calculada con Tmax + HRmax | Físicamente inconsistente; la API ya trae `indicecalormax` |
| Reporte | 19 páginas (4 ocultas), varias duplicadas | Navegación confusa |

## Arquitectura propuesta

```mermaid
flowchart LR
    A1["API /ws/redmet/estaciones"] --> E["Estaciones_met<br/>+ estrato (API)<br/>+ región climática (config)"]
    A2["API /ws/getlecturasdia"] --> F["fxLecturasEstacion_met_diario"] --> D["Fact_Diaria_met<br/>estación × día"]
    D --> M["Fact_Mensual_met (DAX)<br/>estación × año × mes<br/>+ N_dias (completitud)"]
    C["Calendario<br/>año civil + hidrológico,<br/>pentada, día juliano"] -.-> D & M
    E -.-> D & M
    P1["Agrupar_por<br/>(parámetro de campo)"] --> R["Reporte"]
    P2["Variables<br/>(unidad, regla, colores)"] --> R
    P3["Años_Comparacion · Periodo A/B ·<br/>Periodo base"] --> R
    D & M --> R
```

### Tablas

| Tabla | Origen | Notas |
|---|---|---|
| `Estaciones_met` | API (igual que el semanal) | Se le une `config/estaciones_region.csv` (estación → región climática). El Salvador: región = estrato recodificado (Litoral/Bajo → Pacífico; Medio/Alto → Montañosa), como en `script_nuevo.R`. |
| `TablaEstaciones_met` | Lista de IDs | Único lugar para agregar o quitar estaciones (equivale a `estaciones_ids` y `estaciones_nousar` de R). |
| `Calendario` | M (del semanal) | Se agregan Pentada, Día juliano, Mes abreviado (Ene…Dic). |
| `Fact_Diaria_met` | `fxLecturasEstacion_met_diario` (del semanal) | Actualización incremental. Radiación en MJ/m² = suma W/m² × 900 / 10⁶. |
| `Fact_Mensual_met` | Tabla calculada DAX | Grano estación × año × mes: sumas (Pp, Rad, ETo), medias (T, HR, viento), `BH = Pp − ETo`, `N_dias`. Replica `mensual_por_estacion()` de R. |
| `Agrupar_por` | Parámetro de campo | Estación · Estrato altitudinal · Región climática. Se usa en ejes, leyendas y múltiplos pequeños. |
| `Variables` | Tabla (`config/variables.csv`) | Variable, unidad, regla de agregación, decimales y colores de los scripts R (ver Apariencia). |
| `Años_Comparacion` | Tabla desconectada | Equivale a `anios_ad` de R (líneas de años adicionales). |
| `Periodo A`, `Periodo B` | Copias de fechas | Conserva la comparación entre periodos. |
| `_Medidas` | — | Todas las medidas. |

### Reglas de cálculo (iguales a los scripts R)

1. **Lectura → día → mes por estación:** sumas para Pp, Rad, ETo; medias para T, HR, viento.
2. **Mes por grupo:** promedio de las estaciones del grupo (estrato, región o una sola estación) que tienen dato.
3. **Histórico por grupo y mes:** sobre los años del **periodo base** (por defecto, todos los anteriores al año de análisis): media, mínimo, máximo, P33 y P66 **de los valores mensuales del grupo** (no de valores diarios).
4. **Acumulados:** suma acumulada desde enero (o desde el inicio del año hidrológico, según se decida). Las bandas acumuladas se calculan como en R (`cumsum` de cada estadístico).
5. **Anomalías:** T en °C; Pp en mm y %. Categorías de `script_nuevo.R`: ±0.5/±1 °C y ±15/±40 %.
6. **Completitud:** un mes entra al histórico solo si tiene ≥ 80 % de días con dato (*mejora respecto a R; validar*).

Todas las medidas usan la variable elegida en `Variables` y la agrupación elegida en `Agrupar_por`, así que **un mismo visual sirve para todas las variables y agrupaciones**.

### Apariencia (de `tema_boletin` y las paletas de R)

| Elemento | Estilo |
|---|---|
| Rango histórico (mín–máx) | Banda clara (alfa ~0.18) |
| Rango normal (P33–P66) | Banda más intensa (alfa ~0.40) |
| Media histórica | Línea discontinua dorada (`gold1`/`gold3`) con puntos |
| Año de análisis | Línea continua gruesa con puntos, color por variable |
| Años adicionales | Paleta `#4000D3 #F720F0 #FF8C00 #666666 #008B8B #8B0000 #2F4F4F #B8860B`, etiqueta al final |
| Paletas por variable | T: `tomato`/`tomato3` + `red4` · Pp: `steelblue`/`steelblue4` + `blue4` · Rad: `#F4A460`/`#CD853F` + `#8B4513` · ETo: `#8FBC8F`/`#2E8B57` + `#006400` · BH: `#7EC8E3`/`#4A90D9`, barras `#2171B5` (superávit) / `#D94701` (déficit) |
| Anomalías | `#d73027 #fc8d59 #91bfdb #4575b4 #313695` (muy por encima → muy por debajo) |
| Tipografía y ejes | Fondo blanco, cuadrícula gris discontinua, ejes negros, título centrado en negrita, subtítulo gris, leyenda abajo, nota de fuente y n.º de años |

Se implementa con un **tema JSON** y, para el gráfico climatológico, con el visual que se decida (ver decisión D1).

## Paridad: páginas heredadas → páginas nuevas

| Página nueva | Reemplaza a (heredadas) |
|---|---|
| **1. Mapa y resumen** — valor del último día/semana/mes y anomalía por estación, coloreado por categoría | Mapa de precipitación, Mapa de Radiación, Mapa de Sensación Térmica |
| **2. Serie diaria** — variable × agrupación × rango de fechas, con tabla | Precipitación diaria, Comparativas por estación/por año (gráficas diarias), Comparación de Temperaturas |
| **3. Climatología mensual** — estilo R con bandas, media, actual, años adicionales y etiquetas de anomalía | Comparativo histórico de Pp, ETP (mensual y diaria), TMax, TMin, Radiación, Sensación térmica; Precipitación histórico (oculta) |
| **4. Acumulados** — Pp, Rad y ETo acumuladas vs. histórico; comparación Periodo A vs. B | Comparativas por estación, Comparativas por año (acumulada anual), Comparación entre Periodos (×2) |
| **5. Balance hídrico** — mensual (barras superávit/déficit + bandas) y por pentada | Balance hídrico (×2) |
| **6. Radiación por niveles** — pentadas con umbrales subóptimo/aceptable/óptimo editables | Comparación de Radiación |
| **7. Anomalías** — tabla/heatmap grupo × mes (como `script_nuevo.R`) | *Nuevo* |
| **8. Notas metodológicas** | *Nuevo* |

Panel de filtros uniforme en todas: Variable · Agrupar por · País · Estrato · Región · Estación · Año de análisis · Años adicionales.

## Fases

### Fase 0 · Línea base y seguridad
- [x] Repositorio Git; commit 1 = versión heredada sin cambios.
- [x] Commit 2 = README, plan, bitácora, `.gitignore`.
- [ ] Sacar las credenciales de los scripts R (`Sys.getenv("REDMET_USER")`/`.Renviron`) y cambiar esas contraseñas; luego versionar los scripts.

### Fase 1 · Definiciones y configuración
- [x] Resolver las decisiones (abajo).
- [ ] `config/estaciones_region.csv` con `tools/generar_regiones.R` (todas las estaciones) y `tools/aplicar_regiones.py` (spatial join con `regiones_gcs_wgs_1984.shp`, mismo criterio que R).
- [ ] `config/variables.csv` (variables, unidades, reglas, colores).

### Fase 2 · Modelo nuevo (rama `v2`)
- [x] Nuevo proyecto `Condiciones_observadas.pbip` en este repositorio, con tablas tomadas del semanal (`Estaciones_met`, `TablaEstaciones_met`, `Calendario`, `fxLecturasEstacion_met_diario`, `Fact_Diaria_met`).
- [x] `Fact_Mensual_met`, `Agrupar_por`, `Variables`, `Meses_Acum`, `Anios_Comparacion`, `Base_Inicio/Fin`, `Periodo_A/B`.
- [x] Abrir en Desktop, actualizar y validar carga.
- [x] Fecha/hora automática **desactivada**.

### Fase 3 · Medidas y validación
- [x] Medidas genéricas: valor del periodo, histórico (media, mín, máx, P33, P66), acumulados, anomalías, categoría, colores dinámicos.
- [ ] **Validación contra R:** mismas cifras que `script_figs_zonasclima_.R` para 2 regiones × (Pp, T, Rad, ETo, BH) en un año cerrado (tolerancia 0.1).

### Fase 4 · Reporte y tema
- [x] Tema JSON con el estilo de `tema_boletin`.
- [x] Páginas generadas (8). Pendiente: revisión visual y ajustes en Desktop.

### Fase 5 · Cierre
- [ ] Revisión de paridad página por página.
- [ ] Documentación (arquitectura, diccionario, medidas, guía de usuario) con los generadores del semanal.
- [ ] Publicación; retiro del `.pbip` heredado (queda en el historial de Git); etiqueta `v1.0`.

## Decisiones (2026-11-04)

| # | Tema | Decisión |
|---|---|---|
| D1 | Gráfico climatológico | **Deneb** (visual gratuito y de código abierto, en AppSource) para páginas 3–5; visuales nativos en el resto. |
| D2 | Tmax/Tmin mensual | Como los scripts R: **máxima y mínima absolutas** del mes. Con varias estaciones, promedio de esos extremos entre estaciones. |
| D3 | Inicio de acumulados | **Seleccionable**: año civil (ene–dic) o hidrológico (nov–oct). Tabla `Meses_Acum`. |
| D4 | Estaciones | **Todas** las del tablero heredado (61 IDs, incluido Chaparrastique = 40), no solo las 44 de los scripts. |
| D5 | Periodo base | **Seleccionable** (`Base_Inicio`, `Base_Fin`); por defecto todos los años anteriores al de análisis. |
| D6 | Cuencas | Se mantienen (Excel de SharePoint, hoja `Hoja2`), unidas a `Estaciones_met` por nombre. |
| D7 | Fuente de datos | Solo el **endpoint diario** (`getlecturasdia`). La irradiancia diurna media se aproxima como Σ W/m² / 52 (ventana fija 06:00–18:59, igual que R). |
| D8 | Agregación entre estaciones | Variables acumulativas (Pp, ETo, BH, Rad): **suma por estación y luego promedio** de las estaciones con dato. Promedios: promedio por estación y luego entre estaciones. Extremos: extremo por estación y luego promedio. |
| D9 | Meses incompletos | Los valores **mensuales** solo se muestran cuando el mes terminó y tiene ≥ 80 % de días con dato (`Fact_Mensual_met[Mes_Valido]`). |
| D10 | Radiación | Selector entre **energía diaria acumulada (MJ/m²)** e **irradiancia diurna media (W/m²)** (variables RAD e IRR). |
| D11 | Exportar | No hay botón nativo para exportar la página con licencia Pro (la API de exportación requiere capacidad dedicada). Se usa *Exportar → PDF* del servicio con "Solo página actual" y se documenta en la guía de usuario. |

## Diseño propuesto para las páginas diarias (precipitación y radiación)

- **Mapa:** burbujas de tamaño fijo coloreadas por **clases** del total del periodo (Pp: 0, 1–5, 5–20, 20–50, > 50 mm; Rad: escala secuencial) con etiqueta de valor. El tamaño variable de las burbujas actuales dificulta comparar.
- **Matriz de calor grupo × día:** filas = estación, estrato o región (según *Agrupar por*), columnas = días, color = valor. Reemplaza la gráfica de columnas con 40 estaciones en la leyenda.
- **Serie del grupo:** columnas diarias + línea del **acumulado** (eje secundario) para Pp; columnas diarias + **media móvil de 7 días** + líneas de umbral (subóptimo/aceptable) para radiación.
- **Múltiplos pequeños** por grupo cuando se comparan estratos o regiones, en lugar de leyendas largas.
