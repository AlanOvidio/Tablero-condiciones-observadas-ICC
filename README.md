# Tablero de condiciones meteorológicas observadas — ICC

Tablero de Power BI que muestra las condiciones meteorológicas observadas por la **Red Meteorológica del ICC** (API REDMET) en Guatemala y El Salvador, y su comparación con el registro histórico. Uso principal: **consulta de información meteorológica**; uso secundario: apoyo a la toma de decisiones.

- **Responsable:** Alan — equipo CeH, ICC
- **Formato:** Power BI Project (`.pbip`), modelo en TMDL y reporte en PBIR, versionado con Git
- **Modelo de referencia:** `Tablero-semanal-ICC` (mismas funciones de API, calendario y dimensión de estaciones)

## Estado

En **reformulación**. La versión heredada (`20260108 - Power BI Guatemala.pbip`) se conserva sin cambios en el primer commit como línea base. El plan está en [docs/01_plan_reformulacion.md](docs/01_plan_reformulacion.md) y cada cambio se registra en [docs/02_decisiones_y_cambios.md](docs/02_decisiones_y_cambios.md).

## Contenido

```
├── 20260108 - Power BI Guatemala.pbip   ← versión heredada (se retirará al alcanzar paridad)
├── docs/                                ← plan, decisiones y bitácora
├── config/                              ← tablas editables (estación → región climática, variables)
├── tools/                               ← scripts auxiliares (asignación de regiones)
└── otros_archivos/                      ← shapefile de regiones climáticas y scripts R de referencia
```

> Los scripts `.R` de `otros_archivos/` **no se versionan** porque contienen credenciales en texto plano. Ver el plan, fase 0.
