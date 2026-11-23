# FASE-4 — Sistema integral de Software FJ

Proyecto académico de Programación de la UNAD para gestionar clientes,
servicios y reservas mediante programación orientada a objetos. Los datos se
mantienen en objetos y listas en memoria; no se utiliza una base de datos. El
archivo `logs.txt` guarda los eventos y errores.

## Integrantes

- JEFERSSON ANDRES BAUTISTA VEGA
- ANGEL SEBASTIAN ROMERO BUITRAGO
- LUIS ALEJANDRO REYES DIAZ
- FABIAN ANDRES BOLANO ALEAN

## Requisitos del ejercicio

- `Entidad` es la clase abstracta que comparte el identificador y la descripción
  de las entidades del sistema.
- `Cliente` valida y encapsula nombre, documento, correo y teléfono. También
  administra su lista interna de reservas y entrega una copia al consultarla.
- `Servicio` es la clase base abstracta. `ReservaSala`, `AlquilerEquipo` y
  `Asesoria` heredan sus datos y validan sus propios parámetros.
- Los servicios especializados sobrescriben `describir` y `calcular_costo`.
  Como el enunciado no define tarifas diferentes por tipo, sus cálculos delegan
  la fórmula común a `Servicio`: tarifa por horas, descuento e impuesto.
- `Reserva` vincula un cliente con un servicio y una duración. Su flujo permite
  confirmar, cancelar o procesar la reserva, con los estados pendiente,
  confirmada, cancelada y completada.
- Las clases usan excepciones propias para informar datos inválidos, servicios
  no disponibles, operaciones no permitidas y cálculos inconsistentes. Los
  parámetros obligatorios omitidos también producen errores propios que quedan
  registrados. Las operaciones inválidas de la demostración no impiden ejecutar
  las siguientes.
- En Python, `calcular_costo(horas, impuesto=0.19, descuento=0.0)` permite
  distintas variantes mediante parámetros opcionales y nombrados. Por ejemplo:

  ```python
  servicio.calcular_costo(2)
  servicio.calcular_costo(2, 0.1)
  servicio.calcular_costo(2, impuesto=0.1, descuento=0.25)
  ```

  Python no selecciona métodos por sobrecarga de firmas en tiempo de ejecución;
  esta interfaz ofrece las variantes solicitadas sin duplicar la fórmula.

## Ejecutar el sistema interactivo

Se requiere Python 3 y no se necesitan dependencias externas. Abre una
terminal, entra en la carpeta del proyecto y ejecuta:

```bash
cd FASE-4
python3 main.py
```

Si ya estás dentro de `FASE-4`, ejecuta directamente `python3 main.py`. El
programa mostrará el menú y esperará que escribas el número de una opción en la
terminal. Después de cada acción volverá al menú:

| Opción | Acción |
| --- | --- |
| `1` | Registrar cliente: ingresa nombre, documento, correo y teléfono cuando se soliciten. |
| `2` | Registrar servicio: elige sala, alquiler de equipo o asesoría y completa los datos solicitados. |
| `3` | Mostrar los clientes registrados y sus identificadores. |
| `4` | Mostrar los servicios registrados y sus identificadores. |
| `5` | Crear reserva: elige el ID de un cliente, el ID de un servicio y la duración en horas. |
| `6` | Gestionar una reserva: indica su ID y luego confirma, procesa o cancela. |
| `7` | Mostrar las reservas y su estado actual. |
| `8` | Ejecutar la demostración automática de 15 operaciones de ejemplo. |
| `0` | Salir del programa. |

Para completar una reserva, primero créala con la opción `5`, confírmala con
`6` → `1` y luego procésala con `6` → `2`. Al procesarla puedes presionar
`Enter` para usar el impuesto predeterminado (19 %) y el descuento
predeterminado (0 %). Si ingresas valores, hazlo como proporciones: por ejemplo,
`0.19` equivale a 19 % y `0.10` equivale a 10 %. Solo se pueden procesar
reservas confirmadas; las opciones inválidas o los datos incorrectos muestran
un error y el menú permite continuar.

Los clientes, servicios y reservas se conservan únicamente mientras el
programa está abierto; al salir se pierden. Los eventos y errores quedan
registrados en `logs.txt`.

## Ejecutar las pruebas

Desde la carpeta del proyecto (`FASE-4`), ejecuta:

```bash
python3 -m unittest discover -s tests -v
```

Las pruebas comprueban las validaciones de los servicios, las variantes de
cálculo, la asociación de reservas al cliente, las transiciones de estado, la
interacción con el menú y la demostración de más de diez operaciones.

## Uso de inteligencia artificial

Se utilizó inteligencia artificial como apoyo para la corrección de errores y
la documentación del código. El equipo revisó e integró los cambios y es
responsable del contenido y del funcionamiento del proyecto.
