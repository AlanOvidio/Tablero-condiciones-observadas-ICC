# Diccionario de datos

> Generado automáticamente por `tools/generar_docs_modelo.py` el 2026-11-13. No editar a mano: los cambios se pierden al regenerar.

## Parámetros y funciones de Power Query

| Nombre | Descripción | Definición |
|---|---|---|
| `RangeStart` | Inicio del rango de carga en Desktop (en el servicio lo fija la actualización incremental). Usar 01-ene-2008 00:00 para tener el histórico completo. | `#datetime(2008, 1, 1, 0, 0, 0)` |
| `RangeEnd` | Fin del rango de carga en Desktop, exclusivo. Una fecha futura (p. ej. 2030) carga hasta el último dato. | `#datetime(2026, 11, 9, 0, 0, 0)` |
| `InicioAnioHidrologico` | Fecha de referencia del inicio del año hidrológico (se usa el mes: noviembre). | `#date(2025, 11, 1)` |
| `fxLecturasEstacion_met_diario` | Resumen diario de una estación (endpoint /ws/getlecturasdia). | Función (ver `expressions.tmdl`) |
| `fxLimpiarDiario` | Control de calidad: valores diarios fuera de rango → nulo (límites editables dentro de la función). | Función (ver `expressions.tmdl`) |

## Actualización incremental

| Tabla | Ventana de historia | Se refresca en cada actualización |
|---|---|---|
| `Fact_Diaria_met` | 19 años | últimos 7 días |
| `Fact_Mensual_met` | 19 años | últimos 2 meses |

## Relaciones

| Desde (muchos) | Hacia (uno) | Activa | Filtro |
|---|---|---|---|
| `Fact_Diaria_met.Fecha` | `Calendario.Fecha` | Sí | una dirección |
| `Fact_Diaria_met.estacionid` | `Estaciones_met.estacionid` | Sí | una dirección |
| `Fact_Mensual_met.estacionid` | `Estaciones_met.estacionid` | Sí | una dirección |

## Tablas

### `Anio_Sel`

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `Año` | int64 | 0 |  |  |

<details><summary>Expresión DAX (tabla calculada)</summary>

```dax
SELECTCOLUMNS ( GENERATESERIES ( 2008, YEAR ( TODAY () ), 1 ), "Año", [Value] )
```
</details>


### `Anios_Base`

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `Año` | int64 | 0 |  |  |

<details><summary>Expresión DAX (tabla calculada)</summary>

```dax
SELECTCOLUMNS ( GENERATESERIES ( 2008, YEAR ( TODAY () ), 1 ), "Año", [Value] )
```
</details>


### `Anios_Comparacion`

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `Año` | int64 | 0 |  |  |

<details><summary>Expresión DAX (tabla calculada)</summary>

```dax
DISTINCT ( SELECTCOLUMNS ( Calendario, "Año", Calendario[Anio] ) )
```
</details>


### `Calendario` — tabla de fechas marcada

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `Fecha` | dateTime | dd-mmm-yy |  | clave |
| `Anio` | int64 | 0 |  |  |
| `Mes_Num` | int64 | 0 |  | oculta |
| `Mes` | string |  | `Mes_Num` |  |
| `Mes_Anio` | string |  | `Mes_Anio_Num` |  |
| `Mes_Anio_Num` | int64 | 0 |  | oculta |
| `Fecha_Mes` | dateTime | mmm yyyy |  |  |
| `Dia_Juliano` | int64 | 0 |  |  |
| `Pentada` | int64 | 0 |  |  |
| `Pentada_Anio` | string |  | `Pentada_Anio_Num` |  |
| `Pentada_Anio_Num` | int64 | 0 |  | oculta |
| `Inicio_Semana` | dateTime | Long Date |  |  |
| `Anio_Hidrologico` | int64 | 0 |  |  |
| `Fecha_Corta` | string |  |  |  |
| `Trimestre` | string |  |  |  |
| `Dia` | int64 | 0 |  |  |
| `Fecha_Larga` | string |  | `Fecha` |  |
| `Fecha_Abrev` | string |  | `Fecha` |  |

**Jerarquía `Jerarquía de fechas`:** Año (`Anio`) → Trimestre (`Trimestre`) → Mes (`Mes`) → Día (`Dia`)

<details><summary>Consulta de Power Query (M)</summary>

```powerquery
let
    FechaInicio = #date(2008, 1, 1),
    // Hasta el 31-dic del año en curso (hora de Guatemala) para que los ejes mensuales muestren el año completo
    FechaFin    = Date.EndOfYear(Date.From(DateTimeZone.SwitchZone(DateTimeZone.UtcNow(), -6))),
    MesInicioHidro = Date.Month(InicioAnioHidrologico),
    MesesAbrev = {"Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"},
    Lista = List.Dates(FechaInicio, Duration.Days(FechaFin - FechaInicio) + 1, #duration(1, 0, 0, 0)),
    Tabla = Table.FromList(Lista, Splitter.SplitByNothing(), {"Fecha"}),
    TipoFecha = Table.TransformColumnTypes(Tabla, {{"Fecha", type date}}),
    Anio = Table.AddColumn(TipoFecha, "Anio", each Date.Year([Fecha]), Int64.Type),
    Mes = Table.AddColumn(Anio, "Mes_Num", each Date.Month([Fecha]), Int64.Type),
    MesAbrev = Table.AddColumn(Mes, "Mes", each MesesAbrev{[Mes_Num] - 1}, type text),
    MesAnio = Table.AddColumn(MesAbrev, "Mes_Anio", each MesesAbrev{[Mes_Num] - 1} & " " & Text.From([Anio]), type text),
    MesAnioNum = Table.AddColumn(MesAnio, "Mes_Anio_Num", each [Anio] * 100 + [Mes_Num], Int64.Type),
    FechaMes = Table.AddColumn(MesAnioNum, "Fecha_Mes", each Date.StartOfMonth([Fecha]), type date),
    DiaJuliano = Table.AddColumn(FechaMes, "Dia_Juliano", each Date.DayOfYear([Fecha]), Int64.Type),
    Pentada = Table.AddColumn(DiaJuliano, "Pentada", each List.Min({Number.RoundUp([Dia_Juliano] / 5), 73}), Int64.Type),
    PentadaAnio = Table.AddColumn(Pentada, "Pentada_Anio", each "P" & Text.PadStart(Text.From([Pentada]), 2, "0") & " " & Text.From([Anio]), type text),
    PentadaAnioNum = Table.AddColumn(PentadaAnio, "Pentada_Anio_Num", each [Anio] * 100 + [Pentada], Int64.Type),
    InicioSemana = Table.AddColumn(PentadaAnioNum, "Inicio_Semana", each Date.StartOfWeek([Fecha], Day.Monday), type date),
    // Año hidrológico por mes (nov–oct): noviembre de 2025 pertenece al año hidrológico 2026
    AnioHidro = Table.AddColumn(InicioSemana, "Anio_Hidrologico", each if [Mes_Num] >= MesInicioHidro then [Anio] + 1 else [Anio], Int64.Type),
    FechaCorta = Table.AddColumn(AnioHidro, "Fecha_Corta", each Date.ToText([Fecha], "dd-MMM", "es-GT"), type text),
    // Niveles de la jerarquía de fechas
    Trimestre = Table.AddColumn(FechaCorta, "Trimestre", each "T" & Text.From(Date.QuarterOfYear([Fecha])), type text),
    Dia = Table.AddColumn(Trimestre, "Dia", each Date.Day([Fecha]), Int64.Type),
    // Representaciones de texto de la fecha (la columna Fecha no se modifica)
    FechaLarga = Table.AddColumn(Dia, "Fecha_Larga", each Text.From(Date.Day([Fecha])) & " " & Date.ToText([Fecha], "MMMM", "es-GT") & ", " & Text.From(Date.Year([Fecha])), type text),
    FechaAbrev = Table.AddColumn(FechaLarga, "Fecha_Abrev", each Text.From(Date.Day([Fecha])) & "-" & Text.Lower(MesesAbrev{[Mes_Num] - 1}) & "-" & Text.From(Date.Year([Fecha])), type text)
in
    FechaAbrev
```
</details>


### `Capas`

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `Capa` | string |  | `Orden` |  |
| `Orden` | int64 | 0 |  | oculta |

<details><summary>Expresión DAX (tabla calculada)</summary>

```dax
DATATABLE (
    "Capa", STRING, "Orden", INTEGER,
    {
        {"Año actual", 1},
        {"Media histórica", 2},
        {"Rango histórico (mín–máx)", 3},
        {"Rango normal (P33–P66)", 4},
        {"Años adicionales", 5},
        {"Anomalías", 6}
    }
)
```
</details>


### `Cuencas_met`

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `Clave` | string |  |  |  |
| `Cuenca` | string |  |  |  |

<details><summary>Consulta de Power Query (M)</summary>

```powerquery
let
    // Fuente heredada (Excel de 2020). Se une a Estaciones_met por nombre normalizado.
    Origen = SharePoint.Files("https://asazgua.sharepoint.com/sites/DataPowerBI/", [ApiVersion = 15]),
    Archivo = Origen{[Name = "Meteorologicas_10062020.xlsx", #"Folder Path" = "https://asazgua.sharepoint.com/sites/DataPowerBI/Documentos compartidos/"]}[Content],
    Hoja = Excel.Workbook(Archivo){[Item = "Hoja2", Kind = "Sheet"]}[Data],
    Encabezados = Table.PromoteHeaders(Hoja, [PromoteAllScalars = true]),
    Clave = Table.AddColumn(Encabezados, "Clave", each Text.Lower(Text.Trim(Text.From([Estación]))), type text),
    Sel = Table.SelectColumns(Clave, {"Clave", "Cuenca"}),
    Tipos = Table.TransformColumnTypes(Sel, {{"Cuenca", type text}}),
    SinVacios = Table.SelectRows(Tipos, each [Clave] <> null and [Clave] <> ""),
    Unicos = Table.Distinct(SinVacios, {"Clave"})
in
    Unicos
```
</details>


### `Dias_Periodo`

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `Día` | int64 | 0 |  |  |

<details><summary>Expresión DAX (tabla calculada)</summary>

```dax
SELECTCOLUMNS ( GENERATESERIES ( 1, 366, 1 ), "Día", [Value] )
```
</details>


### `Estaciones_met`

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `estacionid` | int64 | 0 |  | oculta |
| `Código` | string |  |  |  |
| `Estación` | string |  |  |  |
| `País` | string |  |  |  |
| `Estrato` | string |  | `Orden_Estrato` |  |
| `Región climática` | string |  | `Orden_Region` |  |
| `Latitud` | double |  |  |  |
| `Longitud` | double |  |  |  |
| `Altitud` | int64 | 0 |  |  |
| `Activa` | int64 | 0 |  | oculta |
| `Redmet` | int64 | 0 |  | oculta |
| `Orden_Region` | int64 | 0 |  | oculta |
| `Orden_Estrato` | int64 | 0 |  | oculta |
| `Cuenca =` | string |  |  |  |
| `Excluir_Agregados` | int64 | 0 |  |  |
| `Tipo` | string |  |  |  |

<details><summary>Consulta de Power Query (M)</summary>

```powerquery
let
    Origen = Json.Document(Web.Contents(
        "https://redmet.icc.org.gt/ws/redmet/estaciones",
        [Headers = [Accept = "Application/json"]]
    )),
    Tabla = Table.FromList(Origen[estaciones], Splitter.SplitByNothing(), {"r"}),
    Expandir = Table.ExpandRecordColumn(Tabla, "r",
        {"estacionid", "codigo", "finca", "latitud", "longitud", "altitud", "activa", "redmet", "pais", "estrato"}),
    ExpPais = Table.ExpandRecordColumn(Expandir, "pais", {"nombre"}, {"País"}),
    ExpEstrato = Table.ExpandRecordColumn(ExpPais, "estrato", {"nombre"}, {"Estrato"}),
    Tipos = Table.TransformColumnTypes(ExpEstrato, {
        {"estacionid", Int64.Type}, {"codigo", type text}, {"finca", type text},
        {"latitud", type number}, {"longitud", type number}, {"altitud", Int64.Type},
        {"activa", Int64.Type}, {"redmet", Int64.Type}, {"País", type text}, {"Estrato", type text}
    }),
    // Solo las estaciones de TablaEstaciones_met
    Seleccion = Table.SelectRows(Tipos, each List.Contains(TablaEstaciones_met[estacionid], [estacionid])),

    // Región climática: spatial join con regiones_gcs_wgs_1984.shp (tools/generar_regiones.R).
    // Bloque generado desde config/estaciones_region.csv: no editar a mano.
    Regiones = #table(type table [estacionid = Int64.Type, Region = text], {
        // <regiones>
        {38, "Montañosa (SV)"},
        {47, "Montañosa (SV)"},
        {45, "Pacífico (SV)"},
        {39, "Pacífico (SV)"},
        {40, "Pacífico (SV)"},
        {46, "Pacífico (SV)"},
        {79, "Pacífico (SV)"},
        {78, "Pacífico (SV)"},
        {103, "Pacífico (SV)"},
        {80, "Pacífico (SV)"},
        {3, "Altiplano Central"},
        {67, "Altiplano Central"},
        {94, "Altiplano Central"},
        {36, "Altiplano Central"},
        {74, "Altiplano Central"},
        {32, "Bocacosta"},
        {91, "Bocacosta"},
        {6, "Bocacosta"},
        {1, "Bocacosta"},
        {105, "Bocacosta"},
        {31, "Bocacosta"},
        {33, "Bocacosta"},
        {21, "Bocacosta"},
        {83, "Bocacosta"},
        {17, "Bocacosta"},
        {82, "Bocacosta"},
        {14, "Bocacosta"},
        {92, "Bocacosta"},
        {84, "Bocacosta"},
        {69, "Bocacosta"},
        {16, "Bocacosta"},
        {96, "Bocacosta"},
        {98, "Bocacosta"},
        {97, "Bocacosta"},
        {24, "Bocacosta"},
        {85, "Bocacosta"},
        {2, "Bocacosta"},
        {22, "Bocacosta"},
        {25, "Bocacosta"},
        {99, "Bocacosta"},
        {100, "Bocacosta"},
        {102, "Bocacosta"},
        {37, "Bocacosta"},
        {95, "Caribe"},
        {30, "Pacífico"},
        {20, "Pacífico"},
        {35, "Pacífico"},
        {4, "Pacífico"},
        {88, "Pacífico"},
        {28, "Pacífico"},
        {12, "Pacífico"},
        {68, "Pacífico"},
        {7, "Pacífico"},
        {23, "Pacífico"},
        {27, "Pacífico"},
        {87, "Pacífico"},
        {81, "Pacífico"},
        {26, "Pacífico"},
        {75, "Pacífico"},
        {34, "Pacífico"},
        {93, "Pacífico"},
        {86, "Pacífico"},
        {77, "Pacífico"},
        {42, "Pacífico"},
        {101, "Pacífico"},
        {106, "Pacífico"},
        {107, "Pacífico"},
        {73, "Pacífico"},
        {15, "Pacífico"},
        {13, "Pacífico"},
        {44, "Pacífico"},
        {29, "Pacífico"},
        {8, "Pacífico"},
        {76, "Pacífico"},
        {90, "Pacífico"},
        {9, "Pacífico"},
        {19, "Pacífico"},
        {18, "Pacífico"},
        {89, "Pacífico"},
        {5, "Pacífico"},
        {43, "Pacífico"},
        {10, "Pacífico"},
        {11, "Pacífico"},
        {50, "Sin región"},
        {53, "Sin región"},
        {51, "Sin región"},
        {49, "Sin región"},
        {54, "Sin región"},
        {52, "Sin región"},
        {48, "Sin región"},
        {66, "Sin región"},
        {61, "Sin región"},
        {60, "Sin región"},
        {58, "Sin región"},
        {62, "Sin región"},
        {59, "Sin región"},
        {65, "Sin región"},
        {56, "Sin región"},
        {57, "Sin región"},
        {64, "Sin región"},
        {63, "Sin región"}
        // </regiones>
    }),
    UnirRegion = Table.NestedJoin(Seleccion, {"estacionid"}, Regiones, {"estacionid"}, "R", JoinKind.LeftOuter),
    ExpRegion = Table.ExpandTableColumn(UnirRegion, "R", {"Region"}, {"RegionCSV"}),
    // Estaciones sin región en el CSV: El Salvador usa el estrato (como script_nuevo.R)
    Region = Table.AddColumn(ExpRegion, "Región climática", each
        if [RegionCSV] <> null then [RegionCSV]
        else if [País] = "El Salvador" then
            (if List.Contains({"Litoral", "Bajo"}, [Estrato]) then "Pacífico (SV)" else "Montañosa (SV)")
        else "Sin región", type text),
    OrdenRegion = Table.AddColumn(Region, "Orden_Region", each
        let p = List.PositionOf({"Pacífico", "Bocacosta", "Altiplano Central", "Pacífico (SV)", "Montañosa (SV)"}, [Región climática])
        in if p < 0 then 99 else p + 1, Int64.Type),
    OrdenEstrato = Table.AddColumn(OrdenRegion, "Orden_Estrato", each
        let p = List.PositionOf({"Litoral", "Bajo", "Medio", "Alto"}, [Estrato])
        in if p < 0 then 99 else p + 1, Int64.Type),
    Renombrar = Table.RenameColumns(OrdenEstrato, {
        {"codigo", "Código"}, {"finca", "Estación"}, {"latitud", "Latitud"},
        {"longitud", "Longitud"}, {"altitud", "Altitud"}, {"activa", "Activa"}, {"redmet", "Redmet"}
    }),
    SinCSV = Table.RemoveColumns(Renombrar, {"RegionCSV"}),
    // 1 = se excluye de las agregaciones (lista ExcluirAgregados de TablaEstaciones_met)
    ConTipo = Table.AddColumn(SinCSV, "Tipo", each if List.Contains(Table.SelectRows(TablaEstaciones_met, each [Tipo] = "B")[estacionid], [estacionid]) then "B" else "A", type text),
    Final = Table.AddColumn(ConTipo, "Excluir_Agregados", each if List.Contains(Table.SelectRows(TablaEstaciones_met, each [Excluir_Agregados] = 1)[estacionid], [estacionid]) then 1 else 0, Int64.Type)
in
    Final
```
</details>


### `Fact_Diaria_met` — actualización incremental

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `estacionid` | int64 | 0 |  | oculta |
| `Fecha` | dateTime | Long Date |  |  |
| `Temp_Media` | double | 0.0 |  |  |
| `Temp_Min` | double | 0.0 |  |  |
| `Temp_Max` | double | 0.0 |  |  |
| `Precip_Total` | double | 0.0 |  |  |
| `ETO_Total` | double | 0.0 |  |  |
| `Balance_Hidrico` | double | 0.0 |  |  |
| `Rad_Total` | double | 0 |  | oculta |
| `Rad_MJ` | double | 0.00 |  |  |
| `Irradiancia_Diurna` | double | 0 |  |  |
| `IC_Media` | double | 0.0 |  |  |
| `IC_Max` | double | 0.0 |  |  |
| `IC_Min` | double | 0.0 |  |  |
| `Excluir_Agregados` | int64 | 0 |  |  |
| `Tipo` | string |  |  |  |

<details><summary>Consulta de Power Query (M)</summary>

```powerquery
let
    Fuente = TablaEstaciones_met,
    EjecutarAPI = Table.AddColumn(Fuente, "Lecturas", each fxLecturasEstacion_met_diario([estacionid], RangeStart, RangeEnd)),
    ExpandirLista = Table.ExpandListColumn(EjecutarAPI, "Lecturas"),
    QuitarVacias = Table.SelectRows(ExpandirLista, each [Lecturas] <> null),
    ExpandirCampos = Table.ExpandRecordColumn(QuitarVacias, "Lecturas",
        {"dia", "tempavg", "tempmin", "tempmax", "radiaciontotal", "lluviasum", "etosum", "indicecaloravg", "indicecalormin", "indicecalormax"},
        {"Fecha", "Temp_Media", "Temp_Min", "Temp_Max", "Rad_Total", "Precip_Total", "ETO_Total", "IC_Media", "IC_Min", "IC_Max"}),
    EtoTexto = Table.TransformColumnTypes(ExpandirCampos, {{"ETO_Total", type text}}),
    EtoVacio = Table.ReplaceValue(EtoTexto, "", null, Replacer.ReplaceValue, {"ETO_Total"}),
    Tipos = Table.TransformColumnTypes(EtoVacio, {
        {"estacionid", Int64.Type}, {"Fecha", type date}, {"Temp_Media", type number}, {"Temp_Min", type number},
        {"Temp_Max", type number}, {"Rad_Total", type number}, {"Precip_Total", type number}, {"ETO_Total", type number},
        {"IC_Media", type number}, {"IC_Min", type number}, {"IC_Max", type number}
    }),
    // Control de calidad: valores fuera de rango → nulo (límites en fxLimpiarDiario)
    Limpio = fxLimpiarDiario(Tipos),
    Incremental = Table.SelectRows(Limpio, each
        [Fecha] >= Date.From(List.Max({RangeStart, #datetime(2008, 1, 1, 0, 0, 0)})) and
        [Fecha] < Date.From(RangeEnd)),
    // Energía diaria (MJ/m²) = Σ lecturas de 15 min (W/m²) × 900 s / 10⁶
    RadMJ = Table.AddColumn(Incremental, "Rad_MJ", each [Rad_Total] * 900 / 1000000, type number),
    // Irradiancia diurna media (W/m²) = Σ lecturas / 52 (06:00–18:59, como los scripts R)
    Irradiancia = Table.AddColumn(RadMJ, "Irradiancia_Diurna", each [Rad_Total] / 52, type number),
    // Balance hídrico diario: nulo si falta la ETo
    Balance = Table.AddColumn(Irradiancia, "Balance_Hidrico", each [Precip_Total] - [ETO_Total], type number)
in
    Balance
```
</details>


### `Fact_Mensual_met` — actualización incremental

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `estacionid` | int64 | 0 |  | oculta |
| `Anio` | int64 | 0 |  |  |
| `Mes` | int64 | 0 |  |  |
| `Fecha_Mes` | dateTime | mmm yyyy |  |  |
| `Dias_Mes` | int64 | 0 |  | oculta |
| `N_Dias` | int64 | 0 |  |  |
| `Precip` | double | 0.0 |  |  |
| `ETo` | double | 0.0 |  |  |
| `N_Dias_ETo` | int64 | 0 |  | oculta |
| `Rad_MJ` | double | 0.0 |  |  |
| `Irradiancia` | double | 0 |  |  |
| `Temp_Media` | double | 0.0 |  |  |
| `Temp_Max_Abs` | double | 0.0 |  |  |
| `Temp_Min_Abs` | double | 0.0 |  |  |
| `IC_Max` | double | 0.0 |  |  |
| `BH` | double | 0.0 |  |  |
| `ETo_Dia` | double | 0.0 |  |  |
| `Completitud` | double | 0% |  |  |
| `Mes_Completo` | boolean |  |  |  |
| `Mes_Valido` | boolean |  |  |  |
| `IC_Media` | double | 0.0 |  |  |
| `IC_Min_Abs` | double | 0.0 |  |  |
| `Mes_Preliminar` | boolean | """TRUE"";""TRUE"";""FALSE""" |  |  |

<details><summary>Consulta de Power Query (M)</summary>

```powerquery
let
    Fuente = TablaEstaciones_met,
    EjecutarAPI = Table.AddColumn(Fuente, "Lecturas", each fxLecturasEstacion_met_diario([estacionid], RangeStart, RangeEnd)),
    ExpandirLista = Table.ExpandListColumn(EjecutarAPI, "Lecturas"),
    QuitarVacias = Table.SelectRows(ExpandirLista, each [Lecturas] <> null),
    ExpandirCampos = Table.ExpandRecordColumn(QuitarVacias, "Lecturas",
        {"dia", "tempavg", "tempmin", "tempmax", "radiaciontotal", "lluviasum", "etosum", "indicecaloravg", "indicecalormin", "indicecalormax"},
        {"Fecha", "Temp_Media", "Temp_Min", "Temp_Max", "Rad_Total", "Precip_Total", "ETO_Total", "IC_Media", "IC_Min", "IC_Max"}),
    // ETo puede llegar como texto vacío: se deja nulo (no 0)
    EtoTexto = Table.TransformColumnTypes(ExpandirCampos, {{"ETO_Total", type text}}),
    EtoVacio = Table.ReplaceValue(EtoTexto, "", null, Replacer.ReplaceValue, {"ETO_Total"}),
    Tipos = Table.TransformColumnTypes(EtoVacio, {
        {"estacionid", Int64.Type}, {"Fecha", type date}, {"Temp_Media", type number}, {"Temp_Min", type number},
        {"Temp_Max", type number}, {"Rad_Total", type number}, {"Precip_Total", type number}, {"ETO_Total", type number},
        {"IC_Media", type number}, {"IC_Min", type number}, {"IC_Max", type number}
    }),
    // Control de calidad: valores fuera de rango → nulo (límites en fxLimpiarDiario)
    Limpio = fxLimpiarDiario(Tipos),
    // Filtro de actualización incremental (particiones por mes: un mes nunca queda partido)
    Incremental = Table.SelectRows(Limpio, each
        [Fecha] >= Date.From(List.Max({RangeStart, #datetime(2008, 1, 1, 0, 0, 0)})) and
        [Fecha] < Date.From(RangeEnd)),
    Anio = Table.AddColumn(Incremental, "Anio", each Date.Year([Fecha]), Int64.Type),
    Mes = Table.AddColumn(Anio, "Mes", each Date.Month([Fecha]), Int64.Type),
    // Día → mes por estación (como mensual_por_estacion() de los scripts R)
    Mensual = Table.Group(Mes, {"estacionid", "Anio", "Mes"}, {
        {"N_Dias", each Table.RowCount(_), Int64.Type},
        // Días con dato por variable (completitud de cada variable, no solo de filas)
        {"N_P", each List.Count(List.RemoveNulls([Precip_Total])), Int64.Type},
        {"N_T", each List.Count(List.RemoveNulls([Temp_Media])), Int64.Type},
        {"N_Tx", each List.Count(List.RemoveNulls([Temp_Max])), Int64.Type},
        {"N_Tn", each List.Count(List.RemoveNulls([Temp_Min])), Int64.Type},
        {"N_R", each List.Count(List.RemoveNulls([Rad_Total])), Int64.Type},
        {"N_IC", each List.Count(List.RemoveNulls([IC_Media])), Int64.Type},
        {"N_ICx", each List.Count(List.RemoveNulls([IC_Max])), Int64.Type},
        {"N_ICn", each List.Count(List.RemoveNulls([IC_Min])), Int64.Type},
        {"Precip", each List.Sum([Precip_Total]), type nullable number},
        {"ETo", each List.Sum([ETO_Total]), type nullable number},
        {"N_Dias_ETo", each List.Count(List.RemoveNulls([ETO_Total])), Int64.Type},
        // Energía (MJ/m²) = Σ lecturas de 15 min (W/m²) × 900 s / 10⁶
        {"Rad_MJ", each List.Sum([Rad_Total]) * 900 / 1000000, type nullable number},
        // Irradiancia diurna media (W/m²) = Σ W/m² del día / 52 lecturas (06:00–18:59)
        {"Irradiancia", each List.Average([Rad_Total]) / 52, type nullable number},
        {"Temp_Media", each List.Average([Temp_Media]), type nullable number},
        {"Temp_Max_Abs", each List.Max([Temp_Max]), type nullable number},
        {"Temp_Min_Abs", each List.Min([Temp_Min]), type nullable number},
        {"IC_Media", each List.Average([IC_Media]), type nullable number},
        {"IC_Max", each List.Max([IC_Max]), type nullable number},
        {"IC_Min_Abs", each List.Min([IC_Min]), type nullable number}
    }),
    Hoy = Date.From(DateTimeZone.SwitchZone(DateTimeZone.UtcNow(), -6)),
    FechaMes = Table.AddColumn(Mensual, "Fecha_Mes", each #date([Anio], [Mes], 1), type date),
    DiasMes = Table.AddColumn(FechaMes, "Dias_Mes", each Date.DaysInMonth([Fecha_Mes]), Int64.Type),
    // Días de referencia: el mes completo si ya cerró; si está en curso, los días transcurridos (dato preliminar)
    DiasRef = Table.AddColumn(DiasMes, "Dias_Ref", each if Date.EndOfMonth([Fecha_Mes]) < Hoy then [Dias_Mes] else List.Max({1, Duration.Days(Hoy - [Fecha_Mes])}), Int64.Type),
    // Valor mensual solo si la variable tiene dato en ≥ 80 % de los días de referencia; si no, nulo
    UmbralCompletitud = 0.8,
    Reglas = {{"Precip", "N_P"}, {"ETo", "N_Dias_ETo"}, {"Rad_MJ", "N_R"}, {"Irradiancia", "N_R"},
              {"Temp_Media", "N_T"}, {"Temp_Max_Abs", "N_Tx"}, {"Temp_Min_Abs", "N_Tn"},
              {"IC_Media", "N_IC"}, {"IC_Max", "N_ICx"}, {"IC_Min_Abs", "N_ICn"}},
    PorVariable = List.Accumulate(Reglas, DiasRef, (tb, r) =>
        Table.ReplaceValue(tb, each Record.Field(_, r{0}),
            each if Record.Field(_, r{1}) >= UmbralCompletitud * [Dias_Ref] then Record.Field(_, r{0}) else null,
            Replacer.ReplaceValue, {r{0}})),
    SinConteos = Table.RemoveColumns(PorVariable, {"N_P", "N_T", "N_Tx", "N_Tn", "N_R", "N_IC", "N_ICx", "N_ICn"}),
    // Table.ReplaceValue deja las columnas sin tipo: se vuelven a tipar como número
    Tipado = Table.TransformColumnTypes(SinConteos, List.Transform(
        {"Precip", "ETo", "Rad_MJ", "Irradiancia", "Temp_Media", "Temp_Max_Abs", "Temp_Min_Abs", "IC_Media", "IC_Max", "IC_Min_Abs"},
        (c) => {c, type number})),
    BH = Table.AddColumn(Tipado, "BH", each if [ETo] <> null and [Precip] <> null then [Precip] - [ETo] else null, type nullable number),
    EToDia = Table.AddColumn(BH, "ETo_Dia", each if [ETo] <> null then [ETo] / [N_Dias_ETo] else null, type nullable number),
    Completitud = Table.AddColumn(EToDia, "Completitud", each [N_Dias] / [Dias_Mes], type number),
    // Mes cerrado: terminó antes de hoy (hora de Guatemala). Válido: ≥ 80 % de días con registro (del mes, o de los días transcurridos si está en curso)
    // (además, cada variable se anula arriba si no alcanza su propia completitud)
    Cerrado = Table.AddColumn(Completitud, "Mes_Completo", each Date.EndOfMonth([Fecha_Mes]) < Hoy, type logical),
    Valido = Table.AddColumn(Cerrado, "Mes_Valido", each if [Mes_Completo] then [Completitud] >= 0.8 else [N_Dias] >= 0.8 * [Dias_Ref], type logical),
    // Mes en curso con datos suficientes: se muestra como preliminar
    Preliminar = Table.AddColumn(Valido, "Mes_Preliminar", each not [Mes_Completo] and [Mes_Valido], type logical),
    Final = Table.RemoveColumns(Preliminar, {"Dias_Ref"})
in
    Final
```
</details>


### `Meses_Acum`

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `Modo` | string |  |  |  |
| `Pos` | int64 | 0 |  | oculta |
| `Mes_Num` | int64 | 0 |  | oculta |
| `Mes_Eje` | string |  | `Pos` |  |
| `Desfase_Anio` | int64 | 0 |  | oculta |

<details><summary>Expresión DAX (tabla calculada)</summary>

```dax
DATATABLE (
    "Modo", STRING, "Pos", INTEGER, "Mes_Num", INTEGER, "Mes_Eje", STRING, "Desfase_Anio", INTEGER,
    {
        {"Año calendario (ene–dic)", 1, 1, "Ene", 0},
        {"Año calendario (ene–dic)", 2, 2, "Feb", 0},
        {"Año calendario (ene–dic)", 3, 3, "Mar", 0},
        {"Año calendario (ene–dic)", 4, 4, "Abr", 0},
        {"Año calendario (ene–dic)", 5, 5, "May", 0},
        {"Año calendario (ene–dic)", 6, 6, "Jun", 0},
        {"Año calendario (ene–dic)", 7, 7, "Jul", 0},
        {"Año calendario (ene–dic)", 8, 8, "Ago", 0},
        {"Año calendario (ene–dic)", 9, 9, "Sep", 0},
        {"Año calendario (ene–dic)", 10, 10, "Oct", 0},
        {"Año calendario (ene–dic)", 11, 11, "Nov", 0},
        {"Año calendario (ene–dic)", 12, 12, "Dic", 0},
        {"Año hidrológico (nov–oct)", 1, 11, "Nov ", 1},
        {"Año hidrológico (nov–oct)", 2, 12, "Dic ", 1},
        {"Año hidrológico (nov–oct)", 3, 1, "Ene ", 0},
        {"Año hidrológico (nov–oct)", 4, 2, "Feb ", 0},
        {"Año hidrológico (nov–oct)", 5, 3, "Mar ", 0},
        {"Año hidrológico (nov–oct)", 6, 4, "Abr ", 0},
        {"Año hidrológico (nov–oct)", 7, 5, "May ", 0},
        {"Año hidrológico (nov–oct)", 8, 6, "Jun ", 0},
        {"Año hidrológico (nov–oct)", 9, 7, "Jul ", 0},
        {"Año hidrológico (nov–oct)", 10, 8, "Ago ", 0},
        {"Año hidrológico (nov–oct)", 11, 9, "Sep ", 0},
        {"Año hidrológico (nov–oct)", 12, 10, "Oct ", 0}
    }
)
```
</details>


### `Metodo_Agregacion`

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `Método` | string |  | `Orden` |  |
| `Orden` | int64 | 0 |  | oculta |

<details><summary>Expresión DAX (tabla calculada)</summary>

```dax
DATATABLE (
    "Método", STRING, "Orden", INTEGER,
    {
        {"Anomalías (tablero)", 1},
        {"Promedio directo (scripts R)", 2}
    }
)
```
</details>


### `Periodo_A`

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `Fecha` | dateTime | dd/mm/yyyy |  |  |

<details><summary>Expresión DAX (tabla calculada)</summary>

```dax
SELECTCOLUMNS ( CALENDAR ( DATE ( 2008, 1, 1 ), TODAY () ), "Fecha", [Date] )
```
</details>


### `Periodo_B`

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `Fecha` | dateTime | dd/mm/yyyy |  |  |

<details><summary>Expresión DAX (tabla calculada)</summary>

```dax
SELECTCOLUMNS ( CALENDAR ( DATE ( 2008, 1, 1 ), TODAY () ), "Fecha", [Date] )
```
</details>


### `TablaEstaciones_met`

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `estacionid` | int64 | 0 |  |  |
| `Solo_Precip` | boolean | """TRUE"";""TRUE"";""FALSE""" |  |  |
| `Excluir_Agregados` | int64 | 0 |  |  |
| `Tipo` | string |  |  |  |

<details><summary>Consulta de Power Query (M)</summary>

```powerquery
let
    // Estaciones que se descargan. AQUÍ se agregan o quitan estaciones.
    Estaciones = {1, 3, 4, 5, 6, 8, 9, 10, 11, 13, 14, 15, 17, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 33, 34, 36, 37, 38, 39, 40, 45, 46, 47, 67, 73, 74, 75, 78, 79, 80, 94, 42, 69, 76, 77, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93},
    // Tipo B (solo se combinan entre ellas en selecciones a mano); el resto es Tipo A (RLS incluidas)
    TipoB = {81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93},
    // Excluidas de las agregaciones (estrato, región, cuenca, país, red); entran si se eligen a mano
    ExcluirAgregados = {81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 42, 69, 76, 77},
    // Estaciones que solo miden precipitación (RLS): el resto de sus variables se descarta
    SoloPrecipitacion = {42, 69, 76, 77},
    Tabla = Table.FromList(Estaciones, Splitter.SplitByNothing(), {"estacionid"}),
    Solo = Table.AddColumn(Tabla, "Solo_Precip", each List.Contains(SoloPrecipitacion, [estacionid])),
    Excl = Table.AddColumn(Solo, "Excluir_Agregados", each if List.Contains(ExcluirAgregados, [estacionid]) then 1 else 0),
    Tipo = Table.AddColumn(Excl, "Tipo", each if List.Contains(TipoB, [estacionid]) then "B" else "A"),
    Tipos = Table.TransformColumnTypes(Tipo, {{"estacionid", Int64.Type}, {"Solo_Precip", type logical}, {"Excluir_Agregados", Int64.Type}, {"Tipo", type text}})
in
    Tipos
```
</details>


### `Umbral_Rad_Opt`

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `MJ` | int64 | 0 |  |  |

<details><summary>Expresión DAX (tabla calculada)</summary>

```dax
SELECTCOLUMNS ( GENERATESERIES ( 0, 35, 1 ), "MJ", [Value] )
```
</details>


### `Umbral_Rad_Sub`

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `MJ` | int64 | 0 |  |  |

<details><summary>Expresión DAX (tabla calculada)</summary>

```dax
SELECTCOLUMNS ( GENERATESERIES ( 0, 35, 1 ), "MJ", [Value] )
```
</details>


### `Variables`

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `Clave` | string |  |  |  |
| `Variable` | string |  | `Orden` |  |
| `Unidad` | string |  |  |  |
| `Regla` | string |  |  |  |
| `Orden` | int64 | 0 |  | oculta |
| `Grupo` | string |  |  |  |
| `Anom_Tipo` | string |  |  | oculta |
| `Umbral1` | double |  |  | oculta |
| `Umbral2` | double |  |  | oculta |
| `Color_Actual` | string |  |  | oculta |
| `Color_Rango` | string |  |  | oculta |
| `Color_Normal` | string |  |  | oculta |
| `Decimales` | int64 | 0 |  | oculta |
| `Positivo_Azul` | int64 | 0 |  | oculta |

<details><summary>Expresión DAX (tabla calculada)</summary>

```dax
DATATABLE (
    "Clave", STRING, "Variable", STRING, "Unidad", STRING, "Regla", STRING, "Orden", INTEGER, "Grupo", STRING, "Anom_Tipo", STRING, "Umbral1", DOUBLE, "Umbral2", DOUBLE, "Color_Actual", STRING, "Color_Rango", STRING, "Color_Normal", STRING, "Decimales", INTEGER, "Positivo_Azul", INTEGER,
    {
        {"PCP", "Precipitación", "mm", "Suma", 1, "Agua", "pct", 15, 40, "#00008B", "#4682B4", "#36648B", 0, 1},
        {"ETO", "Evapotranspiración potencial (ETo)", "mm", "Suma", 2, "Agua", "pct", 15, 40, "#006400", "#8FBC8F", "#2E8B57", 0, 0},
        {"ETOD", "ETo media diaria", "mm/día", "Promedio", 3, "Agua", "pct", 15, 40, "#006400", "#8FBC8F", "#2E8B57", 1, 0},
        {"BH", "Balance hídrico (P − ETo)", "mm", "Suma", 4, "Agua", "pct", 25, 50, "#1B2A49", "#C9CED8", "#6B7A99", 0, 1},
        {"RAD", "Radiación solar", "MJ/m²", "Suma", 5, "Radiación", "pct", 10, 20, "#8B4513", "#F4A460", "#CD853F", 0, 0},
        {"IRR", "Irradiancia diurna media", "W/m²", "Promedio", 6, "Radiación", "pct", 10, 20, "#8B4513", "#F4A460", "#CD853F", 0, 0},
        {"TMED", "Temperatura media", "°C", "Promedio", 7, "Temperatura", "abs", 0.5, 1, "#8B0000", "#CD4F39", "#FF6347", 1, 0},
        {"TMAX", "Temperatura máxima", "°C", "Máximo", 8, "Temperatura", "abs", 0.5, 1, "#8B0000", "#CD4F39", "#FF6347", 1, 0},
        {"TMIN", "Temperatura mínima", "°C", "Mínimo", 9, "Temperatura", "abs", 0.5, 1, "#8B0000", "#CD4F39", "#FF6347", 1, 0},
        {"ICMED", "Sensación térmica media", "°C", "Promedio", 10, "Temperatura", "abs", 0.5, 1, "#A63603", "#FDAE6B", "#E6550D", 1, 0},
        {"IC", "Sensación térmica máxima", "°C", "Máximo", 11, "Temperatura", "abs", 0.5, 1, "#A63603", "#FDAE6B", "#E6550D", 1, 0},
        {"ICMIN", "Sensación térmica mínima", "°C", "Mínimo", 12, "Temperatura", "abs", 0.5, 1, "#A63603", "#FDAE6B", "#E6550D", 1, 0}
    }
)
```
</details>


### `Vista_Comp`

| Columna | Tipo | Formato | Ordenar por | Notas |
|---|---|---|---|---|
| `Vista` | string |  | `Orden` |  |
| `Orden` | int64 | 0 |  | oculta |

<details><summary>Expresión DAX (tabla calculada)</summary>

```dax
DATATABLE (
    "Vista", STRING, "Orden", INTEGER,
    {
        {"Mensual", 1},
        {"Acumulado mensual", 2}
    }
)
```
</details>


