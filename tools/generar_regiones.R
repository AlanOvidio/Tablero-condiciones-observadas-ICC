# Asigna la región climática a cada estación (spatial join) y escribe
# config/estaciones_region.csv. Mismo criterio que script_figs_zonasclima_.R.
#
# Credenciales: definir en ~/.Renviron (no en el código)
#   REDMET_USER=...
#   REDMET_PASS=...
# Ejecutar desde la raíz del repositorio:  Rscript tools/generar_regiones.R

suppressPackageStartupMessages({
  library(httr); library(jsonlite); library(dplyr); library(sf)
})

usuario    <- Sys.getenv("REDMET_USER")
contrasena <- Sys.getenv("REDMET_PASS")
if (usuario == "" || contrasena == "") stop("Defina REDMET_USER y REDMET_PASS en .Renviron")

met_st <- bind_rows(
  fromJSON(content(
    GET("https://redmet.icc.org.gt/ws/redmet/estaciones",
        authenticate(usuario, contrasena, type = "basic"),
        add_headers(Accept = "application/json")),
    as = "text", encoding = "UTF-8"), flatten = TRUE),
  .id = "estacion") %>%
  filter(redmet == 1)

gtm_proj <- "+proj=tmerc +lat_0=14.66666666666667 +lon_0=-90.33333333333333 +k=0.9999 +x_0=500000 +y_0=0 +datum=WGS84 +units=m +no_defs"

reg_clim <- st_read("otros_archivos/regiones_gcs_wgs_1984.shp", quiet = TRUE) %>%
  st_transform(st_crs(gtm_proj)) %>%
  select(region_climatica = NOMBRE)

salida <- met_st %>%
  select(estacionid, codigo, finca, latitud, longitud, pais = pais.nombre, estrato = estrato.nombre) %>%
  st_as_sf(coords = c("longitud", "latitud"), crs = 4326, remove = FALSE) %>%
  st_transform(st_crs(gtm_proj)) %>%
  st_join(reg_clim) %>%
  st_drop_geometry() %>%
  mutate(region_climatica = case_when(
    !is.na(region_climatica)                              ~ region_climatica,
    pais == "El Salvador" & estrato %in% c("Litoral", "Bajo")  ~ "Pacifico",
    pais == "El Salvador" & estrato %in% c("Medio", "Alto")    ~ "Montañosa",
    TRUE                                                  ~ "Sin región")) %>%
  select(estacionid, codigo, finca, pais, estrato, region_climatica) %>%
  arrange(pais, region_climatica, finca)

dir.create("config", showWarnings = FALSE)
write.csv(salida, "config/estaciones_region.csv", row.names = FALSE, fileEncoding = "UTF-8")
print(table(salida$pais, salida$region_climatica))
cat("Escrito config/estaciones_region.csv (", nrow(salida), "estaciones )\n")
