# Catálogo de medidas DAX

> Generado automáticamente por `tools/generar_docs_modelo.py` el 2026-11-10 (100 medidas). No editar a mano.

Convenciones: las medidas con prefijo `_` son auxiliares. Con varias estaciones, las variables acumulativas (precipitación, ETo, balance, radiación) **suman por estación y luego promedian entre estaciones**; los promedios se calculan por estación y luego entre estaciones; las temperaturas máxima y mínima mensuales son el extremo de cada estación, promediado. Las medidas que dependen de la variable usan `Var_Sel` (tabla `Variables`). Ver `01_arquitectura.md` y `06_decisiones_y_cambios.md`.

## Índice

- [0 Contexto](#0-contexto) (11)
- [1 Diario](#1-diario) (7)
- [2 Mensual](#2-mensual) (3)
- [3 Histórico](#3-histórico) (8)
- [4 Anomalías](#4-anomalías) (8)
- [5 Años adicionales](#5-años-adicionales) (16)
- [6 Acumulados](#6-acumulados) (7)
- [7 Textos y banderas](#7-textos-y-banderas) (16)
- [8 Páginas heredadas](#8-páginas-heredadas) (20)
- [9 Validación](#9-validación) (4)

## 0 Contexto

| Medida | Formato | Descripción |
|---|---|---|
| `Var_Sel` |  | Variable elegida; sin selección, la primera disponible en la página |
| `Var_Nombre` |  |  |
| `Var_Unidad` |  |  |
| `Var_Regla` |  | Suma (acumulativas) · Promedio · Máximo · Mínimo |
| `Ultima_Fecha` | dd/mm/yyyy |  |
| `Ultimo_Mes_Completo` | 0 | Último mes cerrado (AAAAMM) |
| `Anio_Analisis` | 0 | Año del segmentador Año de análisis; sin selección, el año del último dato |
| `Base_Ini` | 0 | Inicio del periodo histórico (segmentador) |
| `Base_Fin` | 0 | Fin del periodo histórico; nunca incluye el año de análisis |
| `N_Estaciones` | 0 | Estaciones de la selección que tienen datos |
| `Base_Disponible` | 0 | Filtro del segmentador de periodo histórico: solo años anteriores al de análisis |

<details><summary><code>Var_Sel</code></summary>

```dax
SELECTEDVALUE (
    Variables[Clave],
    MAXX ( TOPN ( 1, VALUES ( Variables ), Variables[Orden], ASC ), Variables[Clave] )
)
```
</details>

<details><summary><code>Var_Nombre</code></summary>

```dax
VAR _v = [Var_Sel]
RETURN MAXX ( FILTER ( ALL ( Variables ), Variables[Clave] = _v ), Variables[Variable] )
```
</details>

<details><summary><code>Var_Unidad</code></summary>

```dax
VAR _v = [Var_Sel]
RETURN MAXX ( FILTER ( ALL ( Variables ), Variables[Clave] = _v ), Variables[Unidad] )
```
</details>

<details><summary><code>Var_Regla</code></summary>

```dax
VAR _v = [Var_Sel]
RETURN MAXX ( FILTER ( ALL ( Variables ), Variables[Clave] = _v ), Variables[Regla] )
```
</details>

<details><summary><code>Ultima_Fecha</code></summary>

```dax
CALCULATE ( MAX ( Fact_Diaria_met[Fecha] ), REMOVEFILTERS () )
```
</details>

<details><summary><code>Ultimo_Mes_Completo</code></summary>

```dax
CALCULATE (
    MAXX ( FILTER ( Fact_Mensual_met, Fact_Mensual_met[Mes_Completo] ), Fact_Mensual_met[Anio] * 100 + Fact_Mensual_met[Mes] ),
    REMOVEFILTERS ()
)
```
</details>

<details><summary><code>Anio_Analisis</code></summary>

```dax
SELECTEDVALUE ( Anio_Sel[Año], YEAR ( [Ultima_Fecha] ) )
```
</details>

<details><summary><code>Base_Ini</code></summary>

```dax
MIN ( Anios_Base[Año] )
```
</details>

<details><summary><code>Base_Fin</code></summary>

```dax
MIN ( MAX ( Anios_Base[Año] ), [Anio_Analisis] - 1 )
```
</details>

<details><summary><code>N_Estaciones</code></summary>

```dax
CALCULATE ( DISTINCTCOUNT ( Fact_Mensual_met[estacionid] ) )
```
</details>

<details><summary><code>Base_Disponible</code></summary>

```dax
IF ( MAX ( Anios_Base[Año] ) < [Anio_Analisis], 1 )
```
</details>

## 1 Diario

| Medida | Formato | Descripción |
|---|---|---|
| `_Dia_Est` |  | Valor de UNA estación en el periodo del contexto |
| `Valor_Diario` | 0.0 | Suma (o promedio/extremo) por estación y luego promedio de las estaciones con dato |
| `PCP_Anio` | 0.0 | Precipitación en el año de análisis (eje de pentadas) |
| `ETO_Anio` | 0.0 | ETo en el año de análisis (eje de pentadas) |
| `BH_Anio` | 0.0 | Balance en el año de análisis (eje de pentadas) |
| `Pentada_Inicio` | dd/mm/yyyy |  |
| `Pentada_Fin` | dd/mm/yyyy |  |

<details><summary><code>_Dia_Est</code></summary>

```dax
VAR v = [Var_Sel]
RETURN
    SWITCH (
        v,
        "PCP", SUM ( Fact_Diaria_met[Precip_Total] ),
        "ETO", SUM ( Fact_Diaria_met[ETO_Total] ),
        "ETOD", AVERAGE ( Fact_Diaria_met[ETO_Total] ),
        "BH", SUM ( Fact_Diaria_met[Balance_Hidrico] ),
        "RAD", SUM ( Fact_Diaria_met[Rad_MJ] ),
        "IRR", AVERAGE ( Fact_Diaria_met[Irradiancia_Diurna] ),
        "TMED", AVERAGE ( Fact_Diaria_met[Temp_Media] ),
        "TMAX", MAX ( Fact_Diaria_met[Temp_Max] ),
        "TMIN", MIN ( Fact_Diaria_met[Temp_Min] ),
        "ICMED", AVERAGE ( Fact_Diaria_met[IC_Media] ),
        "IC", MAX ( Fact_Diaria_met[IC_Max] ),
        "ICMIN", MIN ( Fact_Diaria_met[IC_Min] )
    )
```
</details>

<details><summary><code>Valor_Diario</code></summary>

```dax
AVERAGEX ( VALUES ( Estaciones_met[estacionid] ), [_Dia_Est] )
```
</details>

<details><summary><code>PCP_Anio</code></summary>

```dax
VAR _y = [Anio_Analisis] RETURN CALCULATE ( [Valor_Diario], Variables[Clave] = "PCP", Calendario[Anio] = _y )
```
</details>

<details><summary><code>ETO_Anio</code></summary>

```dax
VAR _y = [Anio_Analisis] RETURN CALCULATE ( [Valor_Diario], Variables[Clave] = "ETO", Calendario[Anio] = _y )
```
</details>

<details><summary><code>BH_Anio</code></summary>

```dax
VAR _y = [Anio_Analisis] RETURN CALCULATE ( [Valor_Diario], Variables[Clave] = "BH", Calendario[Anio] = _y )
```
</details>

<details><summary><code>Pentada_Inicio</code></summary>

```dax
VAR _y = [Anio_Analisis] RETURN CALCULATE ( MIN ( Calendario[Fecha] ), Calendario[Anio] = _y )
```
</details>

<details><summary><code>Pentada_Fin</code></summary>

```dax
VAR _y = [Anio_Analisis] RETURN CALCULATE ( MAX ( Calendario[Fecha] ), Calendario[Anio] = _y )
```
</details>

## 2 Mensual

| Medida | Formato | Descripción |
|---|---|---|
| `_Mes_Est` |  | Valor de UNA estación en los meses del contexto (solo meses cerrados con ≥ 80 % de días) |
| `_Grupo_Mes` |  | Promedio entre las estaciones seleccionadas (pool estación-año) |
| `Valor_Mensual` | 0.0 | Variable por mes en el año de análisis; el mes en curso no se muestra |

<details><summary><code>_Mes_Est</code></summary>

```dax
VAR v = [Var_Sel]
RETURN
    CALCULATE (
        SWITCH (
            v,
            "PCP", SUM ( Fact_Mensual_met[Precip] ),
            "ETO", SUM ( Fact_Mensual_met[ETo] ),
            "ETOD", AVERAGE ( Fact_Mensual_met[ETo_Dia] ),
            "BH", SUM ( Fact_Mensual_met[BH] ),
            "RAD", SUM ( Fact_Mensual_met[Rad_MJ] ),
            "IRR", AVERAGE ( Fact_Mensual_met[Irradiancia] ),
            "TMED", AVERAGE ( Fact_Mensual_met[Temp_Media] ),
            "TMAX", MAX ( Fact_Mensual_met[Temp_Max_Abs] ),
            "TMIN", MIN ( Fact_Mensual_met[Temp_Min_Abs] ),
            "ICMED", AVERAGE ( Fact_Mensual_met[IC_Media] ),
            "IC", MAX ( Fact_Mensual_met[IC_Max] ),
            "ICMIN", MIN ( Fact_Mensual_met[IC_Min_Abs] )
        ),
        Fact_Mensual_met[Mes_Valido] = TRUE ()
    )
```
</details>

<details><summary><code>_Grupo_Mes</code></summary>

```dax
AVERAGEX ( VALUES ( Estaciones_met[estacionid] ), [_Mes_Est] )
```
</details>

<details><summary><code>Valor_Mensual</code></summary>

```dax
VAR _y = [Anio_Analisis]
RETURN
    CALCULATE (
        [_Grupo_Mes],
        Fact_Mensual_met[Anio] = _y,
        TREATAS ( VALUES ( Calendario[Mes_Num] ), Fact_Mensual_met[Mes] )
    )
```
</details>

## 3 Histórico

| Medida | Formato | Descripción |
|---|---|---|
| `Hist_Media` | 0.0 | Media de los valores mensuales de la selección en el periodo histórico |
| `Hist_Min` | 0.0 | Mínimo histórico |
| `Hist_Max` | 0.0 | Máximo histórico |
| `Hist_P33` | 0.0 | Percentil 33 (igual a quantile tipo 7 de R) |
| `Hist_P66` | 0.0 | Percentil 66 |
| `Hist_N_Anios` | 0.0 | Años con dato en el periodo histórico |
| `Hist_Anio_Ini` | 0 | Año real con datos de la selección (para la leyenda y el subtítulo) |
| `Hist_Anio_Fin` | 0 | Año real con datos de la selección (para la leyenda y el subtítulo) |

<details><summary><code>Hist_Media</code></summary>

```dax
VAR _meses = VALUES ( Calendario[Mes_Num] )
VAR _ini = [Base_Ini]
VAR _fin = [Base_Fin]
VAR _t =
    FILTER (
        ADDCOLUMNS (
            FILTER ( ALL ( Fact_Mensual_met[Anio] ), Fact_Mensual_met[Anio] >= _ini && Fact_Mensual_met[Anio] <= _fin ),
            "@v", CALCULATE ( [_Grupo_Mes], TREATAS ( _meses, Fact_Mensual_met[Mes] ) )
        ),
        NOT ISBLANK ( [@v] )
    )
RETURN
    AVERAGEX ( _t, [@v] )
```
</details>

<details><summary><code>Hist_Min</code></summary>

```dax
VAR _meses = VALUES ( Calendario[Mes_Num] )
VAR _ini = [Base_Ini]
VAR _fin = [Base_Fin]
VAR _t =
    FILTER (
        ADDCOLUMNS (
            FILTER ( ALL ( Fact_Mensual_met[Anio] ), Fact_Mensual_met[Anio] >= _ini && Fact_Mensual_met[Anio] <= _fin ),
            "@v", CALCULATE ( [_Grupo_Mes], TREATAS ( _meses, Fact_Mensual_met[Mes] ) )
        ),
        NOT ISBLANK ( [@v] )
    )
RETURN
    MINX ( _t, [@v] )
```
</details>

<details><summary><code>Hist_Max</code></summary>

```dax
VAR _meses = VALUES ( Calendario[Mes_Num] )
VAR _ini = [Base_Ini]
VAR _fin = [Base_Fin]
VAR _t =
    FILTER (
        ADDCOLUMNS (
            FILTER ( ALL ( Fact_Mensual_met[Anio] ), Fact_Mensual_met[Anio] >= _ini && Fact_Mensual_met[Anio] <= _fin ),
            "@v", CALCULATE ( [_Grupo_Mes], TREATAS ( _meses, Fact_Mensual_met[Mes] ) )
        ),
        NOT ISBLANK ( [@v] )
    )
RETURN
    MAXX ( _t, [@v] )
```
</details>

<details><summary><code>Hist_P33</code></summary>

```dax
VAR _meses = VALUES ( Calendario[Mes_Num] )
VAR _ini = [Base_Ini]
VAR _fin = [Base_Fin]
VAR _t =
    FILTER (
        ADDCOLUMNS (
            FILTER ( ALL ( Fact_Mensual_met[Anio] ), Fact_Mensual_met[Anio] >= _ini && Fact_Mensual_met[Anio] <= _fin ),
            "@v", CALCULATE ( [_Grupo_Mes], TREATAS ( _meses, Fact_Mensual_met[Mes] ) )
        ),
        NOT ISBLANK ( [@v] )
    )
RETURN
    PERCENTILEX.INC ( _t, [@v], 0.33 )
```
</details>

<details><summary><code>Hist_P66</code></summary>

```dax
VAR _meses = VALUES ( Calendario[Mes_Num] )
VAR _ini = [Base_Ini]
VAR _fin = [Base_Fin]
VAR _t =
    FILTER (
        ADDCOLUMNS (
            FILTER ( ALL ( Fact_Mensual_met[Anio] ), Fact_Mensual_met[Anio] >= _ini && Fact_Mensual_met[Anio] <= _fin ),
            "@v", CALCULATE ( [_Grupo_Mes], TREATAS ( _meses, Fact_Mensual_met[Mes] ) )
        ),
        NOT ISBLANK ( [@v] )
    )
RETURN
    PERCENTILEX.INC ( _t, [@v], 0.66 )
```
</details>

<details><summary><code>Hist_N_Anios</code></summary>

```dax
VAR _meses = VALUES ( Calendario[Mes_Num] )
VAR _ini = [Base_Ini]
VAR _fin = [Base_Fin]
VAR _t =
    FILTER (
        ADDCOLUMNS (
            FILTER ( ALL ( Fact_Mensual_met[Anio] ), Fact_Mensual_met[Anio] >= _ini && Fact_Mensual_met[Anio] <= _fin ),
            "@v", CALCULATE ( [_Grupo_Mes], TREATAS ( _meses, Fact_Mensual_met[Mes] ) )
        ),
        NOT ISBLANK ( [@v] )
    )
RETURN
    COUNTROWS ( _t )
```
</details>

<details><summary><code>Hist_Anio_Ini</code></summary>

```dax
VAR _ini = [Base_Ini]
VAR _fin = [Base_Fin]
RETURN
    CALCULATE (
        MIN ( Fact_Mensual_met[Anio] ),
        Fact_Mensual_met[Mes_Valido] = TRUE (),
        Fact_Mensual_met[Anio] >= _ini,
        Fact_Mensual_met[Anio] <= _fin
    )
```
</details>

<details><summary><code>Hist_Anio_Fin</code></summary>

```dax
VAR _ini = [Base_Ini]
VAR _fin = [Base_Fin]
RETURN
    CALCULATE (
        MAX ( Fact_Mensual_met[Anio] ),
        Fact_Mensual_met[Mes_Valido] = TRUE (),
        Fact_Mensual_met[Anio] >= _ini,
        Fact_Mensual_met[Anio] <= _fin
    )
```
</details>

## 4 Anomalías

| Medida | Formato | Descripción |
|---|---|---|
| `Anomalia` | +0.0;-0.0;0.0 | Año de análisis − media histórica |
| `Anomalia_Pct` | +0.0%;-0.0%;0.0% |  |
| `Anomalia_Etiqueta` |  | Texto como en los scripts R ('\|' = salto de línea) |
| `Anomalia_Color` |  | Lluvia y balance: positivo azul; temperatura, ETo y radiación: positivo rojo |
| `Anomalia_Acum` | +0.0;-0.0;0.0 | Acumulado del año − acumulado medio |
| `Anomalia_Acum_Pct` | +0.0%;-0.0%;0.0% |  |
| `Anomalia_Acum_Etiqueta` |  | Texto como en los scripts R ('\|' = salto de línea) |
| `Anomalia_Acum_Color` |  | Lluvia y balance: positivo azul; temperatura, ETo y radiación: positivo rojo |

<details><summary><code>Anomalia</code></summary>

```dax
IF ( NOT ISBLANK ( [Valor_Mensual] ) && NOT ISBLANK ( [Hist_Media] ), [Valor_Mensual] - [Hist_Media] )
```
</details>

<details><summary><code>Anomalia_Pct</code></summary>

```dax
IF ( NOT ISBLANK ( [Anomalia] ), DIVIDE ( [Anomalia], [Hist_Media] ) )
```
</details>

<details><summary><code>Anomalia_Etiqueta</code></summary>

```dax
VAR _a = [Anomalia]
VAR _v = [Var_Sel]
VAR _tipo = MAXX ( FILTER ( ALL ( Variables ), Variables[Clave] = _v ), Variables[Anom_Tipo] )
RETURN
    IF (
        NOT ISBLANK ( _a ),
        FORMAT ( _a, "+0.#;-0.#;0" ) & " " & [Var_Unidad]
            & IF ( _tipo = "pct", "|(" & FORMAT ( [Anomalia_Pct], "+0.#%;-0.#%;0%" ) & ")" )
    )
```
</details>

<details><summary><code>Anomalia_Color</code></summary>

```dax
VAR _a = [Anomalia]
VAR _v = [Var_Sel]
VAR _azul = MAXX ( FILTER ( ALL ( Variables ), Variables[Clave] = _v ), Variables[Positivo_Azul] ) = 1
RETURN IF ( NOT ISBLANK ( _a ), IF ( ( _a >= 0 ) = _azul, "#4575b4", "#d73027" ) )
```
</details>

<details><summary><code>Anomalia_Acum</code></summary>

```dax
IF ( NOT ISBLANK ( [Acum_Mensual] ) && NOT ISBLANK ( [Hist_Acum_Media] ), [Acum_Mensual] - [Hist_Acum_Media] )
```
</details>

<details><summary><code>Anomalia_Acum_Pct</code></summary>

```dax
IF ( NOT ISBLANK ( [Anomalia_Acum] ), DIVIDE ( [Anomalia_Acum], [Hist_Acum_Media] ) )
```
</details>

<details><summary><code>Anomalia_Acum_Etiqueta</code></summary>

```dax
VAR _a = [Anomalia_Acum]
VAR _v = [Var_Sel]
VAR _tipo = MAXX ( FILTER ( ALL ( Variables ), Variables[Clave] = _v ), Variables[Anom_Tipo] )
RETURN
    IF (
        NOT ISBLANK ( _a ),
        FORMAT ( _a, "+0.#;-0.#;0" ) & " " & [Var_Unidad]
            & IF ( _tipo = "pct", "|(" & FORMAT ( [Anomalia_Acum_Pct], "+0.#%;-0.#%;0%" ) & ")" )
    )
```
</details>

<details><summary><code>Anomalia_Acum_Color</code></summary>

```dax
VAR _a = [Anomalia_Acum]
VAR _v = [Var_Sel]
VAR _azul = MAXX ( FILTER ( ALL ( Variables ), Variables[Clave] = _v ), Variables[Positivo_Azul] ) = 1
RETURN IF ( NOT ISBLANK ( _a ), IF ( ( _a >= 0 ) = _azul, "#4575b4", "#d73027" ) )
```
</details>

## 5 Años adicionales

| Medida | Formato | Descripción |
|---|---|---|
| `Anio_Comp_1` | 0 | Año adicional n.º 1 de la selección |
| `Anio_Comp_1_Txt` |  |  |
| `Valor_Comp_1` | 0.0 | Mismas estaciones que la selección |
| `Acum_Comp_1` | 0.0 |  |
| `Anio_Comp_2` | 0 | Año adicional n.º 2 de la selección |
| `Anio_Comp_2_Txt` |  |  |
| `Valor_Comp_2` | 0.0 | Mismas estaciones que la selección |
| `Acum_Comp_2` | 0.0 |  |
| `Anio_Comp_3` | 0 | Año adicional n.º 3 de la selección |
| `Anio_Comp_3_Txt` |  |  |
| `Valor_Comp_3` | 0.0 | Mismas estaciones que la selección |
| `Acum_Comp_3` | 0.0 |  |
| `Anio_Comp_4` | 0 | Año adicional n.º 4 de la selección |
| `Anio_Comp_4_Txt` |  |  |
| `Valor_Comp_4` | 0.0 | Mismas estaciones que la selección |
| `Acum_Comp_4` | 0.0 |  |

<details><summary><code>Anio_Comp_1</code></summary>

```dax
VAR _t = VALUES ( Anios_Comparacion[Año] )
RETURN
    IF (
        ISFILTERED ( Anios_Comparacion[Año] ) && COUNTROWS ( _t ) >= 1,
        MAXX ( TOPN ( 1, _t, Anios_Comparacion[Año], ASC ), Anios_Comparacion[Año] )
    )
```
</details>

<details><summary><code>Anio_Comp_1_Txt</code></summary>

```dax
FORMAT ( [Anio_Comp_1], "0" )
```
</details>

<details><summary><code>Valor_Comp_1</code></summary>

```dax
VAR _y = [Anio_Comp_1]
RETURN
    IF (
        NOT ISBLANK ( _y ),
        CALCULATE ( [_Grupo_Mes], Fact_Mensual_met[Anio] = _y, TREATAS ( VALUES ( Calendario[Mes_Num] ), Fact_Mensual_met[Mes] ) )
    )
```
</details>

<details><summary><code>Acum_Comp_1</code></summary>

```dax
VAR _modo = SELECTEDVALUE ( Meses_Acum[Modo], "Año calendario (ene–dic)" )
VAR _p = MAX ( Meses_Acum[Pos] )
VAR _y = [Anio_Comp_1]
VAR _pares =
    SELECTCOLUMNS (
        FILTER ( ALL ( Meses_Acum ), Meses_Acum[Modo] = _modo && Meses_Acum[Pos] <= _p ),
        "Anio", _y - Meses_Acum[Desfase_Anio],
        "Mes", Meses_Acum[Mes_Num]
    )
VAR _ultimo = MAXX ( _pares, [Anio] * 100 + [Mes] )
RETURN
    IF (
        NOT ISBLANK ( _y ) && [Var_Regla] = "Suma" && _ultimo <= [Ultimo_Mes_Completo],
        CALCULATE ( [_Grupo_Mes], TREATAS ( _pares, Fact_Mensual_met[Anio], Fact_Mensual_met[Mes] ) )
    )
```
</details>

<details><summary><code>Anio_Comp_2</code></summary>

```dax
VAR _t = VALUES ( Anios_Comparacion[Año] )
RETURN
    IF (
        ISFILTERED ( Anios_Comparacion[Año] ) && COUNTROWS ( _t ) >= 2,
        MAXX ( TOPN ( 2, _t, Anios_Comparacion[Año], ASC ), Anios_Comparacion[Año] )
    )
```
</details>

<details><summary><code>Anio_Comp_2_Txt</code></summary>

```dax
FORMAT ( [Anio_Comp_2], "0" )
```
</details>

<details><summary><code>Valor_Comp_2</code></summary>

```dax
VAR _y = [Anio_Comp_2]
RETURN
    IF (
        NOT ISBLANK ( _y ),
        CALCULATE ( [_Grupo_Mes], Fact_Mensual_met[Anio] = _y, TREATAS ( VALUES ( Calendario[Mes_Num] ), Fact_Mensual_met[Mes] ) )
    )
```
</details>

<details><summary><code>Acum_Comp_2</code></summary>

```dax
VAR _modo = SELECTEDVALUE ( Meses_Acum[Modo], "Año calendario (ene–dic)" )
VAR _p = MAX ( Meses_Acum[Pos] )
VAR _y = [Anio_Comp_2]
VAR _pares =
    SELECTCOLUMNS (
        FILTER ( ALL ( Meses_Acum ), Meses_Acum[Modo] = _modo && Meses_Acum[Pos] <= _p ),
        "Anio", _y - Meses_Acum[Desfase_Anio],
        "Mes", Meses_Acum[Mes_Num]
    )
VAR _ultimo = MAXX ( _pares, [Anio] * 100 + [Mes] )
RETURN
    IF (
        NOT ISBLANK ( _y ) && [Var_Regla] = "Suma" && _ultimo <= [Ultimo_Mes_Completo],
        CALCULATE ( [_Grupo_Mes], TREATAS ( _pares, Fact_Mensual_met[Anio], Fact_Mensual_met[Mes] ) )
    )
```
</details>

<details><summary><code>Anio_Comp_3</code></summary>

```dax
VAR _t = VALUES ( Anios_Comparacion[Año] )
RETURN
    IF (
        ISFILTERED ( Anios_Comparacion[Año] ) && COUNTROWS ( _t ) >= 3,
        MAXX ( TOPN ( 3, _t, Anios_Comparacion[Año], ASC ), Anios_Comparacion[Año] )
    )
```
</details>

<details><summary><code>Anio_Comp_3_Txt</code></summary>

```dax
FORMAT ( [Anio_Comp_3], "0" )
```
</details>

<details><summary><code>Valor_Comp_3</code></summary>

```dax
VAR _y = [Anio_Comp_3]
RETURN
    IF (
        NOT ISBLANK ( _y ),
        CALCULATE ( [_Grupo_Mes], Fact_Mensual_met[Anio] = _y, TREATAS ( VALUES ( Calendario[Mes_Num] ), Fact_Mensual_met[Mes] ) )
    )
```
</details>

<details><summary><code>Acum_Comp_3</code></summary>

```dax
VAR _modo = SELECTEDVALUE ( Meses_Acum[Modo], "Año calendario (ene–dic)" )
VAR _p = MAX ( Meses_Acum[Pos] )
VAR _y = [Anio_Comp_3]
VAR _pares =
    SELECTCOLUMNS (
        FILTER ( ALL ( Meses_Acum ), Meses_Acum[Modo] = _modo && Meses_Acum[Pos] <= _p ),
        "Anio", _y - Meses_Acum[Desfase_Anio],
        "Mes", Meses_Acum[Mes_Num]
    )
VAR _ultimo = MAXX ( _pares, [Anio] * 100 + [Mes] )
RETURN
    IF (
        NOT ISBLANK ( _y ) && [Var_Regla] = "Suma" && _ultimo <= [Ultimo_Mes_Completo],
        CALCULATE ( [_Grupo_Mes], TREATAS ( _pares, Fact_Mensual_met[Anio], Fact_Mensual_met[Mes] ) )
    )
```
</details>

<details><summary><code>Anio_Comp_4</code></summary>

```dax
VAR _t = VALUES ( Anios_Comparacion[Año] )
RETURN
    IF (
        ISFILTERED ( Anios_Comparacion[Año] ) && COUNTROWS ( _t ) >= 4,
        MAXX ( TOPN ( 4, _t, Anios_Comparacion[Año], ASC ), Anios_Comparacion[Año] )
    )
```
</details>

<details><summary><code>Anio_Comp_4_Txt</code></summary>

```dax
FORMAT ( [Anio_Comp_4], "0" )
```
</details>

<details><summary><code>Valor_Comp_4</code></summary>

```dax
VAR _y = [Anio_Comp_4]
RETURN
    IF (
        NOT ISBLANK ( _y ),
        CALCULATE ( [_Grupo_Mes], Fact_Mensual_met[Anio] = _y, TREATAS ( VALUES ( Calendario[Mes_Num] ), Fact_Mensual_met[Mes] ) )
    )
```
</details>

<details><summary><code>Acum_Comp_4</code></summary>

```dax
VAR _modo = SELECTEDVALUE ( Meses_Acum[Modo], "Año calendario (ene–dic)" )
VAR _p = MAX ( Meses_Acum[Pos] )
VAR _y = [Anio_Comp_4]
VAR _pares =
    SELECTCOLUMNS (
        FILTER ( ALL ( Meses_Acum ), Meses_Acum[Modo] = _modo && Meses_Acum[Pos] <= _p ),
        "Anio", _y - Meses_Acum[Desfase_Anio],
        "Mes", Meses_Acum[Mes_Num]
    )
VAR _ultimo = MAXX ( _pares, [Anio] * 100 + [Mes] )
RETURN
    IF (
        NOT ISBLANK ( _y ) && [Var_Regla] = "Suma" && _ultimo <= [Ultimo_Mes_Completo],
        CALCULATE ( [_Grupo_Mes], TREATAS ( _pares, Fact_Mensual_met[Anio], Fact_Mensual_met[Mes] ) )
    )
```
</details>

## 6 Acumulados

| Medida | Formato | Descripción |
|---|---|---|
| `Modo_Hidro` | 0 |  |
| `Acum_Mensual` | 0.0 | Acumulado del año de análisis (civil o hidrológico); suma por estación y luego promedio |
| `Hist_Acum_Media` | 0.0 | Suma acumulada de Hist_Media (como los scripts R) |
| `Hist_Acum_Min` | 0.0 | Suma acumulada de Hist_Min (como los scripts R) |
| `Hist_Acum_Max` | 0.0 | Suma acumulada de Hist_Max (como los scripts R) |
| `Hist_Acum_P33` | 0.0 | Suma acumulada de Hist_P33 (como los scripts R) |
| `Hist_Acum_P66` | 0.0 | Suma acumulada de Hist_P66 (como los scripts R) |

<details><summary><code>Modo_Hidro</code></summary>

```dax
IF ( SELECTEDVALUE ( Meses_Acum[Modo], "Año calendario (ene–dic)" ) = "Año calendario (ene–dic)", 0, 1 )
```
</details>

<details><summary><code>Acum_Mensual</code></summary>

```dax
VAR _modo = SELECTEDVALUE ( Meses_Acum[Modo], "Año calendario (ene–dic)" )
VAR _p = MAX ( Meses_Acum[Pos] )
VAR _y = [Anio_Analisis]
VAR _pares =
    SELECTCOLUMNS (
        FILTER ( ALL ( Meses_Acum ), Meses_Acum[Modo] = _modo && Meses_Acum[Pos] <= _p ),
        "Anio", _y - Meses_Acum[Desfase_Anio],
        "Mes", Meses_Acum[Mes_Num]
    )
VAR _ultimo = MAXX ( _pares, [Anio] * 100 + [Mes] )
RETURN
    IF (
        NOT ISBLANK ( _y ) && [Var_Regla] = "Suma" && _ultimo <= [Ultimo_Mes_Completo],
        CALCULATE ( [_Grupo_Mes], TREATAS ( _pares, Fact_Mensual_met[Anio], Fact_Mensual_met[Mes] ) )
    )
```
</details>

<details><summary><code>Hist_Acum_Media</code></summary>

```dax
VAR _modo = SELECTEDVALUE ( Meses_Acum[Modo], "Año calendario (ene–dic)" )
VAR _p = MAX ( Meses_Acum[Pos] )
RETURN
    IF (
        [Var_Regla] = "Suma",
        SUMX (
            FILTER ( ALL ( Meses_Acum ), Meses_Acum[Modo] = _modo && Meses_Acum[Pos] <= _p ),
            VAR _m = Meses_Acum[Mes_Num]
            RETURN CALCULATE ( [Hist_Media], REMOVEFILTERS ( Meses_Acum ), Calendario[Mes_Num] = _m )
        )
    )
```
</details>

<details><summary><code>Hist_Acum_Min</code></summary>

```dax
VAR _modo = SELECTEDVALUE ( Meses_Acum[Modo], "Año calendario (ene–dic)" )
VAR _p = MAX ( Meses_Acum[Pos] )
RETURN
    IF (
        [Var_Regla] = "Suma",
        SUMX (
            FILTER ( ALL ( Meses_Acum ), Meses_Acum[Modo] = _modo && Meses_Acum[Pos] <= _p ),
            VAR _m = Meses_Acum[Mes_Num]
            RETURN CALCULATE ( [Hist_Min], REMOVEFILTERS ( Meses_Acum ), Calendario[Mes_Num] = _m )
        )
    )
```
</details>

<details><summary><code>Hist_Acum_Max</code></summary>

```dax
VAR _modo = SELECTEDVALUE ( Meses_Acum[Modo], "Año calendario (ene–dic)" )
VAR _p = MAX ( Meses_Acum[Pos] )
RETURN
    IF (
        [Var_Regla] = "Suma",
        SUMX (
            FILTER ( ALL ( Meses_Acum ), Meses_Acum[Modo] = _modo && Meses_Acum[Pos] <= _p ),
            VAR _m = Meses_Acum[Mes_Num]
            RETURN CALCULATE ( [Hist_Max], REMOVEFILTERS ( Meses_Acum ), Calendario[Mes_Num] = _m )
        )
    )
```
</details>

<details><summary><code>Hist_Acum_P33</code></summary>

```dax
VAR _modo = SELECTEDVALUE ( Meses_Acum[Modo], "Año calendario (ene–dic)" )
VAR _p = MAX ( Meses_Acum[Pos] )
RETURN
    IF (
        [Var_Regla] = "Suma",
        SUMX (
            FILTER ( ALL ( Meses_Acum ), Meses_Acum[Modo] = _modo && Meses_Acum[Pos] <= _p ),
            VAR _m = Meses_Acum[Mes_Num]
            RETURN CALCULATE ( [Hist_P33], REMOVEFILTERS ( Meses_Acum ), Calendario[Mes_Num] = _m )
        )
    )
```
</details>

<details><summary><code>Hist_Acum_P66</code></summary>

```dax
VAR _modo = SELECTEDVALUE ( Meses_Acum[Modo], "Año calendario (ene–dic)" )
VAR _p = MAX ( Meses_Acum[Pos] )
RETURN
    IF (
        [Var_Regla] = "Suma",
        SUMX (
            FILTER ( ALL ( Meses_Acum ), Meses_Acum[Modo] = _modo && Meses_Acum[Pos] <= _p ),
            VAR _m = Meses_Acum[Mes_Num]
            RETURN CALCULATE ( [Hist_P66], REMOVEFILTERS ( Meses_Acum ), Calendario[Mes_Num] = _m )
        )
    )
```
</details>

## 7 Textos y banderas

| Medida | Formato | Descripción |
|---|---|---|
| `Color_Actual` |  |  |
| `Color_Rango` |  |  |
| `Color_Normal` |  |  |
| `Mostrar_Actual` | 0 | Bandera de los scripts R (sin selección: encendida) |
| `Mostrar_Media` | 0 | Bandera de los scripts R (sin selección: apagada) |
| `Mostrar_Rangos` | 0 | Bandera de los scripts R (sin selección: encendida) |
| `Mostrar_Anios` | 0 | Bandera de los scripts R (sin selección: encendida) |
| `Mostrar_Anomalias` | 0 | Bandera de los scripts R (sin selección: encendida) |
| `Etiqueta_Actual` |  |  |
| `Etiqueta_Rango` |  |  |
| `Delimitacion` |  |  |
| `Titulo_Seleccion` |  | Estación individual, estrato o región si es una agregación predeterminada; si no, la delimitación |
| `Subtitulo_Seleccion` |  | El periodo histórico va en la leyenda |
| `Subtitulo_Acumulado` |  | El periodo histórico va en la leyenda |
| `Eje_Y` |  |  |
| `Eje_Y_Acum` |  |  |

<details><summary><code>Color_Actual</code></summary>

```dax
VAR _v = [Var_Sel]
RETURN MAXX ( FILTER ( ALL ( Variables ), Variables[Clave] = _v ), Variables[Color_Actual] )
```
</details>

<details><summary><code>Color_Rango</code></summary>

```dax
VAR _v = [Var_Sel]
RETURN MAXX ( FILTER ( ALL ( Variables ), Variables[Clave] = _v ), Variables[Color_Rango] )
```
</details>

<details><summary><code>Color_Normal</code></summary>

```dax
VAR _v = [Var_Sel]
RETURN MAXX ( FILTER ( ALL ( Variables ), Variables[Clave] = _v ), Variables[Color_Normal] )
```
</details>

<details><summary><code>Mostrar_Actual</code></summary>

```dax
IF ( ISFILTERED ( Capas[Capa] ), IF ( "Año actual" IN VALUES ( Capas[Capa] ), 1, 0 ), 1 )
```
</details>

<details><summary><code>Mostrar_Media</code></summary>

```dax
IF ( ISFILTERED ( Capas[Capa] ), IF ( "Media histórica" IN VALUES ( Capas[Capa] ), 1, 0 ), 0 )
```
</details>

<details><summary><code>Mostrar_Rangos</code></summary>

```dax
IF ( ISFILTERED ( Capas[Capa] ), IF ( "Rangos históricos" IN VALUES ( Capas[Capa] ), 1, 0 ), 1 )
```
</details>

<details><summary><code>Mostrar_Anios</code></summary>

```dax
IF ( ISFILTERED ( Capas[Capa] ), IF ( "Años adicionales" IN VALUES ( Capas[Capa] ), 1, 0 ), 1 )
```
</details>

<details><summary><code>Mostrar_Anomalias</code></summary>

```dax
IF ( ISFILTERED ( Capas[Capa] ), IF ( "Anomalías" IN VALUES ( Capas[Capa] ), 1, 0 ), 1 )
```
</details>

<details><summary><code>Etiqueta_Actual</code></summary>

```dax
"Actual (" & [Anio_Analisis] & ")"
```
</details>

<details><summary><code>Etiqueta_Rango</code></summary>

```dax
"Rango histórico (" & [Hist_Anio_Ini] & "–" & [Hist_Anio_Fin] & ")"
```
</details>

<details><summary><code>Delimitacion</code></summary>

```dax
VAR _p = CALCULATETABLE ( VALUES ( Estaciones_met[País] ), Fact_Mensual_met )
RETURN
    IF (
        COUNTROWS ( _p ) = 1,
        IF ( MAXX ( _p, Estaciones_met[País] ) = "Guatemala", "Costa sur de Guatemala", MAXX ( _p, Estaciones_met[País] ) ),
        "Red ICC (Guatemala y El Salvador)"
    )
```
</details>

<details><summary><code>Titulo_Seleccion</code></summary>

```dax
VAR _n = [N_Estaciones]
VAR _est = CALCULATETABLE ( VALUES ( Estaciones_met[Estación] ), Fact_Mensual_met )
VAR _estr = CALCULATETABLE ( VALUES ( Estaciones_met[Estrato] ), Fact_Mensual_met )
VAR _reg = CALCULATETABLE ( VALUES ( Estaciones_met[Región climática] ), Fact_Mensual_met )
VAR _fEst = ISFILTERED ( Estaciones_met[Estación] )
VAR _fEstr = ISFILTERED ( Estaciones_met[Estrato] ) && COUNTROWS ( _estr ) = 1
VAR _fReg = ISFILTERED ( Estaciones_met[Región climática] ) && COUNTROWS ( _reg ) = 1
RETURN
    SWITCH (
        TRUE (),
        _n = 1, "Estación " & MAXX ( _est, Estaciones_met[Estación] ),
        NOT _fEst && _fEstr && _fReg, "Estrato " & MAXX ( _estr, Estaciones_met[Estrato] ) & " — Región " & MAXX ( _reg, Estaciones_met[Región climática] ),
        NOT _fEst && _fEstr, "Estrato " & MAXX ( _estr, Estaciones_met[Estrato] ),
        NOT _fEst && _fReg, "Región " & MAXX ( _reg, Estaciones_met[Región climática] ),
        [Delimitacion]
    )
```
</details>

<details><summary><code>Subtitulo_Seleccion</code></summary>

```dax
VAR _n = [N_Estaciones]
VAR _t = [Titulo_Seleccion]
VAR _d = [Delimitacion]
RETURN
    "Año " & [Anio_Analisis]
        & IF ( _t <> _d && _n > 1, "  |  " & _d )
        & "  |  " & _n & IF ( _n = 1, " estación", " estaciones" )
```
</details>

<details><summary><code>Subtitulo_Acumulado</code></summary>

```dax
VAR _n = [N_Estaciones]
VAR _t = [Titulo_Seleccion]
VAR _d = [Delimitacion]
RETURN
    "Año " & [Anio_Analisis] & IF ( [Modo_Hidro] = 1, " (hidrológico)", " (calendario)" )
        & IF ( _t <> _d && _n > 1, "  |  " & _d )
        & "  |  " & _n & IF ( _n = 1, " estación", " estaciones" )
```
</details>

<details><summary><code>Eje_Y</code></summary>

```dax
[Var_Nombre] & " (" & [Var_Unidad] & ")"
```
</details>

<details><summary><code>Eje_Y_Acum</code></summary>

```dax
[Var_Nombre] & " acumulada (" & [Var_Unidad] & ")"
```
</details>

## 8 Páginas heredadas

| Medida | Formato | Descripción |
|---|---|---|
| `Mensual_Por_Anio` | 0.0 | Valor mensual con el año del contexto (año en la leyenda o en el segmentador) |
| `Acum_Mes_Por_Anio` | 0.0 | Acumulado de enero al mes del contexto |
| `Mensual_Pp` | 0.0 |  |
| `Mensual_ETPd` | 0.0 |  |
| `Mensual_TMax` | 0.0 |  |
| `Mensual_TMin` | 0.0 |  |
| `Mensual_TMed` | 0.0 |  |
| `Acum_Mes_Pp` | 0.0 |  |
| `Acum_Diario` | 0.0 | Acumulado desde el 1 de enero hasta la fecha del contexto |
| `Color_Mapa` |  | Color del mapa en 5 clases relativas entre las estaciones visibles |
| `Rad_Media_Pentada` | 0.0 | Radiación media diaria (MJ/m²) de la pentada en el año de análisis |
| `Banda_Rad_Suboptima` | 0 |  |
| `Banda_Rad_Aceptable` | 0 |  |
| `Banda_Rad_Optima` | 0 |  |
| `IC_Ultimo_Dia` | 0.0 | Sensación térmica máxima del último día con datos |
| `IC_Ultimos_7` | 0.0 |  |
| `Valor_Periodo_A` | 0.0 | Variable en las fechas del Periodo A |
| `Acum_Periodo_A` | 0.0 | Acumulado desde el inicio del Periodo A (eje: día del periodo) |
| `Valor_Periodo_B` | 0.0 | Variable en las fechas del Periodo B |
| `Acum_Periodo_B` | 0.0 | Acumulado desde el inicio del Periodo B (eje: día del periodo) |

<details><summary><code>Mensual_Por_Anio</code></summary>

```dax
CALCULATE (
    [_Grupo_Mes],
    TREATAS ( VALUES ( Calendario[Anio] ), Fact_Mensual_met[Anio] ),
    TREATAS ( VALUES ( Calendario[Mes_Num] ), Fact_Mensual_met[Mes] )
)
```
</details>

<details><summary><code>Acum_Mes_Por_Anio</code></summary>

```dax
VAR _m = MAX ( Calendario[Mes_Num] )
VAR _y = MAX ( Calendario[Anio] )
RETURN
    IF (
        [Var_Regla] = "Suma" && _y * 100 + _m <= [Ultimo_Mes_Completo],
        CALCULATE ( [_Grupo_Mes], Fact_Mensual_met[Anio] = _y, Fact_Mensual_met[Mes] <= _m )
    )
```
</details>

<details><summary><code>Mensual_Pp</code></summary>

```dax
CALCULATE ( [Mensual_Por_Anio], Variables[Clave] = "PCP" )
```
</details>

<details><summary><code>Mensual_ETPd</code></summary>

```dax
CALCULATE ( [Mensual_Por_Anio], Variables[Clave] = "ETOD" )
```
</details>

<details><summary><code>Mensual_TMax</code></summary>

```dax
CALCULATE ( [Mensual_Por_Anio], Variables[Clave] = "TMAX" )
```
</details>

<details><summary><code>Mensual_TMin</code></summary>

```dax
CALCULATE ( [Mensual_Por_Anio], Variables[Clave] = "TMIN" )
```
</details>

<details><summary><code>Mensual_TMed</code></summary>

```dax
CALCULATE ( [Mensual_Por_Anio], Variables[Clave] = "TMED" )
```
</details>

<details><summary><code>Acum_Mes_Pp</code></summary>

```dax
CALCULATE ( [Acum_Mes_Por_Anio], Variables[Clave] = "PCP" )
```
</details>

<details><summary><code>Acum_Diario</code></summary>

```dax
VAR _fin = MAX ( Calendario[Fecha] )
VAR _ini = DATE ( YEAR ( _fin ), 1, 1 )
RETURN
    IF (
        [Var_Regla] = "Suma" && _fin <= [Ultima_Fecha],
        AVERAGEX (
            VALUES ( Estaciones_met[estacionid] ),
            CALCULATE ( [_Dia_Est], REMOVEFILTERS ( Calendario ), DATESBETWEEN ( Calendario[Fecha], _ini, _fin ) )
        )
    )
```
</details>

<details><summary><code>Color_Mapa</code></summary>

```dax
VAR _v = [Valor_Diario]
VAR _sel = [Var_Sel]
VAR _g = MAXX ( FILTER ( ALL ( Variables ), Variables[Clave] = _sel ), Variables[Grupo] )
VAR _t = ADDCOLUMNS ( ALLSELECTED ( Estaciones_met[estacionid] ), "@v", [Valor_Diario] )
VAR _mn = MINX ( _t, [@v] )
VAR _mx = MAXX ( _t, [@v] )
VAR _k = IF ( _mx = _mn, 2, INT ( MIN ( DIVIDE ( _v - _mn, _mx - _mn ), 0.999 ) * 5 ) )
RETURN
    IF (
        NOT ISBLANK ( _v ),
        SWITCH (
            _g,
            "Agua", SWITCH ( _k, 0, "#DEEBF7", 1, "#9ECAE1", 2, "#4292C6", 3, "#2171B5", "#08306B" ),
            "Radiación", SWITCH ( _k, 0, "#FEE6CE", 1, "#FDAE6B", 2, "#F16913", 3, "#D94801", "#7F2704" ),
            SWITCH ( _k, 0, "#FEE0D2", 1, "#FC9272", 2, "#EF3B2C", 3, "#CB181D", "#67000D" )
        )
    )
```
</details>

<details><summary><code>Rad_Media_Pentada</code></summary>

```dax
VAR _y = [Anio_Analisis]
RETURN
    AVERAGEX (
        VALUES ( Estaciones_met[estacionid] ),
        CALCULATE ( AVERAGE ( Fact_Diaria_met[Rad_MJ] ), Calendario[Anio] = _y )
    )
```
</details>

<details><summary><code>Banda_Rad_Suboptima</code></summary>

```dax
SELECTEDVALUE ( Umbral_Rad_Sub[MJ], 12 )
```
</details>

<details><summary><code>Banda_Rad_Aceptable</code></summary>

```dax
SELECTEDVALUE ( Umbral_Rad_Opt[MJ], 20 ) - [Banda_Rad_Suboptima]
```
</details>

<details><summary><code>Banda_Rad_Optima</code></summary>

```dax
10
```
</details>

<details><summary><code>IC_Ultimo_Dia</code></summary>

```dax
VAR _u = [Ultima_Fecha] RETURN CALCULATE ( [Valor_Diario], Variables[Clave] = "IC", REMOVEFILTERS ( Calendario ), Calendario[Fecha] = _u )
```
</details>

<details><summary><code>IC_Ultimos_7</code></summary>

```dax
VAR _u = [Ultima_Fecha]
VAR _d = MAX ( Calendario[Fecha] )
RETURN IF ( _d > _u - 7 && _d <= _u, CALCULATE ( [Valor_Diario], Variables[Clave] = "IC" ) )
```
</details>

<details><summary><code>Valor_Periodo_A</code></summary>

```dax
AVERAGEX (
    VALUES ( Estaciones_met[estacionid] ),
    CALCULATE ( [_Dia_Est], REMOVEFILTERS ( Calendario ), TREATAS ( VALUES ( Periodo_A[Fecha] ), Fact_Diaria_met[Fecha] ) )
)
```
</details>

<details><summary><code>Acum_Periodo_A</code></summary>

```dax
VAR _ini = MIN ( Periodo_A[Fecha] )
VAR _fin = MAX ( Periodo_A[Fecha] )
VAR _f = _ini + MAX ( Dias_Periodo[Día] ) - 1
RETURN
    IF (
        [Var_Regla] = "Suma" && _f <= _fin && _f <= [Ultima_Fecha],
        AVERAGEX (
            VALUES ( Estaciones_met[estacionid] ),
            CALCULATE ( [_Dia_Est], REMOVEFILTERS ( Calendario ), DATESBETWEEN ( Calendario[Fecha], _ini, _f ) )
        )
    )
```
</details>

<details><summary><code>Valor_Periodo_B</code></summary>

```dax
AVERAGEX (
    VALUES ( Estaciones_met[estacionid] ),
    CALCULATE ( [_Dia_Est], REMOVEFILTERS ( Calendario ), TREATAS ( VALUES ( Periodo_B[Fecha] ), Fact_Diaria_met[Fecha] ) )
)
```
</details>

<details><summary><code>Acum_Periodo_B</code></summary>

```dax
VAR _ini = MIN ( Periodo_B[Fecha] )
VAR _fin = MAX ( Periodo_B[Fecha] )
VAR _f = _ini + MAX ( Dias_Periodo[Día] ) - 1
RETURN
    IF (
        [Var_Regla] = "Suma" && _f <= _fin && _f <= [Ultima_Fecha],
        AVERAGEX (
            VALUES ( Estaciones_met[estacionid] ),
            CALCULATE ( [_Dia_Est], REMOVEFILTERS ( Calendario ), DATESBETWEEN ( Calendario[Fecha], _ini, _f ) )
        )
    )
```
</details>

## 9 Validación

| Medida | Formato | Descripción |
|---|---|---|
| `Val_N_Dias` | #,0 |  |
| `Val_Meses_Validos` | #,0 |  |
| `Val_Primera_Fecha` | dd/mm/yyyy |  |
| `Val_Ultima_Fecha` | dd/mm/yyyy |  |

<details><summary><code>Val_N_Dias</code></summary>

```dax
CALCULATE ( COUNTROWS ( Fact_Diaria_met ) )
```
</details>

<details><summary><code>Val_Meses_Validos</code></summary>

```dax
CALCULATE ( COUNTROWS ( Fact_Mensual_met ), Fact_Mensual_met[Mes_Valido] = TRUE () )
```
</details>

<details><summary><code>Val_Primera_Fecha</code></summary>

```dax
CALCULATE ( MIN ( Fact_Diaria_met[Fecha] ) )
```
</details>

<details><summary><code>Val_Ultima_Fecha</code></summary>

```dax
CALCULATE ( MAX ( Fact_Diaria_met[Fecha] ) )
```
</details>
