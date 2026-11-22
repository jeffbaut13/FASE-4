# FASE-4 — Sistema integral de Software FJ

Proyecto académico de Programación de la UNAD para gestionar clientes,
servicios y reservas mediante programación orientada a objetos. Los datos se
mantienen en objetos y listas en memoria; no se utiliza una base de datos. El
archivo `logs.txt` guarda los eventos y errores.

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

## Ejecutar la demostración

Se requiere Python 3 y no se necesitan dependencias externas:

```bash
python3 main.py
```

La demostración ejecuta 15 operaciones válidas e inválidas: registra un
cliente correcto e intenta registrar datos incorrectos; crea servicios
correctos e incorrectos; crea, confirma, procesa y cancela reservas; e intenta
operaciones que deben rechazarse. Los errores esperados se informan en pantalla
y se escriben en `logs.txt`.

## Ejecutar las pruebas

```bash
python3 -m unittest discover -s tests -v
```

Las pruebas comprueban las validaciones de los servicios, las variantes de
cálculo, la asociación de reservas al cliente, las transiciones de estado, los
errores recuperables y la ejecución de más de diez operaciones en la
demostración.
