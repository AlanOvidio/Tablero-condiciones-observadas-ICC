# Decisiones y cambios

Bitácora del proyecto. Una entrada por cambio lógico (coincide con un commit).

## 2026-11-04 · Línea base y plan
- Se crea el repositorio Git. **Commit 1** = versión heredada sin modificaciones (`20260108 - Power BI Guatemala.pbip`).
- Se agregan `README.md`, `docs/01_plan_reformulacion.md` y esta bitácora.
- `.gitignore` excluye `cache.abf`, `localSettings.json` y los scripts R con credenciales (`otros_archivos/*.R`).
- Decisión: **arquitectura nueva** (modelo propio basado en `Tablero-semanal-ICC`), no reporte delgado sobre el modelo semanal.
- Decisión: la apariencia sigue a los scripts R (`script_figs_zonasclima_.R`, `script_nuevo.R`); agrupación dinámica por **estación, estrato altitudinal o región climática** para todas las variables.
