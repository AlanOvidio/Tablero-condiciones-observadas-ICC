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
