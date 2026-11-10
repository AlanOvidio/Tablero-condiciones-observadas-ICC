# Tablero de condiciones meteorológicas observadas — ICC

Modelo semántico y reporte de Power BI que muestran las condiciones meteorológicas observadas por la **Red Meteorológica del ICC** (API REDMET) en Guatemala y El Salvador y su comparación con el histórico, con gráficas al estilo de los scripts R del equipo. Uso principal: consulta de información meteorológica; uso secundario: apoyo a decisiones.

- **Responsable:** Alan — equipo CeH, Instituto Privado de Investigación sobre Cambio Climático (ICC)
- **Formato:** Power BI Project (`.pbip`): modelo en TMDL y reporte en PBIR, versionados con Git
- **Licencia de Power BI:** Pro · **Visual requerido:** Deneb
- **Estado:** reformulación en la rama `v2` (en validación); `main` conserva la versión heredada

## Contenido de la carpeta

```
├── Condiciones_observadas.pbip            ← abrir este archivo en Power BI Desktop
├── Condiciones_observadas.SemanticModel/  ← modelo: tablas, Power Query (M), medidas DAX (TMDL)
├── Condiciones_observadas.Report/         ← reporte: páginas y visuales (JSON)
├── 20260108 - Power BI Guatemala.pbip     ← versión heredada (se elimina al cerrar la validación)
├── config/estaciones_region.csv           ← estación → región climática (generado)
├── deneb/                                 ← especificaciones Vega-Lite de las gráficas tipo R
├── docs/                                  ← documentación
├── tools/                                 ← regiones y documentación automática
└── otros_archivos/                        ← shapefile de regiones (scripts R de referencia: no se versionan)
```

## Documentación

| Documento | Para quién | Contenido |
|---|---|---|
| [01 · Arquitectura](docs/01_arquitectura.md) | Mantenimiento | Fuentes, flujo de datos, tablas, control de calidad, reglas de agregación, histórico, gráficas Deneb |
| [02 · Diccionario de datos](docs/02_diccionario_datos.md) ⚙️ | Mantenimiento | Parámetros, actualización incremental, relaciones, columnas y consultas |
| [03 · Catálogo de medidas](docs/03_catalogo_medidas.md) ⚙️ | Mantenimiento | Las medidas DAX por carpeta, con descripción y código |
| [04 · Guía de usuario](docs/04_guia_usuario.md) | Usuarios | Filtros, cómo leer las gráficas, páginas |
| [05 · Operación](docs/05_operacion.md) | Mantenimiento | Actualizar, publicar, tareas frecuentes, solución de problemas |
| [06 · Decisiones y cambios](docs/06_decisiones_y_cambios.md) | Mantenimiento | Bitácora: por qué el modelo funciona como funciona |
| [07 · Repositorio Git/GitHub](docs/07_repositorio_git.md) | Mantenimiento | Ramas y flujo de trabajo |
| [08 · Plan de reformulación](docs/08_plan_reformulacion.md) | Mantenimiento | Plan original, diagnóstico de la versión heredada y decisiones |
| [09 · Inventario de visuales](docs/09_inventario_visuales.md) ⚙️ | Mantenimiento | Páginas, visuales y campos |

⚙️ = se genera automáticamente; no editar a mano.

## Inicio rápido

1. Instalar el visual **Deneb** (Visualizaciones → … → Obtener más objetos visuales).
2. Abrir `Condiciones_observadas.pbip` → **Inicio → Actualizar** (descarga desde 2008 las estaciones de `TablaEstaciones_met`).
3. Revisar la página oculta **Validación**.

## Mantener la documentación al día

Después de cualquier cambio al modelo o al reporte, con Power BI cerrado y antes del commit:

```
python tools/generar_docs_modelo.py
```

Y registrar el cambio en [06 · Decisiones y cambios](docs/06_decisiones_y_cambios.md). Si cambian estaciones o el shapefile de regiones:

```
Rscript tools/generar_regiones.R
python tools/aplicar_regiones.py
```
