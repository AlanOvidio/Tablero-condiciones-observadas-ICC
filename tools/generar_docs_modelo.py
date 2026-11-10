#!/usr/bin/env python3
"""
Genera la documentación automática del modelo semántico a partir de los archivos TMDL/PBIR:
  docs/02_diccionario_datos.md   (parámetros, actualización incremental, relaciones, tablas y columnas)
  docs/03_catalogo_medidas.md    (todas las medidas DAX agrupadas por tema, con descripción y código)
  docs/09_inventario_visuales.md (páginas y visuales del reporte con los campos que usan)

Uso (desde la carpeta raíz del proyecto; solo requiere Python 3.8+, sin librerías extra):
    python tools/generar_docs_modelo.py
Ejecutar después de cada cambio al modelo y antes de hacer commit.
Para documentar una medida nueva: agregar un comentario /// encima de la medida en TMDL,
o un comentario // en la primera línea de su expresión, o una entrada en FIJAS (abajo).
"""
import glob, json, os, re, datetime

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROY = "Condiciones_observadas"
DEF = os.path.join(RAIZ, f"{PROY}.SemanticModel", "definition")
PAGS = os.path.join(RAIZ, f"{PROY}.Report", "definition", "pages")
DOCS = os.path.join(RAIZ, "docs")

def leer(p):
    with open(p, encoding="utf-8") as f:
        return f.read().replace("\r\n", "\n")

TOP = re.compile(r"^\t(measure|column|partition|annotation|hierarchy|refreshPolicy)\b", re.M)
PROP = re.compile(r"^\t\t(formatString|lineageTag|displayFolder|dataCategory|annotation|changedProperty|isHidden|formatStringDefinition)\b", re.M)

def expresiones():
    s = leer(os.path.join(DEF, "expressions.tmdl")); out = []
    for b in re.split(r"\n(?=(?:/// .*\n)*expression )", "\n" + s):
        m = re.match(r"((?:/// .*\n)*)expression (\w+) =\s*(.*?)(?:\n\tlineageTag|\Z)", b, re.S)
        if m:
            out.append((m.group(2), m.group(1).replace("///", "").strip(), m.group(3).strip()))
    return out

def auto_desc(n):
    return None


def medidas(texto):
    out = []
    for m in re.finditer(r"^\tmeasure (.+?) =", texto, re.M):
        nombre = m.group(1).strip().strip("'")
        nx = TOP.search(texto, m.end())
        blk = texto[m.start(): nx.start() if nx else len(texto)]
        cab = blk.index("=") + 1
        pm = PROP.search(blk, cab)
        raw = blk[cab: pm.start() if pm else len(blk)]
        if "```" in raw:
            raw = raw.split("```")[1]
        lineas = [l[3:] if l.startswith("\t\t\t") else l.strip() for l in raw.split("\n")]
        expr = "\n".join(lineas).strip()
        g = lambda k: (re.search(rf"^\t\t{k}: (.+)$", blk, re.M) or [None, None])[1]
        previa = texto[:m.start()].rstrip("\n").split("\n")[-1].strip()
        desc = previa[3:].strip() if previa.startswith("///") else None
        if not desc:
            com = [l.strip()[2:].strip() for l in expr.split("\n") if l.strip().startswith("//")]
            desc = " ".join(com[:2]) if com else None
        if not desc:
            desc = auto_desc(nombre)
        out.append(dict(nombre=nombre, expr=expr, fmt=g("formatString"), cat=g("dataCategory"),
                        carpeta=g("displayFolder"), desc=desc))
    return out

def tablas():
    res = {}
    for f in sorted(glob.glob(os.path.join(DEF, "tables", "*.tmdl"))):
        s = leer(f)
        nombre = re.search(r"^table (.+)$", s, re.M).group(1).strip().strip("'")
        t = dict(columnas=[], medidas=medidas(s) if "\tmeasure " in s else [], politica=None, jerarquias=[],
                 fecha="\tdataCategory: Time" in s.split("\n\tcolumn", 1)[0], fuente="")
        for c in re.finditer(r"^\tcolumn (.+?)\n((?:\t\t.*\n|\n(?=\t\t))*)", s, re.M):
            b = c.group(2); g = lambda k: (re.search(rf"^\t\t{k}: (.+)$", b, re.M) or [None, None])[1]
            t["columnas"].append(dict(nombre=c.group(1).strip().strip("'"), tipo=g("dataType"), fmt=g("formatString"),
                                      orden=g("sortByColumn"), clave="\t\tisKey" in b, oculta="\t\tisHidden" in b))
        rp = re.search(r"^\trefreshPolicy\n((?:\t\t\w+: .+\n)+)", s, re.M)
        if rp: t["politica"] = dict(re.findall(r"\t\t(\w+): (.+)", rp.group(1)))
        for h in re.finditer(r"^\thierarchy (.+)\n((?:\t\t.*\n|\n)*)", s, re.M):
            niv = re.findall(r"\t\tlevel (.+)\n(?:\t\t\t.*\n)*?\t\t\tcolumn: (.+)", h.group(2))
            t["jerarquias"].append((h.group(1).strip("'"), [(a.strip("'"), b) for a, b in niv]))
        src = re.search(r"^\tpartition .+?\n.*?source =\s*\n?(.*?)(?=\n\tannotation|\n\t\w|\Z)", s, re.S | re.M)
        if src: t["fuente"] = re.sub(r"^\t{2,4}", "", src.group(1).strip("`\n"), flags=re.M).strip("`\n ")
        res[nombre] = t
    return res

def relaciones():
    s = leer(os.path.join(DEF, "relationships.tmdl")); out = []
    for r in re.split(r"(?=^relationship )", s, flags=re.M):
        if not r.strip(): continue
        out.append(dict(desde=re.search(r"fromColumn: (.+)", r).group(1), hacia=re.search(r"toColumn: (.+)", r).group(1),
                        activa="isActive: false" not in r,
                        filtro=(re.search(r"crossFilteringBehavior: (.+)", r) or [None, "oneDirection"])[1]))
    return out

# Grupos del catálogo = carpetas de visualización (displayFolder) de las medidas
def grupo(m):
    return m["carpeta"] or "Sin carpeta"

def esc(x): return (x or "").replace("|", "\\|").replace("\n", " ")

def ancla(g): return re.sub(r"[^a-z0-9áéíóúñü _-]", "", g.lower()).replace(" ", "-")

PARAM_DESC = {
    "RangeStart": "Inicio del rango de carga en Desktop (en el servicio lo fija la actualización incremental). Usar 01-ene-2008 00:00 para tener el histórico completo.",
    "RangeEnd": "Fin del rango de carga en Desktop, exclusivo. Una fecha futura (p. ej. 2030) carga hasta el último dato.",
    "InicioAnioHidrologico": "Fecha de referencia del inicio del año hidrológico (se usa el mes: noviembre).",
    "fxLecturasEstacion_met_diario": "Resumen diario de una estación (endpoint /ws/getlecturasdia).",
    "fxLimpiarDiario": "Control de calidad: valores diarios fuera de rango → nulo (límites editables dentro de la función).",
}

def gen_diccionario(T, R, E, fecha):
    L = ["# Diccionario de datos\n", f"> Generado automáticamente por `tools/generar_docs_modelo.py` el {fecha}. No editar a mano: los cambios se pierden al regenerar.\n",
         "## Parámetros y funciones de Power Query\n", "| Nombre | Descripción | Definición |", "|---|---|---|"]
    for n, d, e in E:
        if e.lstrip().startswith("(") or "=>" in e.split("\n")[0]:
            L.append(f"| `{n}` | {PARAM_DESC.get(n) or esc(d)} | Función (ver `expressions.tmdl`) |")
        else:
            L.append(f"| `{n}` | {PARAM_DESC.get(n) or esc(d)} | `{esc(e.split(' meta ')[0])}` |")
    L += ["\n## Actualización incremental\n", "| Tabla | Ventana de historia | Se refresca en cada actualización |", "|---|---|---|"]
    for n, t in T.items():
        p = t["politica"]
        if p:
            L.append(f"| `{n}` | {p.get('rollingWindowPeriods')} {'años' if p.get('rollingWindowGranularity') == 'year' else p.get('rollingWindowGranularity')} | "
                     f"últimos {p.get('incrementalPeriods')} {dict(day='días', month='meses', year='años').get(p.get('incrementalGranularity'), p.get('incrementalGranularity'))} |")
    L += ["\n## Relaciones\n", "| Desde (muchos) | Hacia (uno) | Activa | Filtro |", "|---|---|---|---|"]
    for r in R:
        L.append(f"| `{r['desde']}` | `{r['hacia']}` | {'Sí' if r['activa'] else '**No** (inactiva)'} | {'ambas direcciones' if r['filtro'] == 'bothDirections' else 'una dirección'} |")
    L.append("\n## Tablas\n")
    for n, t in T.items():
        if n == "_Medidas": continue
        etiq = [x for x in ["tabla de fechas marcada" if t["fecha"] else "", "actualización incremental" if t["politica"] else ""] if x]
        L.append(f"### `{n}`" + (f" — {', '.join(etiq)}" if etiq else "") + "\n")
        L += ["| Columna | Tipo | Formato | Ordenar por | Notas |", "|---|---|---|---|---|"]
        for c in t["columnas"]:
            notas = ", ".join(x for x in ["clave" if c["clave"] else "", "oculta" if c["oculta"] else ""] if x)
            L.append(f"| `{c['nombre']}` | {c['tipo']} | {esc(c['fmt'])} | {('`' + c['orden'] + '`') if c['orden'] else ''} | {notas} |")
        for h, niv in t["jerarquias"]:
            L.append(f"\n**Jerarquía `{h}`:** " + " → ".join(f"{a} (`{b}`)" for a, b in niv))
        if t["fuente"]:
            dax = not t["fuente"].lstrip().startswith("let")
            L += [f"\n<details><summary>{'Expresión DAX (tabla calculada)' if dax else 'Consulta de Power Query (M)'}</summary>\n",
                  "```dax" if dax else "```powerquery", t["fuente"], "```", "</details>\n"]
        L.append("")
    return "\n".join(L)

def gen_catalogo(T, fecha):
    ms = [m for t in T.values() for m in t["medidas"]]; por = {}
    for m in ms: por.setdefault(grupo(m), []).append(m)
    L = ["# Catálogo de medidas DAX\n", f"> Generado automáticamente por `tools/generar_docs_modelo.py` el {fecha} ({len(ms)} medidas). No editar a mano.\n",
         "Convenciones: las medidas con prefijo `_` son auxiliares. Con varias estaciones, las variables acumulativas "
         "(precipitación, ETo, balance, radiación) **suman por estación y luego promedian entre estaciones**; los promedios se calculan "
         "por estación y luego entre estaciones; las temperaturas máxima y mínima mensuales son el extremo de cada estación, promediado. "
         "Las medidas que dependen de la variable usan `Var_Sel` (tabla `Variables`). Ver `01_arquitectura.md` y `06_decisiones_y_cambios.md`.\n",
         "## Índice\n"]
    orden = sorted(por)
    for g in orden: L.append(f"- [{g}](#{ancla(g)}) ({len(por[g])})")
    for g in orden:
        L += [f"\n## {g}\n", "| Medida | Formato | Descripción |", "|---|---|---|"]
        for m in por[g]:
            fmt = esc(m["fmt"]) + (" · URL de imagen" if m["cat"] == "ImageUrl" else "")
            L.append(f"| `{m['nombre']}` | {fmt} | {esc(m['desc'])} |")
        for m in por[g]:
            L += [f"\n<details><summary><code>{m['nombre']}</code></summary>\n", "```dax", m["expr"], "```", "</details>"]
    return "\n".join(L)

def gen_visuales(fecha):
    orden = json.load(open(os.path.join(PAGS, "pages.json"), encoding="utf-8"))["pageOrder"]
    L = ["# Inventario de páginas y visuales\n", f"> Generado automáticamente por `tools/generar_docs_modelo.py` el {fecha}. No editar a mano.\n"]
    for pid in orden:
        pj = json.load(open(os.path.join(PAGS, pid, "page.json"), encoding="utf-8"))
        vis = []
        for vf in glob.glob(os.path.join(PAGS, pid, "visuals", "*", "visual.json")):
            d = json.load(open(vf, encoding="utf-8")); v = d.get("visual", {})
            tit = None
            for a, b in (("visualContainerObjects", "title"), ("objects", "header")):
                try:
                    e = v[a][b][0]["properties"]["text"]["expr"]
                    tit = e["Literal"]["Value"].strip("'") if "Literal" in e else "[" + e["Measure"]["Property"] + "]"
                except Exception: pass
                if tit: break
            tipo_v = "Deneb (Vega-Lite)" if str(v.get("visualType", "")).startswith("deneb") else v.get("visualType")
            campos = [p["queryRef"].split(".", 1)[-1] for w in v.get("query", {}).get("queryState", {}).values() for p in w["projections"]]
            pos = d.get("position", {})
            vis.append((round(pos.get("y", 0)), pos.get("x", 0), tipo_v, tit, d["name"], campos))
        vis.sort()
        L += [f"## {pj['displayName'].strip()}" + (" (oculta)" if pj.get("visibility") == "HiddenInViewMode" else "") + "\n", f"Tamaño {pj.get('width')}×{pj.get('height')} · {len(vis)} visuales · carpeta `{pid}`\n",
              "| Visual | Título | Campos | ID |", "|---|---|---|---|"]
        for y, x, tipo, tit, vid, campos in vis:
            if not campos: continue
            L.append(f"| {tipo} | {esc(tit)} | {esc(', '.join(campos))} | `{vid[:6]}` |")
        L.append("")
    return "\n".join(L)

if __name__ == "__main__":
    fecha = datetime.date.today().isoformat()
    T, R, E = tablas(), relaciones(), expresiones()
    os.makedirs(DOCS, exist_ok=True)
    for nombre, contenido in [("02_diccionario_datos.md", gen_diccionario(T, R, E, fecha)),
                              ("03_catalogo_medidas.md", gen_catalogo(T, fecha)),
                              ("09_inventario_visuales.md", gen_visuales(fecha))]:
        with open(os.path.join(DOCS, nombre), "w", encoding="utf-8", newline="\n") as f:
            f.write(contenido + "\n")
        print("OK", nombre)
