# Repositorio Git y GitHub

Repositorio privado `Tablero-condiciones-observadas-ICC`, gestionado con GitHub Desktop.

## Ramas y versiones

| Rama / etiqueta | Contenido |
|---|---|
| `main` | Versión vigente. Desde la etiqueta `v1.0` contiene el tablero reformulado (`Condiciones_observadas.pbip`); la versión heredada se retiró en v1.2 (disponible en la etiqueta `v1.0`). |
| `v1.0` | Primera versión del tablero reformulado (fusión del *Pull Request* #1, rama `v2`). |
| Ramas de trabajo | Una por tema (p. ej. `comparativas-mensuales`, `cuencas`). Se fusionan a `main` con un *Pull Request* y, si se publica, se etiqueta la versión (`v1.1`, `v1.2`…). |

## Flujo de trabajo

1. **Fetch origin / Pull** antes de abrir Power BI. Para un cambio nuevo: *Branch → New branch*.
2. Cambios en Power BI → **guardar y cerrar**.
3. `python tools/generar_docs_modelo.py` y anotar el cambio en `docs/06_decisiones_y_cambios.md`.
4. GitHub Desktop: revisar archivos, un commit por cambio lógico → **Push origin**.
5. Al terminar el tema: *Pull Request* hacia `main` → **Merge** → en GitHub Desktop cambiar a `main` → **Pull origin**. Si se publica, etiquetar la versión (*History* → clic derecho → **Create tag** → **Push origin**).

Deshacer: *History* → clic derecho → **Undo commit** (sin push) o **Revert changes in commit** (ya subido).

## Qué se versiona y qué no

| Se versiona | No se versiona (`.gitignore`) |
|---|---|
| `.pbip`, TMDL del modelo, JSON del reporte, `diagramLayout.json`, `docs/`, `tools/`, `config/`, `deneb/`, shapefile de regiones | `.pbi/cache.abf` (datos), `.pbi/localSettings.json`, `_respaldo*/`, `.Rhistory`, índices `.sbn/.sbx` |

Después de clonar en otro equipo: abrir el `.pbip` y **Actualizar** (los datos no viajan en el repositorio).
