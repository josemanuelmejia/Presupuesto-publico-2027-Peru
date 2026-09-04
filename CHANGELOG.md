# Registro de cambios

Las versiones siguen el esquema `AÑO.N`, donde N se incrementa con cada publicación.
Cada entrada indica el estado de cierre de los pliegos, que es el control que decide si
una base puede publicarse.

## 2027.3 — Puno

- Se agrega `asignaciones-puno-2027.csv`: 1 870 asignaciones, 112 pliegos propios, de los
  cuales cierran 108. Base no duplicada: S/ 5 929 375 720.
- No cierran cuatro pliegos, marcados fila por fila en `cuadra_el_pliego`. El gobierno
  regional queda corto en S/ 7 789 915 porque tres proyectos de la misma subsección tienen
  el importe ilegible en el PDF y no pueden repartirse sin inventar. Los otros tres son
  municipales: uno con un dígito mal leído y un par con líneas atribuidas cruzadas.
- Se agrega `departamento` a la base de Tacna y se unifica el orden de columnas: las tres
  bases comparten ahora las mismas 25 variables en el mismo orden.
- El catálogo pasa a llamarse `catalogo-pliegos-2027.csv` y cubre 201 pliegos.

Correcciones al procedimiento de extracción, con efecto sobre todo el país:

- Las municipalidades homónimas dentro de un mismo departamento —Puno tiene tres Santa
  Rosa— se guardan en orden de código y se consumen secuencialmente. Antes el índice
  conservaba solo la última, con lo que dos pliegos desaparecían y otros dos se inflaban.
- El filtro territorial de las partidas nacionales exige el nombre del departamento. Los
  nombres de distrito son demasiado comunes para servir por sí solos.

## 2027.2 — Moquegua

- Se agrega `asignaciones-moquegua-2027.csv`: 709 asignaciones, 23 pliegos propios, todos
  cerrando. Base no duplicada: S/ 2 027 679 753.
- Se unifica el nombre de cada pliego con su código en ambas bases.
- Se reconstruye el extractor del anexo 7: anclaje de columnas calculado una sola vez para
  todo el anexo sobre los propios datos, identificación del pliego por el último nombre
  inequívoco visto, y cierre final por diferencia cuando una sola línea no reconcilia.

## 2027.1 — Tacna

- Primera publicación: `asignaciones-tacna-2027.csv`, 854 asignaciones, 30 pliegos propios,
  todos cerrando. Base no duplicada: S/ 2 562 810 850.
- Lectura de los PDF por coordenadas en lugar de texto plano.
- Apéndice metodológico y script de control.
