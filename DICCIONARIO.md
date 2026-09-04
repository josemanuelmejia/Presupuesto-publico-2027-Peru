# Diccionario de variables

## Bases de asignaciones

`asignaciones-tacna-2027.csv`, `asignaciones-moquegua-2027.csv`, `asignaciones-puno-2027.csv`

Codificación UTF-8 con marca de orden de bytes, separador de punto y coma. Las tres
comparten las mismas 25 variables en el mismo orden, de modo que pueden concatenarse
directamente. Cada caso es una asignación presupuestaria elemental: ningún agregado ni
total del proyecto de ley entra en la base.

| Variable | Contenido | Valores o formato |
|---|---|---|
| `anexo` | Anexo del proyecto de ley del que proviene la fila | 5, 6, 7, 8, A |
| `archivo_pdf` | Archivo de origen | Nombre del PDF |
| `pagina_pdf` | Página dentro del PDF | Entero |
| `pagina_impresa` | Numeración correlativa del proyecto de ley | Entero |
| `nivel_gobierno` | Nivel de gobierno del pliego | Nacional, regional o local |
| `codigo_pliego` | Código del pliego | Tres dígitos en gobierno nacional y regional; seis en gobiernos locales |
| `pliego` | Denominación del pliego | Texto |
| `departamento` | Departamento al que corresponde la base | Tacna, Moquegua, Puno |
| `provincia` | Provincia, cuando el pliego es local | Texto |
| `distrito` | Distrito, cuando el pliego es local | Texto |
| `jurisdicciones_mencionadas` | Distritos y provincias que nombra la denominación de la partida | Separados por barra vertical |
| `categoria_presupuestal` | Categoría a la que pertenece la partida | Programas presupuestales, acciones centrales, APNOP |
| `programa_presupuestal` | Programa, en las filas del anexo 8 | Denominación; el anexo no asigna código numérico |
| `producto` | Producto padre, en las actividades | Código y denominación |
| `codigo_partida` | Código de la partida | Siete dígitos iniciados en 2, 3 o 5; genérica del gasto; o vacío |
| `tipo_partida` | Naturaleza de la asignación | Actividad, proyecto de inversión, producto sin actividades, genérica del gasto, asignación por programa presupuestal, subvención |
| `concepto` | Denominación de la partida | Texto |
| `fuente_financiamiento` | Fuente, donde el anexo la desagrega | Cinco valores; solo en el anexo 7 |
| `monto_soles` | Monto asignado | Entero sin separadores; vacío si el PDF lo dejó ilegible |
| `sector` | Clasificación funcional del gasto | Educación, salud, saneamiento, transporte y otros dieciséis valores |
| `alcance_territorial` | Dónde se ejecuta la obra o el servicio | Localizada en el departamento; multidepartamental |
| `base_no_duplicada` | Si la fila puede sumarse con las demás | Sí; No, replica los anexos 6 y 7 |
| `nota` | Incidencia de lectura y su tratamiento | Texto; vacío en la mayoría |
| `cuadra_el_pliego` | Si el pliego cierra contra su total impreso | Sí, No, No aplica |
| `diferencia_del_pliego` | Diferencia en soles cuando no cierra | Entero con signo |

### Advertencias de uso

- Las filas del anexo 8 replican por programa presupuestal dinero ya consignado en los
  anexos 6 y 7. **Filtrar por `base_no_duplicada` antes de sumar.**
- Las partidas de alcance multidepartamental abarcan varios departamentos y solo una
  fracción indeterminada corresponde al departamento de la base.
- Las líneas del anexo 7 no admiten sector, porque el anexo abre por genérica del gasto
  y no por función. Llevan el valor `No sectorizable`, que es una constatación del anexo
  y no una falla de la clasificación.
- Es un proyecto de ley: las cifras cambian con el debate parlamentario y con la
  autógrafa.

## Catálogo de pliegos

`catalogo-pliegos-2027.csv`. Una fila por pliego, derivada de las bases. La clave es el
par de `departamento` y `codigo_pliego`.

| Variable | Contenido |
|---|---|
| `departamento` | Región a la que corresponde la fila |
| `codigo_pliego` | Clave de unión con las bases |
| `pliego` | Denominación |
| `nivel_gobierno` | Nacional, regional o local |
| `provincia`, `distrito` | Jurisdicción, en los pliegos locales |
| `anexos` | Anexos donde aparece el pliego |
| `n_asignaciones` | Filas que el pliego aporta a la base no duplicada |
| `monto_asignado_soles` | Monto según la regla declarada en la columna siguiente |
| `concepto_del_monto` | Qué mide el monto |
| `referencia_paginas_pdf` | Páginas por archivo, con rangos comprimidos |

`concepto_del_monto` es la columna que evita el error de lectura más probable: para los
pliegos con sede en el departamento el monto es el presupuesto institucional completo,
mientras que para los ministerios es solo la porción localizada allí. **Las dos cifras no
son comparables y sumar la columna entera mezcla ambas magnitudes.**
