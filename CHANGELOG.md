# Registro de cambios

Las versiones siguen el esquema `AÑO.N`, donde N se incrementa con cada publicación.
Cada entrada indica el estado de cierre de los pliegos, que es el control que decide si
una base puede publicarse.

## 2027.5 — Reconstrucción de la referencia y cierre del nivel nacional

**Las cuatro bases fueron regeneradas.** Ninguna región se agrega en esta versión, pero
todas cambian: las correcciones alcanzan a los anexos 4 y 5, de los que dependen las
partidas nacionales de cada base y la validación de todos los pliegos.

Estado: Tacna 30 de 30 pliegos propios y Moquegua 23 de 23, ambas sin observaciones en el
control; Puno 109 de 112 y Arequipa 108 de 111. Base conjunta: S/ 18 410 272 218 en 340
pliegos.

Correcciones a la referencia del anexo 4:

- El código de pliego se repite entre sectores, de modo que deduplicar por código al sumar
  los niveles perdía entidades enteras. La unidad es el par de código y nombre.
- El reconocimiento óptico leyó 484 donde el anexo dice 464, con lo que el Gobierno
  Regional de la Provincia Constitucional del Callao se contaba como pliego nacional. Su
  monto, S/ 1 935 677 477, era exactamente la brecha del nivel regional.
- Se incorporaron 25 pliegos que faltaban por deformación del nombre, entre ellos la
  Presidencia del Consejo de Ministros, el Poder Judicial, el Ministerio de Cultura y el
  INPE, además de tres municipalidades que aparecían en el anexo 8 sin contraparte en el 7.
- El nivel regional cierra ahora exacto contra el total impreso; el nacional queda a 1,3 %
  y el local a 0,78 %.

Correcciones a la lectura del anexo 5:

- Un token de la cola puede valer por dos o tres grupos de miles, porque el OCR pierde el
  espacio que los separa. Así se recuperaron S/ 858 millones del Ministerio de Transportes,
  impresos como «781 32B797».
- El primer grupo no se toma cuando parece un año del propio nombre y la cola ya tiene
  forma completa de importe. Era el caso de «Juegos Panamericanos Lima 2027», donde el año
  se sumaba al monto y lo invalidaba: S/ 369 millones del Instituto Peruano del Deporte.
- Como el transporte concentra las mayores inversiones nacionales en cada región, esas
  partidas faltaban también en las bases departamentales publicadas antes.

Contraste entre anexos:

- El emparejamiento entre el anexo 4 y el anexo 5 se hace por código y no por nombre. Con
  el nombre coincidían 132 de 159 pliegos; con el código emparejan los 158 que tienen
  bloque en ambos, y el nombre queda solo para desempatar los códigos repetidos entre
  sectores. De esos 158 coinciden exactamente 147 y la diferencia total baja de S/ 391
  millones a S/ 22 millones.

## 2027.4 — Arequipa, y correcciones que alcanzan a todas las bases

Publicación nueva:

- `asignaciones-arequipa-2027.csv`: 1 990 asignaciones, 109 pliegos propios, de los cuales
  cierran 105. Base no duplicada: S/ 7 689 419 636. Es la región más grande de la serie.
- El catálogo pasa a cubrir 340 pliegos de las cuatro regiones, con una base conjunta de
  S/ 18 394 920 353.

**Las cuatro bases fueron regeneradas y sus cifras cambian.** Las correcciones de esta
versión afectan a todas, así que conviene reemplazarlas juntas y no mezclar versiones.

Correcciones al procedimiento de extracción:

- El lector por coordenadas no unía las líneas de continuación del nombre de una partida.
  Como en el anexo 5 la denominación termina con el bloque de ubicación, una partida cuyo
  nombre se parte dejaba la mención del departamento en la línea siguiente y quedaba fuera
  de la base. Las partidas nacionales localizadas en Tacna pasan de diez a veintiséis.
- El código del departamento se aprende ahora del encabezado, que está impreso a una
  sangría menor que el de la provincia, en lugar de deducirse de las coincidencias. Si un
  bloque departamental abre con varios homónimos, el contexto anterior los arrastraba al
  departamento equivocado: así, Coporaque de Arequipa había absorbido S/ 16,9 millones de
  su homónimo del Cusco.
- Se agrega coincidencia por prefijo para los nombres que el anexo trunca. La comparación
  aproximada no alcanzaba el umbral: «Municipalidad Distrital de Coronel Gregorio» y el
  nombre completo con «Albarracín Lanchipa» quedan en 0,81 de similitud.
- Una reconciliación final compara, pliego por pliego, la suma de cada fuente contra la
  que declara el anexo 4. Cuando una fuente excede lo declarado y existe un único
  componente de esa fuente cuyo valor es exactamente el exceso, ese componente se retira.
  Aparece cuando el reconocimiento óptico daña el total de una línea y la diferencia se
  materializa como una celda fantasma.
- Se corrige el patrón del anexo 8, que solo reconocía provincias 01 a 03. Las bases de
  Puno y Arequipa publicadas antes estaban incompletas en ese anexo: Puno pasa de 307 a
  768 filas y Arequipa de 309 a 582.
- La marca de cuadre dentro de las bases aplica ahora la regla de coherencia del total: el
  del anexo 4 vale solo si sus propias fuentes lo suman. Sin ella, la Municipalidad
  Provincial de Tarata figuraba como descuadrada por un dígito dañado en la referencia.

Efecto sobre el conjunto del país: el extractor del anexo 7 identifica 1 880 de los 1 887
pliegos locales y cierra 1 836, frente a los 1 744 de la versión anterior.

## 2027.3 — Puno

- Se agrega `asignaciones-puno-2027.csv`. No cierran cuatro pliegos, marcados fila por fila
  en `cuadra_el_pliego`. El gobierno regional queda corto en S/ 7 789 915 porque tres
  proyectos de la misma subsección tienen el importe ilegible en el PDF y no pueden
  repartirse sin inventar.
- Se agrega `departamento` a la base de Tacna y se unifica el orden de columnas: las bases
  comparten las mismas 25 variables en el mismo orden.

Correcciones al procedimiento:

- Las municipalidades homónimas dentro de un mismo departamento —Puno tiene tres Santa
  Rosa— se guardan en orden de código y se consumen secuencialmente. Antes el índice
  conservaba solo la última.
- El filtro territorial de las partidas nacionales exige el nombre del departamento. Los
  nombres de distrito son demasiado comunes para servir por sí solos.

## 2027.2 — Moquegua

- Se agrega `asignaciones-moquegua-2027.csv`, con sus 23 pliegos propios cerrando.
- Se unifica el nombre de cada pliego con su código en todas las bases.
- Se reconstruye el extractor del anexo 7: anclaje de columnas calculado una sola vez para
  todo el anexo sobre los propios datos, identificación del pliego por el último nombre
  inequívoco visto, y cierre final por diferencia cuando una sola línea no reconcilia.

## 2027.1 — Tacna

- Primera publicación: `asignaciones-tacna-2027.csv`, con sus 30 pliegos propios cerrando.
- Lectura de los PDF por coordenadas en lugar de texto plano.
- Apéndice metodológico y script de control.
