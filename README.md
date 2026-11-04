# Tablero de condiciones meteorológicas observadas — ICC

Tablero de Power BI que muestra las condiciones meteorológicas observadas por la **Red Meteorológica del ICC** (API REDMET) en Guatemala y El Salvador, y su comparación con el registro histórico. Uso principal: **consulta de información meteorológica**; uso secundario: apoyo a la toma de decisiones.

- **Responsable:** Alan — equipo CeH, ICC
- **Formato:** Power BI Project (`.pbip`), modelo en TMDL y reporte en PBIR, versionado con Git
- **Modelo de referencia:** `Tablero-semanal-ICC` (mismas funciones de API, calendario y dimensión de estaciones)

## Estado

En **reformulación** (rama `v2`). Plan: [docs/01_plan_reformulacion.md](docs/01_plan_reformulacion.md) · bitácora: [docs/02_decisiones_y_cambios.md](docs/02_decisiones_y_cambios.md).

## Contenido

```
├── Condiciones_observadas.pbip          ← tablero nuevo (abrir este)
├── Condiciones_observadas.SemanticModel/ ← modelo: tablas, Power Query (M), medidas DAX (TMDL)
├── Condiciones_observadas.Report/        ← reporte: páginas y visuales (JSON)
├── 20260108 - Power BI Guatemala.pbip    ← versión heredada; se elimina al alcanzar paridad
├── config/estaciones_region.csv          ← estación → región climática (generado)
├── tools/
│   ├── generar_regiones.R                ← spatial join estaciones × shapefile → config/estaciones_region.csv
│   └── aplicar_regiones.py               ← copia el CSV al modelo (Power BI cerrado)
├── otros_archivos/                       ← shapefile de regiones climáticas (scripts R de referencia: no se versionan)
└── docs/                                 ← plan y bitácora
```

## Actualizar regiones (si cambian estaciones o el shapefile)

Con Power BI Desktop cerrado, desde la raíz del repositorio:

```
Rscript tools/generar_regiones.R
python tools/aplicar_regiones.py
```

Las credenciales de la API se leen de las variables de entorno `REDMET_USER` y `REDMET_PASS`.

> Los scripts `.R` de `otros_archivos/` no se versionan porque contienen credenciales en texto plano.
