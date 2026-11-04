#!/usr/bin/env python3
"""Copia config/estaciones_region.csv al bloque <regiones> de Estaciones_met.tmdl.
Ejecutar con Power BI Desktop CERRADO, desde la raíz del repositorio:
    python tools/aplicar_regiones.py
"""
import csv, os, re, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMDL = os.path.join(RAIZ, "Condiciones_observadas.SemanticModel", "definition", "tables", "Estaciones_met.tmdl")
CSV = os.path.join(RAIZ, "config", "estaciones_region.csv")

# Nombres que se muestran en el tablero
NOMBRE = {
    ("Guatemala", "Region Pacifico"): "Pacífico",
    ("Guatemala", "Region Bocacosta"): "Bocacosta",
    ("Guatemala", "Region Altiplano Central"): "Altiplano Central",
    ("El Salvador", "Pacifico"): "Pacífico (SV)",
    ("El Salvador", "Montañosa"): "Montañosa (SV)",
}

filas = []
with open(CSV, encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        reg = NOMBRE.get((r["pais"], r["region_climatica"]), r["region_climatica"].replace("Region ", ""))
        filas.append(f'{{{int(r["estacionid"])}, "{reg}"}}')

with open(TMDL, encoding="utf-8") as f:
    texto = f.read()
m = re.search(r"(?P<ind>[ \t]*)// <regiones>\n.*?\n(?P<ind2>[ \t]*)// </regiones>", texto, re.S)
if not m:
    sys.exit("No se encontró el bloque <regiones> en Estaciones_met.tmdl")
ind = m.group("ind")
bloque = f"{ind}// <regiones>\n" + ",\n".join(ind + x for x in filas) + f"\n{ind}// </regiones>"
texto = texto[:m.start()] + bloque + texto[m.end():]
with open(TMDL, "w", encoding="utf-8", newline="\n") as f:
    f.write(texto)
print(f"{len(filas)} estaciones con región escritas en Estaciones_met.tmdl")
