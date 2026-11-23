"""Interfaz de terminal para gestionar clientes, servicios y reservas."""
from logger import configurar_logger
from cliente import Cliente
from excepciones import SoftwareFJError
from reserva import Reserva
from servicios import AlquilerEquipo, Asesoria, ReservaSala


logger = configurar_logger()


def _ejecutar_operacion(nombre, accion):
    """Ejecuta una operación del sistema e informa los errores esperados."""
    print(f"\n{nombre}:")
    try:
        resultado = accion()
    except SoftwareFJError as error:
        logger.exception("La operacion '%s' no se pudo completar", nombre)
        print(f"[ERROR] {error}")
        resultado = None
    else:
        logger.info("La operacion '%s' se completo", nombre)
        if resultado is not None:
            print(f"[OK] {resultado}")
    finally:
        logger.info("Intento de operacion finalizado: %s", nombre)
    return resultado


def _leer_entero(mensaje):
    """Solicita un entero y vuelve a preguntar si el formato no es válido."""
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("[ERROR] Ingresa un número entero.")


def _leer_decimal(mensaje):
    """Solicita un número decimal y vuelve a preguntar si no se puede leer."""
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("[ERROR] Ingresa un número válido.")


def _buscar_por_id(elementos, identificador, obtener_id):
    """Encuentra un elemento por identificador o devuelve None."""
    return next(
        (elemento for elemento in elementos if obtener_id(elemento) == identificador),
        None,
    )


def _registrar_cliente(clientes):
    cliente = _ejecutar_operacion(
        "Registrar cliente",
        lambda: Cliente(
            input("Nombre: "),
            input("Documento: "),
            input("Correo: "),
            input("Teléfono: "),
        ),
    )
    if cliente is not None:
        clientes.append(cliente)


def _registrar_servicio(servicios):
    print("\nTipo de servicio: 1) Sala  2) Alquiler de equipo  3) Asesoría")
    tipo = input("Selecciona el tipo: ").strip()
    if tipo not in {"1", "2", "3"}:
        print("[ERROR] Tipo de servicio no válido.")
        return

    nombre = input("Nombre del servicio: ")
    tarifa = _leer_decimal("Tarifa por hora: ")
    if tipo == "1":
        servicio = _ejecutar_operacion(
            "Registrar sala",
            lambda: ReservaSala(
                nombre,
                tarifa,
                _leer_entero("Capacidad de la sala: "),
            ),
        )
    elif tipo == "2":
        servicio = _ejecutar_operacion(
            "Registrar alquiler de equipo",
            lambda: AlquilerEquipo(
                nombre,
                tarifa,
                input("Tipo de equipo: "),
            ),
        )
    else:
        servicio = _ejecutar_operacion(
            "Registrar asesoría",
            lambda: Asesoria(
                nombre,
                tarifa,
                input("Especialidad: "),
            ),
        )

    if servicio is not None:
        servicios.append(servicio)


def _listar_clientes(clientes):
    print("\nClientes registrados:")
    if not clientes:
        print("No hay clientes registrados.")
        return
    for cliente in clientes:
        print(cliente.describir())


def _listar_servicios(servicios):
    print("\nServicios registrados:")
    if not servicios:
        print("No hay servicios registrados.")
        return
    for servicio in servicios:
        print(servicio.describir())


def _crear_reserva(clientes, servicios, reservas):
    if not clientes or not servicios:
        print("[ERROR] Registra al menos un cliente y un servicio primero.")
        return
    _listar_clientes(clientes)
    cliente_id = _leer_entero("ID del cliente: ")
    cliente = _buscar_por_id(clientes, cliente_id, lambda elemento: elemento.id_cliente)
    if cliente is None:
        print("[ERROR] No existe un cliente con ese ID.")
        return

    _listar_servicios(servicios)
    servicio_id = _leer_entero("ID del servicio: ")
    servicio = _buscar_por_id(servicios, servicio_id, lambda elemento: elemento.id)
    if servicio is None:
        print("[ERROR] No existe un servicio con ese ID.")
        return

    reserva = _ejecutar_operacion(
        "Crear reserva",
        lambda: Reserva(cliente, servicio, _leer_decimal("Duración en horas: ")),
    )
    if reserva is not None:
        reservas.append(reserva)


def _listar_reservas(reservas):
    print("\nReservas:")
    if not reservas:
        print("No hay reservas registradas.")
        return
    for reserva in reservas:
        print(reserva.describir())


def _gestionar_reserva(reservas):
    if not reservas:
        print("No hay reservas para gestionar.")
        return
    _listar_reservas(reservas)
    identificador = _leer_entero("ID de la reserva: ")
    reserva = _buscar_por_id(reservas, identificador, lambda elemento: elemento.id)
    if reserva is None:
        print("[ERROR] No existe una reserva con ese ID.")
        return

    print("Acción: 1) Confirmar  2) Procesar  3) Cancelar")
    accion = input("Selecciona la acción: ").strip()
    if accion == "1":
        _ejecutar_operacion("Confirmar reserva", reserva.confirmar)
    elif accion == "2":
        impuesto = _leer_porcentaje("Impuesto (Enter para usar 19 %): ", 0.19)
        descuento = _leer_porcentaje("Descuento (Enter para usar 0 %): ", 0.0)
        _ejecutar_operacion(
            "Procesar reserva",
            lambda: reserva.procesar(impuesto=impuesto, descuento=descuento),
        )
    elif accion == "3":
        _ejecutar_operacion("Cancelar reserva", reserva.cancelar)
    else:
        print("[ERROR] Acción no válida.")


def _leer_porcentaje(mensaje, predeterminado):
    """Lee un porcentaje como proporción; Enter conserva el valor sugerido."""
    while True:
        valor = input(mensaje).strip()
        if not valor:
            return predeterminado
        try:
            return float(valor)
        except ValueError:
            print("[ERROR] Ingresa un número válido o presiona Enter.")


def ejecutar_demostracion():
    """Ejecuta los 15 ejemplos válidos e inválidos del proyecto."""
    logger.info("=== Inicio de la demostración integral ===")
    operaciones = []

    def ejecutar(nombre, accion):
        resultado = _ejecutar_operacion(nombre, accion)
        operaciones.append((nombre, resultado))
        return resultado

    cliente = ejecutar(
        "1. Registrar cliente válido",
        lambda: Cliente("Juan Pérez", "1012345678", "juan@correo.com", "3001234567"),
    )
    ejecutar(
        "2. Intentar registrar cliente inválido",
        lambda: Cliente.crear_seguro("", "abc", "correo-malo", "123"),
    )

    sala = ejecutar(
        "3. Crear sala disponible",
        lambda: ReservaSala("Sala Juntas A", 5000, 10),
    )
    equipo = ejecutar(
        "4. Crear alquiler de equipo",
        lambda: AlquilerEquipo("Portátil Dell", 20000, "Laptop"),
    )
    ejecutar(
        "5. Crear asesoría especializada",
        lambda: Asesoria("Consultoría Cloud", 80000, "AWS"),
    )
    ejecutar(
        "6. Intentar crear servicio inválido",
        lambda: AlquilerEquipo("Equipo sin tipo", 20000, ""),
    )

    reserva_sala = ejecutar(
        "7. Crear reserva de sala",
        lambda: Reserva(cliente, sala, 2),
    )
    if reserva_sala is not None:
        ejecutar("8. Confirmar reserva de sala", reserva_sala.confirmar)
        ejecutar("9. Procesar reserva con impuesto", reserva_sala.procesar)

    reserva_equipo = ejecutar(
        "10. Crear reserva de equipo",
        lambda: Reserva(cliente, equipo, 3),
    )
    if reserva_equipo is not None:
        ejecutar("11. Cancelar reserva de equipo", reserva_equipo.cancelar)
    if reserva_sala is not None:
        ejecutar(
            "12. Intentar cancelar reserva completada",
            reserva_sala.cancelar,
        )

    servicio_no_disponible = ejecutar(
        "13. Crear asesoría no disponible",
        lambda: Asesoria("Asesoría de redes", 60000, "Redes", disponible=False),
    )
    if servicio_no_disponible is not None:
        ejecutar(
            "14. Intentar reservar servicio no disponible",
            lambda: Reserva(cliente, servicio_no_disponible, 1),
        )
    ejecutar(
        "15. Intentar reservar duración inválida",
        lambda: Reserva(cliente, sala, 0),
    )

    logger.info(
        "=== Fin de la demostración: %s operaciones ejecutadas ===",
        len(operaciones),
    )
    print(f"\nDemostración finalizada: {len(operaciones)} operaciones.")
    return operaciones


def main():
    """Ejecuta el menú interactivo de gestión en la terminal."""
    logger.info("=== Inicio del sistema interactivo ===")
    clientes = []
    servicios = []
    reservas = []

    while True:
        print(
            "\n=== Software FJ ===\n"
            "1. Registrar cliente\n"
            "2. Registrar servicio\n"
            "3. Listar clientes\n"
            "4. Listar servicios\n"
            "5. Crear reserva\n"
            "6. Gestionar reserva\n"
            "7. Listar reservas\n"
            "8. Ejecutar demostración\n"
            "0. Salir"
        )
        opcion = input("Selecciona una opción: ").strip()
        if opcion == "0":
            print("Hasta pronto.")
            logger.info("=== Fin del sistema interactivo ===")
            return
        if opcion == "1":
            _registrar_cliente(clientes)
        elif opcion == "2":
            _registrar_servicio(servicios)
        elif opcion == "3":
            _listar_clientes(clientes)
        elif opcion == "4":
            _listar_servicios(servicios)
        elif opcion == "5":
            _crear_reserva(clientes, servicios, reservas)
        elif opcion == "6":
            _gestionar_reserva(reservas)
        elif opcion == "7":
            _listar_reservas(reservas)
        elif opcion == "8":
            ejecutar_demostracion()
        else:
            print("[ERROR] Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    main()
